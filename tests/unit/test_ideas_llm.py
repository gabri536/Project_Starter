from fastapi.testclient import TestClient
from api.main import app, get_llm


# A tiny async fake that returns valid JSON matching IdeasResponse
class FakeLLM:
    async def json_chat(self, user: str) -> str:
        return """
        {
          "ideas": [
            {
              "title": "Starter Project 1",
              "why_it_matches": "Matches your interests and is beginner-friendly.",
              "steps": ["Do A", "Do B", "Do C"],
              "estimated_time_hours": 2.0,
              "difficulty": "easy",
              "starter_resources": []
            },
            {
              "title": "Starter Project 2",
              "why_it_matches": "Matches your interests and is beginner-friendly.",
              "steps": ["Do A", "Do B", "Do C"],
              "estimated_time_hours": 2.0,
              "difficulty": "easy",
              "starter_resources": []
            },
            {
              "title": "Starter Project 3",
              "why_it_matches": "Matches your interests and is beginner-friendly.",
              "steps": ["Do A", "Do B", "Do C"],
              "estimated_time_hours": 2.0,
              "difficulty": "easy",
              "starter_resources": []
            },
            {
              "title": "Starter Project 4",
              "why_it_matches": "Matches your interests and is beginner-friendly.",
              "steps": ["Do A", "Do B", "Do C"],
              "estimated_time_hours": 2.0,
              "difficulty": "easy",
              "starter_resources": []
            },
            {
              "title": "Starter Project 5",
              "why_it_matches": "Matches your interests and is beginner-friendly.",
              "steps": ["Do A", "Do B", "Do C"],
              "estimated_time_hours": 2.0,
              "difficulty": "easy",
              "starter_resources": []
            }
          ]
        }
        """


class FencedLLM:
    async def json_chat(self, user: str) -> str:
        return '```json\n{"ideas":[{"title":"X","why_it_matches":"ok ok ok ok ok","steps":["1","2","3"],"estimated_time_hours":1.5,"difficulty":"easy","starter_resources":[]},{"title":"Y","why_it_matches":"ok ok ok ok ok","steps":["1","2","3"],"estimated_time_hours":1.5,"difficulty":"easy","starter_resources":[]},{"title":"Z","why_it_matches":"ok ok ok ok ok","steps":["1","2","3"],"estimated_time_hours":1.5,"difficulty":"easy","starter_resources":[]},{"title":"W","why_it_matches":"ok ok ok ok ok","steps":["1","2","3"],"estimated_time_hours":1.5,"difficulty":"easy","starter_resources":[]},{"title":"Q","why_it_matches":"ok ok ok ok ok","steps":["1","2","3"],"estimated_time_hours":1.5,"difficulty":"easy","starter_resources":[]}]} \n```'


def test_ideas_llm_ok() -> None:
    app.dependency_overrides[get_llm] = lambda: FakeLLM()
    client = TestClient(app)

    payload = {"hobby": "photography", "interests": ["nature", "coding"]}
    r = client.post("/ideas", json=payload)

    app.dependency_overrides.clear()

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


def test_ideas_llm_repairs_fenced_json() -> None:

    app.dependency_overrides[get_llm] = lambda: FencedLLM()
    client = TestClient(app)
    r = client.post("/ideas", json={"hobby": "x", "interests": ["y"]})
    app.dependency_overrides.clear()

    assert r.status_code == 200
    assert len(r.json()["ideas"]) == 5
