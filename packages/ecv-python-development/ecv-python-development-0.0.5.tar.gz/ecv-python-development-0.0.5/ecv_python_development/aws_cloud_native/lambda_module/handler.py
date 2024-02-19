from __future__ import annotations

import os

from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from typing_extensions import Any, Callable

from .logger import logger
from .metrics import metrics
from .tracer import tracer

app = APIGatewayRestResolver(debug=(os.environ.get("ENVIRONMENT") != "prod"))


class ProcessHandler:
    handler: Callable[..., dict[Any, Any]]


@app.route(".+", method=["GET", "POST", "PUT", "PATCH", "DELETE"])
@tracer.capture_method
def process() -> dict[Any, Any]:
    return ProcessHandler.handler()


@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST,
    log_event=True,
    clear_state=True,
)
@tracer.capture_lambda_handler  # type: ignore
@metrics.log_metrics(raise_on_empty_metrics=False)  # type: ignore
def start_handler(event: dict[Any, Any], context: LambdaContext) -> dict[str, Any]:
    res = app.resolve(event, context)  # type: ignore
    return res


def spawn_handler(
    event: dict[Any, Any],
    context: LambdaContext,
    handler: Callable[..., dict[Any, Any]],
) -> dict[str, Any]:
    ProcessHandler.handler = handler
    return start_handler(event, context)  # type: ignore
