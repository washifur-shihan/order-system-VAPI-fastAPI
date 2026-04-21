from fastapi import APIRouter
from pydantic import BaseModel
from app.services.memory import get_or_create_customer_and_conversation, save_message
from app.services.retrieval import search_menu, get_recent_messages
from app.services.orders import maybe_extract_order
from app.services.llm_chat import generate_answer

router = APIRouter()

class ChatRequest(BaseModel):
    customer_key: str
    message: str
    channel: str = "chat"

@router.post("/")
async def chat(req: ChatRequest):
    customer, conversation = get_or_create_customer_and_conversation(
        customer_key=req.customer_key,
        channel=req.channel
    )

    save_message(conversation["id"], "user", req.message)

    menu_hits = search_menu(req.message, match_count=5)
    recent = get_recent_messages(conversation["id"])

    answer = generate_answer(
        user_message=req.message,
        recent_messages=recent,
        menu_context=menu_hits,
        customer=customer,
        conversation=conversation
    )

    save_message(conversation["id"], "assistant", answer)
    maybe_extract_order(customer["id"], conversation["id"], req.message, answer)

    return {
        "reply": answer,
        "conversation_id": conversation["id"]
    }