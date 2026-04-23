from app.db.supabase import supabase
import json


def get_restaurant_by_id(restaurant_id: str):
    result = (
        supabase.table("restaurants")
        .select("*")
        .eq("id", restaurant_id)
        .single()
        .execute()
    )
    return result.data


def get_restaurant_by_slug(slug: str):
    result = (
        supabase.table("restaurants")
        .select("*")
        .eq("slug", slug)
        .single()
        .execute()
    )
    return result.data


def build_restaurant_prompt(restaurant: dict) -> str:
    return f"""
You are the ordering assistant for {restaurant['name']}.

Rules:
- Only answer using the provided knowledge base for this restaurant.
- Never invent menu items or prices.
- Be concise, natural, and friendly.
- Confirm the order before finalizing it.
- Additional instructions:
{restaurant.get('prompt_instructions') or 'None'}
""".strip()


def build_widget_assistant_config(restaurant: dict) -> str:
    assistant_config = {
        "name": restaurant["slug"],
        "model": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "temperature": 0,
            "messages": [
                {
                    "role": "system",
                    "content": build_restaurant_prompt(restaurant)
                }
            ],
            "knowledgeBaseId": restaurant.get("vapi_knowledge_base_id")
        },
        "voice": {
            "provider": restaurant.get("voice_provider") or "vapi",
            "voiceId": restaurant.get("voice_id") or "Elliot"
        },
        "firstMessage": restaurant.get("welcome_message") or f"Hello, welcome to {restaurant['name']}. How can I help you today?"
    }

    return json.dumps(assistant_config)