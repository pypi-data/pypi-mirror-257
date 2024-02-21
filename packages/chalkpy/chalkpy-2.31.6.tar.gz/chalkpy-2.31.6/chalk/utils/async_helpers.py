from __future__ import annotations

import asyncio
import contextlib
from concurrent.futures import ThreadPoolExecutor
from typing import AsyncIterable, AsyncIterator, Iterable, TypeVar

T = TypeVar("T")


@contextlib.asynccontextmanager
async def async_null_context(obj: T) -> AsyncIterator[T]:
    yield obj


async def async_enumerate(iterable: AsyncIterator[T] | AsyncIterable[T]):
    i = 0
    async for x in iterable:
        yield i, x
        i += 1


def _yield_to_queue(q: asyncio.Queue[T | ellipsis], loop: asyncio.AbstractEventLoop, it: Iterable[T]):
    try:
        for x in it:
            # This should be fast b/c the queue is unbounded
            asyncio.run_coroutine_threadsafe(q.put(x), loop).result()
    finally:
        asyncio.run_coroutine_threadsafe(q.put(...), loop).result()


async def to_async_iterable(iterable: Iterable[T], executor: ThreadPoolExecutor | None = None) -> AsyncIterable[T]:
    """Runs a blocking iterator in an executor, and yields batches asynchronously as they become available."""
    q: asyncio.Queue[T | ellipsis] = asyncio.Queue()
    task = asyncio.get_running_loop().run_in_executor(
        executor, _yield_to_queue, q, asyncio.get_running_loop(), iterable
    )

    try:
        while True:
            item = await q.get()
            if item is ...:
                break
            yield item
    finally:
        # Should be a no-op
        await task
