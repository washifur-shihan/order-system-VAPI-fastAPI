from openai import OpenAI

from app.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def _format_recent_messages(recent_messages: list[dict]) -> str:
    if not recent_messages:
        return "No recent messages."

    lines = []
    for message in recent_messages:
        role = message.get("role", "unknown")
        content = message.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def _format_menu_context(menu_context: list[dict]) -> str:
    if not menu_context:
        return "No matching menu items found."

    chunks = []
    for item in menu_context:
        title = item.get("title") or item.get("name") or "Menu item"
        content = item.get("content") or item.get("text") or ""
        chunks.append(f"{title}: {content}".strip())
    return "\n".join(chunks)


def generate_answer(
    user_message: str,
    recent_messages: list[dict],
    menu_context: list[dict],
    customer: dict,
    conversation: dict,
) -> str:
    system_prompt = (
        "You are a helpful restaurant ordering assistant. "
        "Answer clearly and briefly. "
        "Use the provided menu context when it is relevant, and do not invent menu items."
    )

    user_prompt = (
        f"Customer: {customer}\n"
        f"Conversation: {conversation}\n\n"
        f"Recent messages:\n{_format_recent_messages(recent_messages)}\n\n"
        f"Menu context:\n{_format_menu_context(menu_context)}\n\n"
        f"User message: {user_message}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )

    return response.choices[0].message.content or ""
