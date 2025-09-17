from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_ideas_ok() -> None:
    payload = {"hobby": "photography", "interests": ["nature", "coding"]}
    r = client.post("/ideas", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "ideas" in data and len(data["ideas"]) == 5
    first = data["ideas"][0]
    assert {
        "title",
        "why_it_matches",
        "steps",
        "estimated_time_hours",
        "difficulty",
        "starter_resources",
    } <= set(first)


def test_ideas_validation() -> None:
    r = client.post("/ideas", json={"hobby": "a", "interests": []})
    assert r.status_code == 422
