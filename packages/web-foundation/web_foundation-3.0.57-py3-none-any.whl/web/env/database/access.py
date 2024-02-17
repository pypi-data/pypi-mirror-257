import asyncio
import json as py_json
from typing import List, Type, Coroutine, Callable, Any

from sanic.exceptions import NotFound, MethodNotAllowed

from web.env.database.model_loader import ModelLoader
from web.env.database.models import AbstractDbModel
from web.kernel.transport import Transport
from web.trend.rest.custom import InputContext

AccessCallback = Callable[
    [AbstractDbModel | List[AbstractDbModel] | None, InputContext, Type[ModelLoader]], Coroutine[
        Any, Any, None]]


def extend_fields(main_list: list, add_list: list) -> list:
    if main_list is None:
        main_list = []
    main_list.extend(add_list)
    return main_list


def update_dict(main_dict: dict, add_dict: dict) -> dict:
    if main_dict is None:
        main_dict = {}
    return main_dict | add_dict


async def exec_access(inc: InputContext,
                      model: Type[AbstractDbModel],
                      transport: Transport = None,
                      fetch_fields: List[str] = None,
                      fetch_fields_on_read: List[str] = None,
                      fetch_fields_on_read_all: List[str] = None,
                      drop_cols: List[str] = None,
                      select_values: List[str] = None,
                      select_values_on_read: List[str] = None,
                      select_values_on_read_all: List[str] = None,
                      select_values_rename: dict[str, str] = None,
                      select_values_on_read_rename: dict[str, str] = None,
                      select_values_on_read_all_rename: dict[str, str] = None,
                      full_info: bool = False,
                      middleware: Type[ModelLoader] = ModelLoader,
                      external_callback: AccessCallback = None,
                      retrieved_callback: AccessCallback = None,
                      extended_methods: dict[str, str] = None,
                      ):
    """
    Access to models
    """
    match inc.request.method:
        case "GET":
            kwargs = inc.r_kwargs
            entity_id = kwargs.pop("entity_id", None)
            if entity_id is None:
                limit = inc.request.args.get("limit")
                offset = inc.request.args.get("offset")
                limit = int(limit) if limit and limit.isdigit() else 100
                offset = int(offset) if offset and offset.isdigit() else None
                # order_by = inc.request.args.get("order_by")  # for openapi. Variable forwarded to read_all in kwargs
                for ar, val in inc.request.args.items():
                    if ar in ["limit", "offset"]:
                        continue
                    val = val[0]
                    if val.lower() == 'false':
                        val = False
                    elif val.lower() == 'true':
                        val = True
                    elif val.lower() == 'none':
                        val = None
                    elif val.isdigit():
                        val = int(val)
                    elif "." in val and val.replace('.', '').isdigit():
                        val = float(val)
                    elif val.startswith("[") or val.startswith("{"):
                        val = py_json.loads(val)
                    kwargs[ar] = val

                if fetch_fields_on_read_all is not None:
                    fetch_fields = extend_fields(fetch_fields, fetch_fields_on_read_all)
                if select_values_on_read_all is not None:
                    select_values = extend_fields(select_values, select_values_on_read_all)
                if select_values_on_read_all_rename is not None:
                    select_values_rename = update_dict(select_values_rename, select_values_on_read_all_rename)
                retrieved_all, total = await middleware.read_all(model=model, protection=inc.identity, limit=limit,
                                                                 offset=offset,
                                                                 transport=transport,
                                                                 fetch_fields=fetch_fields,
                                                                 select_values=select_values,
                                                                 select_values_rename=select_values_rename,
                                                                 **kwargs)
                if external_callback:
                    asyncio.create_task(external_callback(retrieved_all, inc, middleware))
                if retrieved_callback:
                    return await retrieved_callback(retrieved_all, inc, middleware)
                if retrieved_all and isinstance(retrieved_all[0], dict):
                    return retrieved_all, total
                res = [await _model.values_dict(drop_cols=drop_cols, full_info=full_info) for _model in retrieved_all]
                return res, total
            if fetch_fields_on_read is not None:
                fetch_fields = extend_fields(fetch_fields, fetch_fields_on_read)
            if select_values_on_read is not None:
                select_values = extend_fields(select_values, select_values_on_read)
            if select_values_on_read_rename is not None:
                select_values_rename = update_dict(select_values_rename, select_values_on_read_rename)
            retrieved = await middleware.read(model=model, entity_id=entity_id, protection=inc.identity,
                                              transport=transport,
                                              fetch_fields=fetch_fields,
                                              select_values=select_values,
                                              select_values_rename=select_values_rename,
                                              **kwargs)
            if not retrieved:
                raise NotFound()

        case "POST":
            retrieved = await middleware.create(model=model, protection=inc.identity, dto=inc.dto,
                                                transport=transport, **inc.r_kwargs)

        case "PATCH":
            entity_id = inc.r_kwargs.pop("entity_id")
            retrieved = await middleware.update(model=model, entity_id=entity_id, protection=inc.identity, dto=inc.dto,
                                                transport=transport, **inc.r_kwargs)

        case "DELETE":
            entity_id = inc.r_kwargs.pop("entity_id")
            retrieved = await middleware.delete(model=model, entity_id=entity_id, protection=inc.identity,
                                                transport=transport, **inc.r_kwargs)

        case _:
            if extended_methods and inc.request.method in extended_methods and hasattr(
                    middleware, extended_methods[inc.request.method]):
                retrieved = await getattr(middleware, extended_methods[inc.request.method])(
                    model=model, protection=inc.identity, transport=transport, dto=inc.dto, **inc.r_kwargs)
            else:
                allowed_methods = ["GET", "POST", "PATCH", "DELETE"]
                if extended_methods:
                    allowed_methods.extend(list(extended_methods.keys()))
                raise MethodNotAllowed(message=f"Method {inc.request.method} not allowed",
                                       method=inc.request.method, allowed_methods=extended_methods)

    if external_callback:
        asyncio.create_task(external_callback(retrieved, inc, middleware))
    if retrieved_callback:
        return await retrieved_callback(retrieved, inc, middleware)
    if isinstance(retrieved, list):
        return [await i.values_dict(drop_cols=drop_cols, full_info=full_info) for i in retrieved]
    elif isinstance(retrieved, dict):
        return retrieved
    return await retrieved.values_dict(drop_cols=drop_cols, full_info=full_info)


async def exec_access_with_total(inc: InputContext,
                                 model: Type[AbstractDbModel],
                                 transport: Transport = None,
                                 fetch_fields: List[str] = None,
                                 fetch_fields_on_read: List[str] = None,
                                 fetch_fields_on_read_all: List[str] = None,
                                 drop_cols: List[str] = None,
                                 select_values: List[str] = None,
                                 select_values_on_read: List[str] = None,
                                 select_values_on_read_all: List[str] = None,
                                 select_values_rename: dict[str, str] = None,
                                 select_values_on_read_rename: dict[str, str] = None,
                                 select_values_on_read_all_rename: dict[str, str] = None,
                                 full_info: bool = False,
                                 middleware: Type[ModelLoader] = ModelLoader,
                                 external_callback: AccessCallback = None,
                                 retrieved_callback: AccessCallback = None,
                                 extended_methods: dict[str, str] = None):
    """Return from read_all dict with "items" and "total" """
    result = await exec_access(inc=inc, model=model, transport=transport,
                               fetch_fields=fetch_fields,
                               fetch_fields_on_read=fetch_fields_on_read,
                               fetch_fields_on_read_all=fetch_fields_on_read_all,
                               drop_cols=drop_cols,
                               select_values=select_values,
                               select_values_on_read=select_values_on_read,
                               select_values_on_read_all=select_values_on_read_all,
                               select_values_rename=select_values_rename,
                               select_values_on_read_rename=select_values_on_read_rename,
                               select_values_on_read_all_rename=select_values_on_read_all_rename,
                               full_info=full_info,
                               middleware=middleware,
                               external_callback=external_callback,
                               retrieved_callback=retrieved_callback,
                               extended_methods=extended_methods)
    if inc.request.method == "GET" and isinstance(result, tuple):
        return {"items": result[0], "total": result[1]}
    return result
