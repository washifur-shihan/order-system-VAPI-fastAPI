from fastapi import APIRouter, Request
from app.services.retrieval import search_menu
from app.services.restaurants import get_restaurant_by_slug

router = APIRouter()


@router.post("/search")
async def kb_search(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}

    print("KB RAW BODY:", body)

    message = body.get("message", {}) or {}
    messages = message.get("messages", []) or []
    metadata = body.get("metadata", {}) or message.get("metadata", {}) or {}

    restaurant_slug = metadata.get("restaurantSlug")
    print("KB restaurantSlug:", restaurant_slug)

    if not restaurant_slug:
        return {"documents": []}

    restaurant = get_restaurant_by_slug(restaurant_slug)
    print("KB restaurant:", restaurant)

    if not restaurant:
        return {"documents": []}

    user_query = ""

    for msg in reversed(messages):
        if msg.get("role") == "user":
            content = msg.get("content", "")

            if isinstance(content, str):
                user_query = content
            elif isinstance(content, list):
                text_parts = []
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_parts.append(part.get("text", ""))
                user_query = " ".join(text_parts).strip()

            break

    print("KB user_query:", user_query)

    if not user_query:
        return {"documents": []}

    results = search_menu(restaurant["id"], user_query, match_count=5)
    print("KB results:", results)

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