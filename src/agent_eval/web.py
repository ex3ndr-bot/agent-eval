from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from agent_eval.engine import evaluate_request
from agent_eval.models import EvaluationRequest, StoredEvaluation
from agent_eval.storage import EvaluationStore
from agent_eval.types import OutputFormat, StrategyType

TEMPLATES = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def create_app() -> FastAPI:
    app = FastAPI(title="Agent Eval", version="0.1.0")
    store = EvaluationStore()

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request) -> HTMLResponse:
        return TEMPLATES.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "formats": [item.value for item in OutputFormat],
                "strategies": [item.value for item in StrategyType],
                "form": {
                    "candidate": "",
                    "reference": "",
                    "output_format": OutputFormat.TEXT.value,
                    "strategy": StrategyType.RULE_BASED.value,
                },
                "result": None,
            },
        )

    @app.post("/evaluate", response_class=HTMLResponse)
    async def evaluate_form(
        request: Request,
        candidate: str = Form(...),
        reference: str = Form(""),
        output_format: str = Form(OutputFormat.TEXT.value),
        strategy: str = Form(StrategyType.RULE_BASED.value),
    ) -> HTMLResponse:
        evaluation_request = EvaluationRequest(
            candidate=_coerce_form_value(candidate, OutputFormat(output_format)),
            reference=_coerce_form_value(reference, OutputFormat(output_format)) if reference else None,
            output_format=OutputFormat(output_format),
            strategy=StrategyType(strategy),
        )
        result = evaluate_request(evaluation_request)
        store.add(StoredEvaluation(request=evaluation_request, result=result))
        return TEMPLATES.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "formats": [item.value for item in OutputFormat],
                "strategies": [item.value for item in StrategyType],
                "form": {
                    "candidate": candidate,
                    "reference": reference,
                    "output_format": output_format,
                    "strategy": strategy,
                },
                "result": result.model_dump_json(indent=2),
            },
        )

    @app.post("/api/evaluations")
    async def create_evaluation(payload: EvaluationRequest) -> dict[str, object]:
        result = evaluate_request(payload)
        store.add(StoredEvaluation(request=payload, result=result))
        return {"result": result.model_dump()}

    @app.get("/api/evaluations")
    async def list_evaluations() -> dict[str, object]:
        return {"items": [item.model_dump() for item in store.list_items()]}

    return app


def _coerce_form_value(value: str, output_format: OutputFormat) -> str | dict[str, object] | list[object]:
    if output_format == OutputFormat.STRUCTURED:
        return json.loads(value)
    return value
