from typing import Any

from django.http import JsonResponse


class JsonProblemResponse(JsonResponse):
    def __init__(
        self,
        title: str,
        detail: str,
        status: int = 500,
        error_type: str = "about:blank",
        context_data: dict[str, Any] = None,
        **kwargs,
    ):
        response_data = {"type": error_type, "title": title, "detail": detail, "status": status}
        if context_data:
            response_data.update(context_data)

        super().__init__(data=response_data, status=status, **kwargs)
