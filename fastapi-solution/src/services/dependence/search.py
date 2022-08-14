from abc import ABC


class AsyncSearchStorage(ABC):
    async def search(self, **kwargs):
        ...

    async def get(self, id, **kwargs):
        ...
