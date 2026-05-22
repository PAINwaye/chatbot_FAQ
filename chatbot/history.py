from database.db import supabase


# CREATE CHAT
def create_chat(user_id, title):

    response = supabase.table(
        "chat_sessions"
    ).insert({
        "user_id": user_id,
        "title": title
    }).execute()

    return response.data[0]["id"]


# SAVE MESSAGE
def save_message(session_id, role, content):

    supabase.table("messages").insert({
        "session_id": session_id,
        "role": role,
        "content": content
    }).execute()


# LOAD USER CHATS
def load_chats(user_id):

    response = supabase.table(
        "chat_sessions"
    ).select("*") \
    .eq("user_id", user_id) \
    .order("created_at", desc=True) \
    .execute()

    return response.data


# LOAD CHAT MESSAGES
def load_messages(session_id):

    response = supabase.table(
        "messages"
    ).select("*") \
    .eq("session_id", session_id) \
    .order("created_at") \
    .execute()

    return response.data


# DELETE CHAT
def delete_chat(session_id):

    supabase.table(
        "chat_sessions"
    ).delete() \
    .eq("id", session_id) \
    .execute()