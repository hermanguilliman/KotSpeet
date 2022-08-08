from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.repository import Repo
from tgbot.models.database import User

async def user_start(m: Message, repo: Repo):
    # update full name if it changes
    user: User | None = await repo.get_user(m.from_user.id)
    if isinstance(user, User):
        if user.full_name != m.from_user.full_name:
            await repo.update_user_full_name(
                user_id=m.from_user.id,
                full_name=m.from_user.full_name)

    else: # register new user
        await repo.add_user(
            user_id=m.from_user.id,
            full_name=m.from_user.full_name,
            language_code=m.from_user.language_code,
        )
    await m.reply("Bot is under construction!")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
