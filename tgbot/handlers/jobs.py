from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo
from tgbot.models.database import User
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tgbot.services.powerswitch import PowerSwitcher
from datetime import datetime, timedelta

async def show_jobs(m: Message, repo: Repo, scheduler: AsyncIOScheduler, switcher: PowerSwitcher):
    run_date = datetime.now() + timedelta(minutes=1)
    scheduler.add_job(switcher.reboot, "date", run_date=run_date)
    s = scheduler.get_jobs()
    await m.reply(f"Here is your jobs:\n {s}")


def register_job_list(dp: Dispatcher):
    dp.register_message_handler(show_jobs, commands=["jobs"], state="*", role=UserRole.ADMIN)
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
