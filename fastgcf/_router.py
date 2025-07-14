from typing import ClassVar, Callable, Optional, Sequence, List, overload
from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.types import DecoratedCallable
from ._handler import handler
from ._proxy import app as _fastapi_app


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
    @router.get
    async def main(start_date: date, end_date: date):
        await asyncio.sleep(1)  # Simulate async processing
        return {"start_date": start_date, "end_date": end_date}

    # That's it! Your Google Cloud Function is ready to handle and validate async GET requests seamlessly.
    ```
    """

    fastapi: ClassVar[FastAPI] = _fastapi_app


    @staticmethod
    @overload
    def get(__fn: DecoratedCallable) -> DecoratedCallable:
        ...

    @staticmethod
    @overload
    def get(
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        ...

    @staticmethod
    def get(
        __fn: Optional[DecoratedCallable] = None,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return handler(__fn, dependencies=dependencies, methods=['GET'])


    @staticmethod
    @overload
    def put(__fn: DecoratedCallable) -> DecoratedCallable:
        ...

    @staticmethod
    @overload
    def put(
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        ...

    @staticmethod
    def put(
        __fn: Optional[DecoratedCallable] = None,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return handler(__fn, dependencies=dependencies, methods=['PUT'])
    

    @staticmethod
    @overload
    def post(__fn: DecoratedCallable) -> DecoratedCallable:
        ...

    @staticmethod
    @overload
    def post(
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        ...

    @staticmethod
    def post(
        __fn: Optional[DecoratedCallable] = None,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return handler(__fn, dependencies=dependencies, methods=['POST'])


    @staticmethod
    @overload
    def options(__fn: DecoratedCallable) -> DecoratedCallable:
        ...

    @staticmethod
    @overload
    def options(
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        ...

    @staticmethod
    def options(
        __fn: Optional[DecoratedCallable] = None,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return handler(__fn, dependencies=dependencies, methods=['OPTIONS'])
    

    @staticmethod
    @overload
    def head(__fn: DecoratedCallable) -> DecoratedCallable:
        ...

    @staticmethod
    @overload
    def head(
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        ...

    @staticmethod
    def head(
        __fn: Optional[DecoratedCallable] = None,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return handler(__fn, dependencies=dependencies, methods=['HEAD'])


    @staticmethod
    @overload
    def patch(__fn: DecoratedCallable) -> DecoratedCallable:
        ...

    @staticmethod
    @overload
    def patch(
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        ...

    @staticmethod
    def patch(
        __fn: Optional[DecoratedCallable] = None,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return handler(__fn, dependencies=dependencies, methods=['PATCH'])


    @staticmethod
    @overload
    def route(__fn: DecoratedCallable) -> DecoratedCallable:
        ...

    @staticmethod
    @overload
    def route(
        *,
        dependencies: Optional[Sequence[Depends]] = None,
        methods: Optional[List[str]] = None,
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        ...

    @staticmethod
    def route(
        __fn: Optional[DecoratedCallable] = None,
        *,
        dependencies: Optional[Sequence[Depends]] = None,
        methods: Optional[List[str]] = None,
    ):
        return handler(__fn, dependencies=dependencies, methods=methods)
