from fastapi import APIRouter, Request
from app.services.retrieval import search_menu
import json

router = APIRouter()

@router.post("/search")
async def kb_search(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}

    print("KB RAW BODY:", json.dumps(body, indent=2, ensure_ascii=False))

    message = body.get("message", {})
    messages = message.get("messages", []) or []
    messages_openai = message.get("messagesOpenAIFormatted", []) or []

    user_query = ""

    # Try standard messages first
    for msg in reversed(messages):
        role = msg.get("role")
        content = msg.get("content")

        if role == "user":
            if isinstance(content, str):
                user_query = content
                break
            elif isinstance(content, list):
                text_parts = []
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_parts.append(part.get("text", ""))
                user_query = " ".join(text_parts).strip()
                if user_query:
                    break

    # Fallback to OpenAI-formatted messages
    if not user_query:
        for msg in reversed(messages_openai):
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

    print("KB SEARCH QUERY:", repr(user_query))

    if not user_query:
        return {"documents": []}

    # Slightly improve recall for short voice queries
    search_query = user_query
    if "pepperoni" in user_query.lower() and "pizza" not in user_query.lower():
        search_query = user_query + " pizza price"

    results = search_menu(search_query, match_count=5)

    print("KB RESULTS COUNT:", len(results))

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