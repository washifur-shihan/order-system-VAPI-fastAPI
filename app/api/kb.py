# from fastapi import APIRouter, Request
# from app.services.retrieval import search_menu
# from app.services.restaurants import get_restaurant_by_slug

# router = APIRouter()


# @router.post("/search")
# async def kb_search(request: Request):
#     try:
#         body = await request.json()
#     except Exception:
#         body = {}

#     print("KB RAW BODY:", body)

#     message = body.get("message", {}) or {}
#     messages = message.get("messages", []) or []
#     restaurant_slug = None

# # 1. Try metadata first
#     metadata = body.get("metadata", {}) or message.get("metadata", {}) or {}
#     restaurant_slug = metadata.get("restaurantSlug")

#     # 2. If not found, get from assistant.name
#     if not restaurant_slug:
#         assistant = body.get("assistant", {}) or {}
#         restaurant_slug = assistant.get("name")

#     print("KB restaurantSlug:", restaurant_slug)

#     if not restaurant_slug:
#         print("❌ No restaurant slug found!")
#         return {"documents": []}

#     restaurant = get_restaurant_by_slug(restaurant_slug)
#     print("KB restaurant:", restaurant)

#     if not restaurant:
#         return {"documents": []}

#     user_query = ""
#     for msg in reversed(messages):
#         if msg.get("role") == "user":
#             content = msg.get("message", "") or msg.get("content", "")
#             if isinstance(content, str):
#                 user_query = content
#             break

#     print("KB user_query:", user_query)

#     if not user_query:
#         return {"documents": []}

#     results = search_menu(restaurant["id"], user_query, match_count=5)
#     print("KB results:", results)

#     return {
#         "documents": [
#             {
#                 "content": row["content"],
#                 "uuid": str(row["id"]),
#                 "similarity": row.get("similarity", 0.9)
#             }
#             for row in results
#         ]
#     }


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

    # 1. Try metadata first
    restaurant_slug = None
    metadata = body.get("metadata", {}) or {}
    restaurant_slug = metadata.get("restaurantSlug")

    # 2. If not in metadata, get it from assistant.name
    if not restaurant_slug:
        assistant = body.get("assistant", {}) or {}
        restaurant_slug = assistant.get("name")

    print("KB restaurantSlug:", restaurant_slug)

    # 3. Stop if still missing
    if not restaurant_slug:
        print("❌ No restaurant slug found!")
        return {"documents": []}

    restaurant = get_restaurant_by_slug(restaurant_slug)
    print("KB restaurant:", restaurant)

    if not restaurant:
        print("❌ Restaurant not found in database!")
        return {"documents": []}

    # 4. Extract latest user query
    user_query = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            content = msg.get("message", "") or msg.get("content", "")
            if isinstance(content, str):
                user_query = content.strip()
            break

    print("KB user_query:", user_query)

    if not user_query:
        print("❌ No user query found!")
        return {"documents": []}

    # 5. Optional normalization for voice queries
    normalized_query = user_query.lower()

    if "pepperoni" in normalized_query and "pizza" not in normalized_query:
        normalized_query += " pizza"

    if "classic" in normalized_query and "burger" not in normalized_query:
        normalized_query += " burger"

    if "smash" in normalized_query and "burger" not in normalized_query:
        normalized_query += " burger"

    if "price" not in normalized_query and "cost" not in normalized_query:
        normalized_query += " price"

    print("KB normalized_query:", normalized_query)

    # 6. Search only this restaurant's menu
    results = search_menu(restaurant["id"], normalized_query, match_count=5)
    print("KB results count:", len(results))
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