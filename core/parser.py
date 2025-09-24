from pydantic import ValidationError
from api.models import IdeaResponse


def parse_llm_json(text: str) -> IdeaResponse:
    try:
        parsed: IdeaResponse = IdeaResponse.model_validate_json(text)
        return parsed

    except ValidationError:
        if "```" in text:
            text = text.split("```")[-1].strip()
        parsed_repaired: IdeaResponse = IdeaResponse.model_validate_json(text)
        return parsed_repaired
