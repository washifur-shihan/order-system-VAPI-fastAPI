from fastapi import APIRouter, Request
from app.services.retrieval import search_menu

router = APIRouter()

@router.post("/search")
async def kb_search(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}

    message = body.get("message", {})
    messages = message.get("messages", [])

    user_query = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            user_query = msg.get("content", "")
            break

    print("KB REQUEST BODY:", body)
    print("KB SEARCH QUERY:", user_query)

    if not user_query:
        return {"documents": []}

    results = search_menu(user_query, match_count=5)

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