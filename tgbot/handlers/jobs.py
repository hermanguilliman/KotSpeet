from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo
from tgbot.models.database import User
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def show_jobs(m: Message, repo: Repo, scheduler: AsyncIOScheduler,*args, **kwargs):
    def hhh():
        print("hey!")
    scheduler.add_job(hhh, "cron", day_of_week="*", hour=7, minute=0)
    s = scheduler.get_jobs()
    await m.reply(f"Here is your jobs:\n {s}")


def register_job_list(dp: Dispatcher):
    dp.register_message_handler(show_jobs, commands=["jobs"], state="*", role=UserRole.ADMIN)
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
