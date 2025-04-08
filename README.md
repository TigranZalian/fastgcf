# fastgcf

[![PyPI Downloads](https://static.pepy.tech/badge/fastgcf)](https://pypi.org/project/fastgcf)

## Unlock the full potential of Google Cloud Functions with FastAPI and async capabilities

Are you bored with using Flask for your Google Cloud Functions and you are looking for a powerful entry point with request validation and async code? The package is designed for just that, providing seamless integration with FastAPI and async code.

### Key Highlights

- Easily register a single entry point for your Google Cloud Function.
- Leverage FastAPI for robust request handling and request validation.
- Harness the power of async code for responsive and scalable functions.
- Define your function's input parameters with ease.
- Use it just as you would use your FastAPI route function.
- Forget about Flask.

### Example Usage

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

### Installation

You can install `fastgcf` using pip:

```bash
pip install fastgcf
```

### Links

- [FastAPI](https://fastapi.tiangolo.com/): The official FastAPI documentation for in-depth information on FastAPI usage and features.
- [Flask](https://flask.palletsprojects.com/): Flask documentation for reference on Flask web framework.

### Acknowledgments

This package is an experimental attempt to mimic FastAPI behavior within Google Cloud Functions. While it provides key features such as request validation, async support, file uploads, streaming responses, and many more, please be aware of the following:

- **Performance Variability**: The package may not offer the same level of performance as a dedicated ASGI server. Performance, especially when handling large files, may not be optimal due to the nature of the proxy used under the hood to proxy Flask requests to FastAPI app.

- **Experimental Nature**: `fastgcf` should be considered experimental. It was tested in basic use cases, including method and request validation, file uploads, streaming responses, and async support.

- **Limitations**: While `fastgcf` may be a great Flask replacement in context of Google Cloud Functions, be aware that certain FastAPI features or behaviors may vary when used with `fastgcf`. It is recommended to thoroughly test and evaluate your use case to ensure compatibility.

By using `fastgcf`, you can benefit from FastAPI's features in the context of Google Cloud Functions, but it's essential to keep these considerations in mind when designing your functions.

### Contribution

Contributions from the community are welcomed! If you'd like to contribute to `fastgcf`, here are a few ways you can get involved:

- Report Issues: If you encounter any bugs or issues, please [open an issue](https://github.com/TigranZalian/fastgcf/issues) on my GitHub repository.

- Submit Pull Requests: If you have improvements or new features to suggest, feel free to [submit a pull request](https://github.com/TigranZalian/fastgcf/pulls) with your changes.

- Share Feedback: I value feedback on your experience using `fastgcf`. Let me know how I can make it better by opening an issue or starting a discussion.

- Documentation: Help improve the documentation by suggesting edits or additions.

- Spread the Word: If you find `fastgcf` useful, consider sharing it with others in your community or network.

By contributing to `fastgcf`, you can help make it even more powerful and useful for others. I appreciate your support and collaboration!
