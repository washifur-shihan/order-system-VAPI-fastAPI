from app.db.supabase import supabase

def get_or_create_customer_and_conversation(customer_key: str, channel: str):
    # Step 1: find customer
    res = supabase.table("customers").select("*").eq("external_customer_id", customer_key).execute()

    if res.data:
        customer = res.data[0]
    else:
        customer = supabase.table("customers").insert({
            "external_customer_id": customer_key
        }).execute().data[0]

    # Step 2: create new conversation
    conversation = supabase.table("conversations").insert({
        "customer_id": customer["id"],
        "channel": channel
    }).execute().data[0]

    return customer, conversation


def save_message(conversation_id: str, role: str, content: str):
    supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "role": role,
        "content": content
    }).execute()

def get_memory_context(conversation_id: str):
    # last messages
    messages = supabase.table("messages") \
        .select("*") \
        .eq("conversation_id", conversation_id) \
        .order("created_at", desc=True) \
        .limit(10) \
        .execute().data

    messages = list(reversed(messages))

    # summary
    conv = supabase.table("conversations") \
        .select("summary") \
        .eq("id", conversation_id) \
        .single() \
        .execute().data

    return {
        "recent_messages": messages,
        "summary": conv.get("summary")
    }