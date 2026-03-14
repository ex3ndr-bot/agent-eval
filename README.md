# Agent Eval

`agent_eval` is a Python package for evaluating AI agent outputs with a consistent scoring model, a local CLI, and a lightweight FastAPI service.

It is designed for teams that need:

- repeatable evaluation criteria
- explainable scores instead of a single opaque number
- pluggable evaluation strategies
- local tooling for batch workflows and service integration

## Features

- Weighted evaluation criteria for `accuracy`, `completeness`, `consistency`, `safety`, and `relevance`
- Three built-in strategies:
  - `RuleBasedStrategy` for regex and keyword checks
  - `StatisticalStrategy` for length, entropy, and readability signals
  - `LLMJudgeStrategy` as an integration-ready placeholder for model-based judging
- `ConfidenceScorer` that combines strategy outputs into a normalized `0-100` score
- Typed Pydantic models for configs, requests, responses, and criterion-level results
- Click CLI for evaluating files from the terminal
- FastAPI application with `/evaluate`, `/history`, and `/configs` endpoints

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

For development:

```bash
pip install -e .[dev]
pytest
```

## Quick Start

Evaluate a sample output from the CLI:

```bash
agent-eval evaluate \
  --input-file examples/sample_output.txt \
  --config examples/sample_config.json
```

Run the API locally:

```bash
uvicorn agent_eval.web:app --reload
```

Submit an evaluation request:

```bash
curl -X POST http://127.0.0.1:8000/evaluate \
  -H "content-type: application/json" \
  -d '{
    "output": {
      "content": "Paris is the capital of France. It is known for the Eiffel Tower."
    },
    "config": {
      "criteria": {
        "accuracy": {"weight": 0.30, "threshold": 0.70},
        "completeness": {"weight": 0.20, "threshold": 0.60},
        "consistency": {"weight": 0.15, "threshold": 0.65},
        "safety": {"weight": 0.20, "threshold": 0.80},
        "relevance": {"weight": 0.15, "threshold": 0.70}
      },
      "enabled_strategies": ["rule_based", "statistical"]
    }
  }'
```

## Core Concepts

### Evaluation criteria

Each criterion has:

- `weight`: contribution to the final score
- `threshold`: minimum acceptable normalized score for that criterion

The built-in criteria are:

- `accuracy`
- `completeness`
- `consistency`
- `safety`
- `relevance`

### Strategies

`agent_eval` separates signal generation from final scoring.

#### `RuleBasedStrategy`

Uses pattern matching and keyword heuristics to detect signals such as:

- factual-style language
- structure and coverage markers
- contradictions
- unsafe or policy-risky language
- prompt alignment indicators

This is fast and deterministic.

#### `StatisticalStrategy`

Computes simple text-quality signals:

- token and sentence length balance
- character entropy
- lexical diversity
- readability approximation

This is useful when you need model-free scoring with broader text-shape awareness.

#### `LLMJudgeStrategy`

This is a documented placeholder for teams that want to route evaluation through an external model later. It returns a neutral, low-confidence signal by default so the pipeline remains stable until the integration is implemented.

## Python Usage

```python
from agent_eval import AgentOutput, EvaluationConfig, Evaluator

output = AgentOutput(
    content="Prepared statements reduce SQL injection risk by separating code from data."
)

config = EvaluationConfig.default()
result = Evaluator().evaluate(output, config)

print(result.score)
for criterion in result.breakdown:
    print(criterion.criterion, criterion.score, criterion.passed)
```

Custom configuration:

```python
from agent_eval import EvaluationConfig

config = EvaluationConfig.model_validate_json(
    """
    {
      "criteria": {
        "accuracy": {"weight": 0.35, "threshold": 0.75},
        "completeness": {"weight": 0.20, "threshold": 0.60},
        "consistency": {"weight": 0.15, "threshold": 0.65},
        "safety": {"weight": 0.20, "threshold": 0.85},
        "relevance": {"weight": 0.10, "threshold": 0.70}
      },
      "enabled_strategies": ["rule_based", "statistical", "llm_judge"]
    }
    """
)
```

## CLI

The CLI reads plain text input from a file and optionally loads an evaluation config from JSON.

```bash
agent-eval evaluate --input-file path/to/output.txt
```

```bash
agent-eval evaluate \
  --input-file examples/sample_output.txt \
  --config examples/sample_config.json \
  --pretty
```

Options:

- `--input-file`: required path to the agent output text file
- `--config`: optional path to a JSON config file
- `--pretty / --compact`: control output formatting

## API

Start the API:

```bash
uvicorn agent_eval.web:app --host 127.0.0.1 --port 8000
```

### `POST /evaluate`

Request body:

```json
{
  "output": {
    "content": "Summarize the report and highlight the key risk."
  },
  "config": {
    "criteria": {
      "accuracy": {"weight": 0.30, "threshold": 0.70},
      "completeness": {"weight": 0.20, "threshold": 0.60},
      "consistency": {"weight": 0.15, "threshold": 0.65},
      "safety": {"weight": 0.20, "threshold": 0.80},
      "relevance": {"weight": 0.15, "threshold": 0.70}
    },
    "enabled_strategies": ["rule_based", "statistical"]
  }
}
```

Response:

```json
{
  "score": 78.4,
  "status": "pass",
  "breakdown": [
    {
      "criterion": "accuracy",
      "score": 80.1,
      "weight": 0.3,
      "threshold": 0.7,
      "passed": true,
      "explanations": [
        "Rule-based checks found evidence of specific, factual wording.",
        "Statistical checks indicate balanced length and healthy lexical diversity."
      ]
    }
  ],
  "recommendations": [
    "Increase coverage to improve completeness."
  ],
  "strategy_summaries": {
    "rule_based": "Deterministic keyword and pattern checks completed.",
    "statistical": "Text quality and structural signals computed."
  }
}
```

### `GET /history`

Returns evaluations performed since process start.

### `GET /configs`

Returns the default config and a stricter preset.

## Package Layout

```text
src/agent_eval/
  __init__.py
  criteria.py
  evaluator.py
  models.py
  scorer.py
  strategies.py
  cli.py
  web.py
examples/
  sample_config.json
  sample_output.txt
```

## Examples

Sample files are included:

- [`examples/sample_config.json`](examples/sample_config.json)
- [`examples/sample_output.txt`](examples/sample_output.txt)

## Design Notes

- Scores are normalized to `0-100` for operator readability.
- Thresholds are stored as `0-1` values to keep criterion rules explicit.
- Recommendations are generated only for underperforming criteria to keep results actionable.
- The library avoids network calls by default.

## Future Extensions

- plug in provider-backed LLM judges
- add domain-specific evaluation presets
- persist history to a database instead of memory
- support structured and multimodal outputs
