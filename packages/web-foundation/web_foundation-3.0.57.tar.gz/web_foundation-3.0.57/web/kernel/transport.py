from __future__ import annotations

import os
from abc import ABCMeta
from pathlib import Path
from typing import List, Any, Dict, Tuple

import loguru

from web import settings
from web.kernel.messaging.channel import GenIMessage
from web.kernel.proc.isolate import Isolate
from web.kernel.types import ISocket, RtWriter, \
    GenEventsType, RtResolver, BackTaskTarget, BackTaskTrigger, BackTaskCallback, TaskReturnEvent, \
    TaskEvent, ITransport, PluginContainer, GenAsyncCall, call_signals, SignalType


class Transport(ITransport, metaclass=ABCMeta):
    async def new_rt(self, writer: RtWriter,
                     events_type: GenEventsType,
                     resolver: RtResolver,
                     use_nested_events: bool = False):
        """
        Start new real-time connection
        :param writer: RtWriter for communication with connection
        :param events_type: Type of events, that will be resolved in connection
        :param resolver: Resolve events
        :param use_nested_events: Set True if need to resolve all subclasses of events_type
        """
        if writer.__class__ not in self.rt_writers.keys():
            self.rt_writers[writer.__class__] = []
        self.rt_writers[writer.__class__].append(writer)

        async def send_in_writer(message: GenIMessage):
            if writer.__class__ not in self.rt_writers or writer not in self.rt_writers[writer.__class__]:
                return
            if msg := await resolver(writer, message):
                await writer.write(msg.prepare(writer.last_index))

        self.channel.add_event_listener(events_type, send_in_writer,
                                        use_nested_classes=use_nested_events)

        async def on_disconnect():
            if writer.__class__ in self.rt_writers and writer in self.rt_writers[writer.__class__]:
                self.rt_writers[writer.__class__].remove(writer)
            self.channel.remove_event_listener(events_type, send_in_writer,
                                               use_nested_classes=use_nested_events)

        await writer.with_lost_callback(on_disconnect).run()

    async def back_task(self,
                        target: BackTaskTarget,
                        args=None,
                        kwargs=None,
                        trigger: BackTaskTrigger = None,
                        exec_type: str = "default",
                        on_error: BackTaskCallback = None,
                        on_complete: BackTaskCallback = None,
                        need_result: bool = False
                        ) -> TaskReturnEvent | None:
        """
        Add task to background scheduler
        :param target: Target func
        :param trigger: AioScheduler Trigger; if None - start task immediately
        :param exec_type:
        :param on_error:
        :param on_complete:
        :param need_result:
        :return:
        """
        if kwargs is None:
            kwargs = {}
        if args is None:
            args = []
        if not settings.SCHEDULER_ENABLE:
            raise ImportError("Apscheduler is not installed on your system. scheduler not enable")
        else:
            return await self.channel.produce(TaskEvent(
                target,
                trigger=trigger,
                args=args,
                kwargs=kwargs,
                exec_type=exec_type,
                on_error=on_error,
                on_complete=on_complete
            ), need_answer=need_result)

    async def set_plugin(self, file_path: Path) -> Tuple[str, str | Exception]:
        container = PluginContainer(file_path)
        status, message = container.import_plugin()
        if status == "success":
            await self._plugins_store.set(container.plugin.name, container)
        if settings.DEBUG:
            getattr(loguru.logger, status)(f"[{self.__class__.__name__}::{self._plugins_store}::{container}] {message}")
        return status, message

    async def remove_plugin(self, plugin_name: str):
        await self._plugins_store.remove(plugin_name)


class TransportIsolate(Isolate):
    _transport: Transport
    _socket: ISocket

    def __init__(self, name: str, transport: Transport, socket: ISocket, **kwargs):
        super().__init__(name, **kwargs)
        self._transport = transport
        self._socket = socket

    async def work(self, *args, **kwargs) -> None:
        self._transport.init_plugins()
        await call_signals(self._transport, SignalType.BEFORE_TRANSPORT_WORK, self._transport)
        loguru.logger.info(f"[{self.name}::Isolate(pid={os.getpid()})]: socket {self._socket}")
        await self._transport.run(self._socket)
