import asyncio
from functools import partial


def run_in_threadpool(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    f = partial(func, *args, **kwargs)
    return loop.run_in_executor(None, f)

