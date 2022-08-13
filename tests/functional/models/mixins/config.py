import orjson


def orjson_dumps(value, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(value, default=default).decode()


class ConfigMixin:
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
