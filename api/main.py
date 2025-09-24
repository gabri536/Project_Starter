from fastapi import FastAPI, Depends
from .models import IdeaRequest, IdeaResponse
from core.llm import LLMClient
from core.parser import parse_llm_json
import json

app = FastAPI(title="Project Starter API")


def get_llm() -> LLMClient:
    return LLMClient()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Server is up. Try /healthz or /docs"}


@app.get("/healthz")
async def healthz() -> dict[str, bool]:
    return {"ok": True}


@app.post("/ideas", response_model=IdeaResponse)
async def ideas(body: IdeaRequest, llm: LLMClient = Depends(get_llm)) -> IdeaResponse:
    schema = IdeaResponse.model_json_schema()
    user = (
        f"HOBBY: {body.hobby}\n"
        f"INTERESTS: {', '.join(body.interests)}\n"
        f"Return exactly 5 ideas.\n"
        f"JSON schema:\n{json.dumps(schema)}"
    )
    content = await llm.json_chat(user)
    return parse_llm_json(content)
