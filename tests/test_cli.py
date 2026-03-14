from click.testing import CliRunner

from agent_eval.cli import main


def test_cli_evaluate_smoke() -> None:
    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            "evaluate",
            "--candidate",
            "Prepared statements prevent SQL injection.",
            "--reference",
            "Prepared statements help prevent SQL injection.",
            "--format",
            "text",
            "--strategy",
            "heuristic",
        ],
    )

    assert result.exit_code == 0
    assert '"overall_score"' in result.output


def test_cli_structured_input_from_inline_json() -> None:
    runner = CliRunner()

    result = runner.invoke(
        main,
        [
            "evaluate",
            "--candidate",
            '{"status":"ok","value":1}',
            "--reference",
            '{"status":"ok","value":1}',
            "--format",
            "structured",
            "--strategy",
            "statistical",
            "--compact",
        ],
    )

    assert result.exit_code == 0
    assert '"confidence"' in result.output
