import flask
import httpx
from ._streams import ExtendedSyncByteStream


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

    response_stream = ExtendedSyncByteStream.from_async_iterator(response.aiter_bytes())

    flask_response = flask.Response(
        response_stream,
        status=response.status_code,
        content_type=response.headers.get('content-type')
    )

    for header, value in response.headers.items():
        flask_response.headers[header] = value

    for cookie in response.cookies.jar:
        flask_response.set_cookie(
            key=cookie.name,
            value=cookie.value,
            expires=cookie.expires,
            domain=cookie.domain,
            path=cookie.path,
            secure=cookie.secure
        )

    return flask_response
