import asyncio
from typing import Generator, AsyncGenerator, Iterator, AsyncIterator, Any, TypeVar
from httpx._types import AsyncByteStream, SyncByteStream


T = TypeVar("T")


def sync_iterator_to_sync_generator(sync_iterator: Iterator[T]) -> Generator[T, None, None]:
    for i in sync_iterator:
        yield i


async def async_iterator_to_async_generator(async_iterator: AsyncIterator[T]) -> AsyncGenerator[T, None]:
    async for i in async_iterator:
        yield i


async def sync_iterator_to_async_generator(sync_iterator: Iterator[T]) -> AsyncGenerator[T, None]:
    for i in sync_iterator:
        yield i


def async_iterator_to_sync_generator(async_iterator: AsyncIterator[T]) -> Generator[T, None, None]:
    while True:
        try:
            yield asyncio.run(async_iterator.__anext__())
        except StopAsyncIteration:
            break


class StreamExtensionsBase():
    @classmethod
    def from_sync_iterator(cls, iterator: Iterator[bytes]) -> Any:
        raise NotImplementedError()

    @classmethod
    def from_async_iterator(cls, iterator: AsyncIterator[bytes]) -> Any:
        raise NotImplementedError()


class ExtendedAsyncByteStream(AsyncByteStream, StreamExtensionsBase):
    def __init__(
        self, generator: AsyncGenerator[bytes, None]
    ) -> None:
        self._generator = generator

    def __aiter__(self) -> AsyncIterator[bytes]:
        return self._generator.__aiter__()
    
    async def aclose(self) -> None:
        await self._generator.aclose()
    
    @classmethod
    def from_async_iterator(cls, iterator: AsyncIterator[bytes]) -> "ExtendedAsyncByteStream":
        async_generator = async_iterator_to_async_generator(iterator)
        return cls(async_generator)
    
    @classmethod
    def from_sync_iterator(cls, iterator: Iterator[bytes]) -> "ExtendedAsyncByteStream":
        async_generator = sync_iterator_to_async_generator(iterator)
        return cls(async_generator)


class ExtendedSyncByteStream(SyncByteStream, StreamExtensionsBase):
    def __init__(
        self, generator: Generator[bytes, None, None]
    ) -> None:
        self._generator = generator

    def __iter__(self) -> Iterator[bytes]:
        return self._generator.__iter__()

    def close(self) -> None:
        self._generator.close()
    
    @classmethod
    def from_async_iterator(cls, iterator: AsyncIterator[bytes]) -> "ExtendedSyncByteStream":
        sync_generator = async_iterator_to_sync_generator(iterator)
        return cls(sync_generator)
    
    @classmethod
    def from_sync_iterator(cls, iterator: Iterator[bytes]) -> "ExtendedSyncByteStream":
        sync_generator = sync_iterator_to_sync_generator(iterator)
        return cls(sync_generator)
