import fastapi
import flask
import httpx
import asyncio
import functions_framework
import functools
from fastapi.types import DecoratedCallable
from typing import Any, Callable, List, Optional, Sequence


app = fastapi.FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
is_entry_point_mounted = False
async_client = httpx.AsyncClient(app=app, base_url='http://server')


def stream_response(response: httpx.Response, chunk_size: Optional[int] = None):
    chunk_size = chunk_size or 8192
    async_iterator = response.aiter_bytes(chunk_size=chunk_size)

    while True:
        try:
            yield asyncio.run(async_iterator.__anext__())
        except StopAsyncIteration:
            break


def convert_flask_request_to_httpx_request(request: flask.Request) -> httpx.Request:
    """
    Convert a Flask HTTP request to an HTTPX request.

    Args:
        request (flask.Request): The incoming Flask HTTP request.

    Returns:
        httpx.Request: An HTTPX request.
    """

    method = request.method
    url = request.url
    form_data = request.form.to_dict(flat=False) if len(request.form) > 0 else None
    headers = {key.lower(): value for key, value in request.headers}
    data = request.data
    params = request.args.to_dict(flat=False)
    cookies = {key: value for key, value in request.cookies.items()}

    files = []
    for file_name, file_stream in request.files.items(multi=True):
        file_headers = {key: value for key, value in file_stream.headers.items()}
        files.append((file_name, (file_stream.filename, file_stream.stream, file_stream.mimetype, file_headers)))

    has_files = len(files) > 0

    if form_data:
        data = form_data

    if len(data) == 0:
        data = None

    if not has_files:
        files = None

    if "content-length" in headers:
        del headers["content-length"]

    httpx_request = httpx.Request(
        method=method,
        url=url,
        headers=headers,
        data=data,
        params=params,
        cookies=cookies,
        files=files,
    )

    # Ensure that the request is encoded as 'application/x-www-form-urlencoded'
    # when form data is present and the 'files' object is falsy,
    # because HTTPX doesn't treat such requests as 'multipart/form-data'
    # even if the content type is set beforehand.
    if not has_files and form_data is not None:
        httpx_request.headers['content-type'] = 'application/x-www-form-urlencoded'

    return httpx_request


def convert_httpx_response_to_flask_response(response: httpx.Response) -> flask.Response:
    """
    Convert an HTTPX response to a Flask response.

    Args:
        response (httpx.Response): The HTTPX response.

    Returns:
        flask.Response: A Flask response.
    """

    flask_response = flask.Response(
        stream_response(response),
        status=response.status_code,
        content_type=response.headers.get('content-type')
    )

    for header, value in response.headers.items():
        flask_response.headers[header] = value

    for cookie in response.cookies:
        flask_response.set_cookie(
            key=cookie.name,
            value=cookie.value,
            expires=cookie.expires,
            domain=cookie.domain,
            path=cookie.path,
            secure=cookie.secure,
            httponly=cookie.http_only,
            samesite=cookie.same_site
        )

    return flask_response


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
    dependencies: Optional[Sequence[fastapi.Depends]] = None,
    methods: Optional[List[str]] = None,
):
    """
    Mounts the entry point for the FastAPI application.

    This function registers the provided `endpoint` as the entry point for the FastAPI application.

    Args:
        endpoint (Callable[..., Any]): The function to be used as the entry point.
        dependencies (Optional[Sequence[fastapi.Depends]], optional): A list of FastAPI dependencies.
            Defaults to None.
        methods (Optional[List[str]], optional): A list of HTTP methods that this entry point should respond to.
            Defaults to None.

    Raises:
        RuntimeError: If the entry point is already mounted.

    Note:
        This function should typically be called only once to set up the main entry point for the application.

    Example:
        _mount_entry_point(my_endpoint_function, dependencies=[get_token])
    """

    global is_entry_point_mounted

    if is_entry_point_mounted:
        raise RuntimeError('Entry point is already mounted')

    app.add_api_route('/', endpoint, dependencies=dependencies, methods=methods)
    is_entry_point_mounted = True


def create_handler(
    dependencies: Optional[Sequence[fastapi.Depends]] = None,
    methods: Optional[List[str]] = None,
) -> Callable[[DecoratedCallable], DecoratedCallable]:
    """
    Decorator for creating HTTP handlers that can be used as entry points.

    This decorator can be used to create HTTP handlers that will be treated as entry points
    in the Google Cloud Function acting like FastAPI handler.

    Args:
        dependencies (Optional[Sequence[fastapi.Depends]], optional): A list of FastAPI dependencies.
            Defaults to None.
        methods (Optional[List[str]], optional): A list of HTTP methods that this handler should respond to.
            Defaults to None.

    Returns:
        Callable[[DecoratedCallable], DecoratedCallable]: A decorator function that can be applied to a handler function.
    """

    def decorator(func: DecoratedCallable) -> DecoratedCallable:
        mount_entry_point(func, dependencies=dependencies, methods=methods)
        func = functions_framework.http(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return asyncio.run(proxy(flask.request))

        return wrapper

    return decorator


class router:
    """
    Unlock the full potential of Google Cloud Functions with FastAPI and async capabilities using the 'router' class!

    Are you looking to create a single powerful entry point for your Google Cloud Function?
    The 'router' class is designed for just that, providing seamless integration with FastAPI and async code.

    Key Highlights:
    - Easily register a single entry point for your Google Cloud Function.
    - Leverage FastAPI for robust request handling and request validation.
    - Harness the power of async code for responsive and scalable functions.
    - Define your function's input parameters with ease.

    Example Usage:

    ```python
    # Import necessary modules
    import asyncio
    from datetime import date
    from fastgcf import router

    # Simply use a decorator
    @router.get()
    async def main(start_date: date, end_date: date):
        await asyncio.sleep(1)  # Simulate async processing
        return {"start_date": start_date, "end_date": end_date}

    # That's it! Your Google Cloud Function is ready to handle and validate async GET requests seamlessly.
    ```
    """

    def get(
        dependencies: Optional[Sequence[fastapi.Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['GET'])

    def put(
        dependencies: Optional[Sequence[fastapi.Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['PUT'])

    def post(
        dependencies: Optional[Sequence[fastapi.Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['POST'])

    def options(
        dependencies: Optional[Sequence[fastapi.Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['OPTIONS'])

    def head(
        dependencies: Optional[Sequence[fastapi.Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['HEAD'])

    def patch(
        dependencies: Optional[Sequence[fastapi.Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['PATCH'])

    def route(
        dependencies: Optional[Sequence[fastapi.Depends]] = None,
        methods: Optional[List[str]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=methods)
