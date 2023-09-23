from typing import AsyncIterator, TypeVar, IO
from httpx import AsyncByteStream


T = TypeVar("T")


class AsyncStream(AsyncByteStream):
    def __init__(self, io_stream: IO[T]) -> None:
        self._io_stream = io_stream

    def __aiter__(self) -> AsyncIterator[bytes]:
        for chunk in self._io_stream:
            yield chunk

    async def aclose(self) -> None:
        self._io_stream.close()
