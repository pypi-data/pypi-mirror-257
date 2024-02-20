import asyncio
import functools
from abc import ABC, abstractmethod
from functools import partial

from pydantic import BaseModel, validate_call


def cannot_call(*args, **kwargs):
    raise Exception("You cannot call this method directly")


def run_in_threadpool(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    f = partial(func, *args, **kwargs)
    return loop.run_in_executor(None, f)


class Call(BaseModel):
    path: str
    args: tuple
    kwargs: dict


class Emitter(ABC):
    def __init__(self):
        self.methods = {}

    def callback(self, path):
        def decorator(func):
            self.methods[path] = validate_call(func)
            return functools.wraps(func)(cannot_call)

        return decorator

    async def _process_data(self, data: Call):
        func = self.methods[data.path]
        await (
            func(*data.args, **data.kwargs)
            if asyncio.iscoroutinefunction(func.raw_function)
            else run_in_threadpool(func, *data.args, **data.kwargs)
        )

    async def listen(self):
        while data := await self.recv():
            await self._process_data(data)

    @abstractmethod
    async def send(self, path, *args, **kwargs):
        """call remote procedure"""

    @abstractmethod
    async def recv(self):
        """recv remote procedure"""
