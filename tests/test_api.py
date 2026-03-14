from fastapi.testclient import TestClient

from agent_eval.web import create_app


def test_api_evaluation_smoke() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/evaluations",
        json={
            "candidate": "Use parameterized queries.",
            "reference": "Parameterized queries improve SQL safety.",
            "output_format": "text",
            "strategy": "rule_based",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["result"]["overall_score"] >= 0


def test_html_index_smoke() -> None:
    client = TestClient(create_app())

    response = client.get("/")

    assert response.status_code == 200
    assert "Agent Eval" in response.text
