from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Any
from app.services.retrieval import search_menu
from app.services.restaurants import get_restaurant_by_slug

router = APIRouter()


class KBMessageItem(BaseModel):
    role: str
    content: Any


class KBMessage(BaseModel):
    messages: List[KBMessageItem]
    metadata: Optional[dict] = None


class KBSearchRequest(BaseModel):
    message: KBMessage
    metadata: Optional[dict] = None


@router.post("/search")
async def kb_search(payload: KBSearchRequest):
    metadata = payload.metadata or payload.message.metadata or {}
    restaurant_slug = metadata.get("restaurantSlug")

    print("KB SEARCH restaurantSlug:", restaurant_slug)
    print("KB SEARCH payload:", payload.model_dump())

    if not restaurant_slug:
        return {"documents": []}

    restaurant = get_restaurant_by_slug(restaurant_slug)
    if not restaurant:
        return {"documents": []}

    user_query = ""
    for msg in reversed(payload.message.messages):
        if msg.role == "user":
            if isinstance(msg.content, str):
                user_query = msg.content
            break

    if not user_query:
        return {"documents": []}

    results = search_menu(restaurant["id"], user_query, match_count=5)

    return {
        "documents": [
            {
                "content": row["content"],
                "uuid": str(row["id"]),
                "similarity": row.get("similarity", 0.9)
            }
            for row in results
        ]
    }