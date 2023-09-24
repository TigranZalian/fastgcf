import asyncio
import typing
import asyncio
from httpx._models import Request, Response
from httpx._transports.asgi import _ASGIApp
from httpx._transports.base import AsyncBaseTransport
from httpx._types import AsyncByteStream


class ASGIResponseByteStream(AsyncByteStream):
    def __init__(
        self, stream: typing.AsyncGenerator[bytes, None]
    ) -> None:
        self._stream = stream

    def __aiter__(self) -> typing.AsyncIterator[bytes]:
        return self._stream.__aiter__()

    async def aclose(self) -> None:
        await self._stream.aclose()


class ASGITransport(AsyncBaseTransport):
    def __init__(
        self,
        app: _ASGIApp,
        raise_app_exceptions: bool = True,
        root_path: str = "",
        client: typing.Tuple[str, int] = ("127.0.0.1", 123),
    ) -> None:
        self.app = app
        self.raise_app_exceptions = raise_app_exceptions
        self.root_path = root_path
        self.client = client

    async def handle_async_request(self, request: Request) -> Response:
        assert isinstance(request.stream, AsyncByteStream)

        # ASGI scope.
        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": request.method,
            "headers": [(k.lower(), v) for (k, v) in request.headers.raw],
            "scheme": request.url.scheme,
            "path": request.url.path,
            "raw_path": request.url.raw_path,
            "query_string": request.url.query,
            "server": (request.url.host, request.url.port),
            "client": self.client,
            "root_path": self.root_path,
        }

        # Request.
        request_body_chunks = request.stream.__aiter__()
        request_complete = False

        # Response.
        status_code = None
        response_headers = None
        sentinel = object()
        body_queue = asyncio.Queue()
        response_started = asyncio.Event()
        response_complete = asyncio.Event()

        # ASGI callables.

        async def receive() -> typing.Dict[str, typing.Any]:
            nonlocal request_complete

            if request_complete:
                await response_complete.wait()
                return {"type": "http.disconnect"}

            try:
                body = await request_body_chunks.__anext__()
            except StopAsyncIteration:
                request_complete = True
                return {"type": "http.request", "body": b"", "more_body": False}
            return {"type": "http.request", "body": body, "more_body": True}

        async def send(message: typing.Dict[str, typing.Any]) -> None:
            nonlocal status_code, response_headers, response_started, response_complete

            if message["type"] == "http.response.start":
                assert not response_started.is_set()
                status_code = message["status"]
                response_headers = message.get("headers", [])
                response_started.set()

            elif message["type"] == "http.response.body":
                assert response_started.is_set()
                assert not response_complete.is_set()
                body = message.get("body", b"")
                more_body = message.get("more_body", False)

                if body and request.method != "HEAD":
                    await body_queue.put(body)

                if not more_body:
                    await body_queue.put(sentinel)
                    response_complete.set()


        async def run_app() -> None:
            try:
                await self.app(scope, receive, send)
            except Exception:  # noqa: PIE-786
                if self.raise_app_exceptions or not response_complete.is_set():
                    raise

        async def body_stream() -> typing.AsyncGenerator[bytes, None]:
            while True:
                body = await body_queue.get()
                if body != sentinel:
                    yield body
                else:
                    return

        asyncio.create_task(run_app())

        await response_started.wait()
        assert status_code is not None
        assert response_headers is not None

        stream = ASGIResponseByteStream(body_stream())

        return Response(status_code, headers=response_headers, stream=stream)
