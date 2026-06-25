from typing import Any

from django.http import HttpResponseForbidden, JsonResponse


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


def validate_report_ownership(report, device_id):
    """
    Validate that a report belongs to the specified device.

    Args:
        report: The Report object to validate
        device_id: The device ID to check against

    Returns:
        HttpResponseForbidden if validation fails, None otherwise
    """
    if report.client != device_id:
        return HttpResponseForbidden("Device_id mismatch")
    return None
