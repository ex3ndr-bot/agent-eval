# Agent Eval

Agent Eval is an MVP Python package for heuristic evaluation of agent outputs. It provides a typed evaluation engine, a CLI, and a small FastAPI web UI without relying on external LLM APIs.

## Features

- Criteria: accuracy, completeness, consistency, safety
- Strategies: rule-based, rubric-style heuristic judge, statistical
- Confidence scoring from 0-100 with explanations
- Input support for text, code, and structured data
- CLI for quick local evaluations
- FastAPI app with JSON API and simple HTML UI

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python3 -m pytest
agent-eval evaluate --candidate "Paris is the capital of France." --reference "Paris is the capital of France."
agent-eval serve --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` after starting the server.

## CLI examples

```bash
agent-eval evaluate \
  --candidate "Use prepared statements to avoid SQL injection." \
  --reference "Prepared statements help prevent SQL injection attacks." \
  --format text \
  --strategy heuristic
```

```bash
agent-eval evaluate \
  --candidate-file examples/sample_code_candidate.py \
  --reference-file examples/sample_code_reference.py \
  --format code \
  --strategy statistical
```

## API examples

```bash
agent-eval serve
```

```bash
curl -X POST http://127.0.0.1:8000/api/evaluations \
  -H "content-type: application/json" \
  -d @examples/sample_request.json
```

## Project layout

- `src/agent_eval/`: package source
- `tests/`: unit and smoke tests
- `examples/`: sample requests, configs, and inputs

## Notes

- The heuristic judge strategy uses a rubric-style scorer implemented locally.
- The statistical strategy uses overlap and distribution signals only.
- The MVP is intentionally self-contained and does not call external model providers.
