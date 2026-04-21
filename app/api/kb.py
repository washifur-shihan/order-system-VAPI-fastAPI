from fastapi import APIRouter, Request
from app.services.retrieval import search_menu

router = APIRouter()

@router.post("/search")
async def kb_search(request: Request):
    body = await request.json()
    message = body.get("message", {})
    messages = message.get("messages", [])

    # get latest user message
    user_query = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            user_query = msg.get("content", "")
            break

    print("KB SEARCH QUERY:", user_query)

    if not user_query:
        return {"documents": []}

    results = search_menu(user_query, match_count=5)

    return {
        "documents": [
            {
                "content": row["content"],
                "similarity": row.get("similarity", 0.9),
                "uuid": str(row["id"])
            }
            for row in results
        ]
    }