from fastapi import FastAPI
from models import Idea, IdeaRequest, IdeaResponse

app = FastAPI(title="Project Starter API")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Server is up. Try /healthz or /docs"}


@app.get("/healthz")
async def healthz() -> dict[str, bool]:
    return {"ok": True}


@app.post("/ideas", response_model=IdeaResponse)
async def ideas(body: IdeaRequest) -> IdeaResponse:
    base = {
        "why_it_matches": "Matches your interests and is beginner-friendly.",
        "steps": ["Set up tools", "Follow a tutorial", "Build a small example"],
        "estimated_time_hours": 2.0,
        "difficulty": "starter",
        "starter_resources": [],
    }
    ideas = [Idea(title=f"{body.hobby.title()} idea {i+1}", **base) for i in range(5)]
    return IdeaResponse(ideas=ideas)
