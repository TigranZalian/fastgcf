from typing import List, Optional, Sequence, Callable, overload
from fastapi.params import Depends
from fastapi.types import DecoratedCallable

import functools
import functions_framework
import asyncio
import flask

from ._proxy import mount_entry_point, proxy


@overload
def handler(__fn: DecoratedCallable) -> DecoratedCallable:
    ...


@overload
def handler(
    *,
    dependencies: Optional[Sequence[Depends]] = None,
    methods: Optional[List[str]] = None,
) -> Callable[[DecoratedCallable], DecoratedCallable]:
    ...


def handler(
    __fn: Optional[DecoratedCallable] = None,
    *,
    dependencies: Optional[Sequence[Depends]] = None,
    methods: Optional[List[str]] = None,
):
    """
    Decorator for creating HTTP handlers that can be used as entry points.

    This decorator can be used to create HTTP handlers that will be treated as entry points
    in the Google Cloud Function acting like FastAPI handler.

    Args:
        dependencies (Optional[Sequence[Depends]], optional): A list of FastAPI dependencies.
            Defaults to None.
        methods (Optional[List[str]], optional): A list of HTTP methods that this handler should respond to.
            Defaults to None.

    Returns:
        Callable[[DecoratedCallable], DecoratedCallable]] | DecoratedCallable: A decorator function that can be applied to a handler function.
    """

    def decorator(func: DecoratedCallable) -> DecoratedCallable:
        mount_entry_point(func, dependencies=dependencies, methods=methods)
        func = functions_framework.http(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return asyncio.run(proxy(flask.request))

        return wrapper

    return decorator(__fn) if __fn else decorator
