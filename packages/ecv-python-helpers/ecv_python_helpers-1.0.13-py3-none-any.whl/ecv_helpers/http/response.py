from __future__ import annotations

import json
from typing import Any

from aws_lambda_powertools.event_handler import Response, content_types


class CustomException(Exception):
    def __init__(
        self,
        custom_status_code: int | None = None,
        custom_error_code: str | None = None,
        custom_error_message: str | None = None,
        custom_error_details: str | None = None,
    ) -> None:
        if custom_status_code:
            self.STATUS_CODE = custom_status_code
        if custom_error_code:
            self.ERROR_CODE = custom_error_code
        if custom_error_message:
            self.ERROR_MESSAGE = custom_error_message
        if custom_error_details:
            self.ERROR_DETAILS = custom_error_details
        super().__init__(self.ERROR_MESSAGE)


def cors_response(code: int, body: Any) -> Response:
    return Response(
        status_code=code,
        content_type=content_types.APPLICATION_JSON,
        headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Header": "*",
        },
        body=body,
    )


def ErrorResponse(error: CustomException) -> Response:
    err = {
        "code": error.ERROR_CODE,
        "message": error.ERROR_MESSAGE,
    }

    if hasattr(error, "ERROR_DETAILS"):
        err["error_details"] = error.ERROR_DETAILS

    return cors_response(
        code=error.STATUS_CODE,
        body=json.dumps({"error": err}),
    )


def SuccessResponse(
    data: Any, status_code: int = 200, **other_data: dict[Any, Any]
) -> Response:
    response = {
        "status": "success",
        "status_code": status_code,
        "data": data,
        **other_data,
    }

    return cors_response(
        code=200,
        body=json.dumps(response),
    )
