from abc import ABC


class AsyncCacheStorage(ABC):
    async def get(self, key: str, **kwargs):
        ...

    async def set(self, key: str, value: str, expire: int, **kwargs):
        ...
