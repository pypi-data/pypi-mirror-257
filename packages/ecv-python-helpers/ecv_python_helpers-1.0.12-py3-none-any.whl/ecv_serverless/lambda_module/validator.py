from __future__ import annotations

import json
from typing import Type

from aws_lambda_powertools.middleware_factory import (
    lambda_handler_decorator,  # type: ignore
)
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, ValidationError
from typing_extensions import Any, Callable

from .exceptions import PydanticBaseModelException, RequestValidationException
from .handler import app
from .logger import log


@lambda_handler_decorator
def validate_function_source(
    handler: Callable[..., dict[Any, Any]],
    event: dict[Any, Any],
    context: LambdaContext,
) -> dict[Any, Any]:
    if _skip_warmup_call(event):
        return {}

    response = handler(event, context)
    print(response)  # check if this is necessary
    return response


@lambda_handler_decorator
def validate_web_request(
    handler: Callable[..., dict[Any, Any]],
    event: dict[Any, Any],
    context: LambdaContext,
    model: Type[BaseModel],
) -> Callable[..., dict[Any, Any]] | dict[Any, Any]:
    if _skip_warmup_call(event):
        return {}

    if not isinstance(model, BaseModel):
        raise PydanticBaseModelException

    body: dict[Any, Any] = {}
    if event["body"]:
        body = json.loads(event["body"])
    if event["queryStringParameters"]:
        body = {**body, **event["queryStringParameters"]}
    if event["pathParameters"]:
        body = {**body, **event["pathParameters"]}

    log("UNVALIDATED_BODY", data=body)
    result = _validate_data(body, model_class=model)

    if not isinstance(result, BaseModel):
        return {
            "body": json.dumps(
                {
                    "error": {
                        "code": RequestValidationException.ERROR_CODE,
                        "message": RequestValidationException.ERROR_MESSAGE,
                        "error_details": _construct_validation_error_message(result),
                    }
                },
                default=str,
            ),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Header": "*",
            },
            "status_code": RequestValidationException.STATUS_CODE,
        }

    setattr(app, "validated_body", result.dict())
    response = handler(event, context)
    print(response)  # check if this is necessary

    return response


def _skip_warmup_call(event: dict[Any, Any]) -> bool:
    skip = False
    if event.get("source") == "serverless-plugin-warmup":
        log("LAMBDA_WARMER_INVOCATION")
        skip = True

    return skip


def _validate_data(
    data: dict[str, Any], model_class: Type[BaseModel]
) -> BaseModel | dict[Any, Any]:
    try:
        validated_data = model_class(**data)
        return validated_data
    except ValidationError as e:
        errors: dict[Any, Any] = {}
        for error in e.errors():
            errors[error["loc"][0]] = error["msg"]
        return errors


def _construct_validation_error_message(
    validated_data: dict[Any, Any]
) -> list[dict[str, Any]]:
    error_message_list: list[dict[Any, Any]] = []
    for field, error in validated_data.items():
        temp_dict: dict[Any, Any] = {}
        temp_dict["field"] = field
        temp_dict["error"] = error
        error_message_list.append(temp_dict)

    return error_message_list
