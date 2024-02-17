import asyncio
import pickle
import socket
import struct

import loguru
from pydantic import BaseModel

from web.kernel.types import ConfAble, SocketConf, SignalType
from web.utils.logger import LoggerSettings


def get_reserved_ports(conf):
    ports = []

    def _get_ports(_conf):
        for attr in vars(_conf).values():
            if isinstance(attr, SocketConf) and attr.port:
                ports.append(attr.port)
            elif issubclass(attr.__class__, BaseModel):
                _get_ports(attr)

    _get_ports(conf)
    return ports


def get_free_port(exclude_ports):
    min_port = 9000
    max_port = 65535
    start_port = max(exclude_ports)
    cur_port = start_port + 1
    while 1:
        if cur_port >= max_port:
            cur_port = min_port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', cur_port)) != 0:
                return cur_port
        cur_port += 1


class SocketHandler:
    """
    Child process log handler
    """

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def write(self, message):
        record = message.record
        data = pickle.dumps(record)
        slen = struct.pack(">L", len(data))
        self.sock.send(slen + data)


class SocketLogger(ConfAble[LoggerSettings]):

    def __init__(self):
        self.port = None
        self.socket = None

    @staticmethod
    async def handle_log_req(client):
        """
        Parent process log handler
        """
        loop = asyncio.get_event_loop()
        while 1:
            chunk = await loop.sock_recv(client, 4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = await loop.sock_recv(client, slen)
            while len(chunk) < slen:
                chunk = chunk + await loop.sock_recv(client, slen - len(chunk))
            record = pickle.loads(chunk)
            level, message = record["level"].name, record["message"]

            loguru.logger.patch(lambda _record: _record.update(record)).log(level, message)
        client.close()

    async def before_app_start(self, app: "WebApp"):
        try:
            self.conf  # check if conf is set
            self.port = self.conf.socket_port or self.port
        except RuntimeError:
            pass
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if not self.port:
            used_ports = get_reserved_ports(app.conf)
            self.port = get_free_port(used_ports)
            loguru.logger.warning(f"Port for logs socket not set in conf! Used port: {self.port}")
        self.socket.bind(('localhost', self.port))
        self.socket.listen(5)
        self.socket.setblocking(False)

        loop = asyncio.get_event_loop()

        async def handle_logs():
            try:
                while 1:
                    client, _ = await loop.sock_accept(self.socket)
                    loop.create_task(self.handle_log_req(client))
            except Exception as e:
                loguru.logger.error(e)
            finally:
                self.socket.close()

        loop.create_task(handle_logs())

        for transport in app._transports:
            transport.on_signal(SignalType.BEFORE_TRANSPORT_WORK, self.before_transport_work(self.port))

    async def after_app_stop(self, app):
        self.socket.close()

    @staticmethod
    def before_transport_work(port):
        async def _before_work(transport):
            loguru.logger.configure(handlers=[{"sink": SocketHandler('localhost', port)}])
        return _before_work
