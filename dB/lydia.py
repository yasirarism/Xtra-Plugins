from database import db_x

lydia = db_x["LYDIA"]


async def add_chat(chat_id, session_id):
    stark = await lydia.find_one({"chat_id": chat_id})
    if stark:
        return False
    await lydia.insert_one({"chat_id": chat_id, "session_id": session_id})
    return True


async def remove_chat(chat_id):
    stark = await lydia.find_one({"chat_id": chat_id})
    if not stark:
        return False
    await lydia.delete_one({"chat_id": chat_id})
    return True

async def get_all_chats():
    return r if (r := [o async for o in lydia.find()]) else False


async def get_session(chat_id):
    stark = await lydia.find_one({"chat_id": chat_id})
    return False if not stark else stark

async def update_session(chat_id, session_id):
    await lydia.update_one({"chat_id": chat_id}, {"$set": {"session_id": session_id}})


