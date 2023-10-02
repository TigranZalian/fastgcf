from typing import Optional, Sequence, List
from ._proxy import create_handler
from fastapi.params import Depends


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

    @staticmethod
    def get(
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['GET'])

    @staticmethod
    def put(
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['PUT'])

    @staticmethod
    def post(
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['POST'])

    @staticmethod
    def options(
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['OPTIONS'])

    @staticmethod
    def head(
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['HEAD'])

    @staticmethod
    def patch(
        dependencies: Optional[Sequence[Depends]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=['PATCH'])

    @staticmethod
    def route(
        dependencies: Optional[Sequence[Depends]] = None,
        methods: Optional[List[str]] = None,
    ):
        return create_handler(dependencies=dependencies, methods=methods)
