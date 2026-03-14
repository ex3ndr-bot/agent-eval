from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import click
import uvicorn

from agent_eval.engine import evaluate_request
from agent_eval.models import EvaluationRequest
from agent_eval.types import OutputFormat, StrategyType
from agent_eval.web import create_app


def _read_input(raw: str | None, file_path: str | None, output_format: OutputFormat) -> str | dict[str, Any] | list[Any]:
    if raw is not None:
        return _parse_value(raw, output_format)
    if file_path is None:
        raise click.ClickException("one of --candidate/--candidate-file or --reference/--reference-file is required")
    return _parse_value(Path(file_path).read_text(encoding="utf-8"), output_format)


def _parse_value(raw: str, output_format: OutputFormat) -> str | dict[str, Any] | list[Any]:
    if output_format == OutputFormat.STRUCTURED:
        return json.loads(raw)
    return raw


@click.group()
def main() -> None:
    """Agent Eval CLI."""


@main.command("evaluate")
@click.option("--candidate", type=str)
@click.option("--candidate-file", type=click.Path(exists=True, dir_okay=False, path_type=str))
@click.option("--reference", type=str)
@click.option("--reference-file", type=click.Path(exists=True, dir_okay=False, path_type=str))
@click.option("--format", "output_format", type=click.Choice([item.value for item in OutputFormat]), default=OutputFormat.TEXT.value, show_default=True)
@click.option("--strategy", type=click.Choice([item.value for item in StrategyType]), default=StrategyType.RULE_BASED.value, show_default=True)
@click.option("--pretty/--compact", default=True, show_default=True)
def evaluate(
    candidate: str | None,
    candidate_file: str | None,
    reference: str | None,
    reference_file: str | None,
    output_format: str,
    strategy: str,
    pretty: bool,
) -> None:
    """Evaluate a candidate output."""
    format_enum = OutputFormat(output_format)
    request = EvaluationRequest(
        candidate=_read_input(candidate, candidate_file, format_enum),
        reference=_read_input(reference, reference_file, format_enum) if (reference is not None or reference_file is not None) else None,
        output_format=format_enum,
        strategy=StrategyType(strategy),
    )
    result = evaluate_request(request)
    click.echo(result.model_dump_json(indent=2 if pretty else None))


@main.command("serve")
@click.option("--host", default="127.0.0.1", show_default=True)
@click.option("--port", default=8000, type=int, show_default=True)
def serve(host: str, port: int) -> None:
    """Run the FastAPI app."""
    uvicorn.run(create_app(), host=host, port=port)
