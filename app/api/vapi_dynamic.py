from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.restaurants import get_restaurant_by_slug, build_restaurant_prompt

router = APIRouter()


class AssistantSelectorMessage(BaseModel):
    metadata: Optional[dict] = None


class AssistantSelectorRequest(BaseModel):
    metadata: Optional[dict] = None
    message: Optional[AssistantSelectorMessage] = None


@router.post("/assistant-selector")
async def assistant_selector(payload: AssistantSelectorRequest):
    print("ASSISTANT SELECTOR HIT:", payload.model_dump())
    metadata = payload.metadata or {}
    if payload.message and payload.message.metadata:
        metadata = {**payload.message.metadata, **metadata}

    restaurant_slug = metadata.get("restaurantSlug")

    if not restaurant_slug:
        return {"error": "Missing restaurantSlug"}

    restaurant = get_restaurant_by_slug(restaurant_slug)
    if not restaurant:
        return {"error": "Restaurant not found"}

    prompt = build_restaurant_prompt(restaurant)

    return {
        "assistant": {
            "name": f"{restaurant['name']} Assistant",
            "model": {
                "provider": "openai",
                "model": "gpt-4.1",
                "messages": [
                    {
                        "role": "system",
                        "content": prompt
                    }
                ]
            },
            "voice": {
                "provider": restaurant.get("voice_provider", "vapi"),
                "voiceId": restaurant.get("voice_id", "Elliot")
            },
            "firstMessage": restaurant.get("welcome_message") or f"Hello, welcome to {restaurant['name']}. How can I help you today?"
        }
    }