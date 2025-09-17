from typing import Literal
from pydantic import BaseModel, Field, HttpUrl

Difficulty = Literal["easy", "medium", "hard"]


class Resource(BaseModel):
    name: str
    url: HttpUrl


class Idea(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    why_it_matches: str = Field(min_length=10, max_length=300)
    steps: list[str] = Field(min_length=1, max_length=10)
    estimated_time: float = Field(ge=0.5, le=20)
    difficulty: Difficulty
    starter_resources: list[Resource] = []


class IdeaRequest(BaseModel):
    hobby: str = Field(min_length=3, max_length=50)
    interests: list[str] = Field(max_length=3)


class IdeaResponse(BaseModel):
    ideas: list[Idea] = Field(min_length=5, max_length=5)
