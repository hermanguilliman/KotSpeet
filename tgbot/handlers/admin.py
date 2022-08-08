from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo
from tgbot.models.database import User
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def admin_start(m: Message, repo: Repo, scheduler: AsyncIOScheduler,*args, **kwargs):
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
    await m.reply("Hello, admin!")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", role=UserRole.ADMIN)
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
