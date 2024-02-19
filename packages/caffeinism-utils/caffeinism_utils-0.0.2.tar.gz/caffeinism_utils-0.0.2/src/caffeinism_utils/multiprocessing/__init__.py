import asyncio
from multiprocessing.connection import Connection

from caffeinism_utils.asyncio import run_in_threadpool


class AsyncPipe:
    def __init__(self, pipe: Connection):
        self.pipe = pipe
        self.lock = asyncio.Lock()

    async def send(self, data):
        async with self.lock:
            return await run_in_threadpool(self.pipe.send, data)

    async def recv(self):
        return await run_in_threadpool(self.pipe.recv)
