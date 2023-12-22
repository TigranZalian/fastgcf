import fastapi
import flask
import httpx
import nest_asyncio

from fastapi.params import Depends
from typing import Any, Callable, List, Optional, Sequence

from ._transport import ASGITransport
from ._converters import convert_flask_request_to_httpx_request, convert_httpx_response_to_flask_response


app = fastapi.FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
is_entry_point_mounted = False
asgi_transport = ASGITransport(app)
async_client = httpx.AsyncClient(transport=asgi_transport, base_url='http://server')


async def proxy(flask_request: flask.Request) -> flask.Response:
    """
    Proxy an incoming Flask request to the current FastAPI application.

    Args:
        flask_request (flask.Request): The incoming Flask request.

    Returns:
        flask.Response: The Flask response from the proxy operation.
    """

    httpx_request = convert_flask_request_to_httpx_request(flask_request)
    httpx_response = await async_client.send(httpx_request, stream=True)
    flask_response = convert_httpx_response_to_flask_response(httpx_response)
    return flask_response


def mount_entry_point(
    endpoint: Callable[..., Any],
    *,
    dependencies: Optional[Sequence[Depends]] = None,
    methods: Optional[List[str]] = None,
):
    """
    Mounts the entry point for the FastAPI application.

    This function registers the provided `endpoint` as the entry point for the FastAPI application.

    Args:
        endpoint (Callable[..., Any]): The function to be used as the entry point.
        dependencies (Optional[Sequence[Depends]], optional): A list of FastAPI dependencies.
            Defaults to None.
        methods (Optional[List[str]], optional): A list of HTTP methods that this entry point should respond to.
            Defaults to None.

    Raises:
        RuntimeError: If the entry point is already mounted.

    Note:
        This function should typically be called only once to set up the main entry point for the application.

    Example:
        mount_entry_point(my_endpoint_function, dependencies=[get_token])
    """

    global is_entry_point_mounted

    if is_entry_point_mounted:
        raise RuntimeError('Entry point is already mounted')

    nest_asyncio.apply()

    app.add_api_route('/', endpoint, dependencies=dependencies, methods=methods)
    is_entry_point_mounted = True
