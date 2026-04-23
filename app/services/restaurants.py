from app.db.supabase import supabase


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