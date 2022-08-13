from datetime import datetime, timedelta
from aiogram_dialog import DialogManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tgbot.services.powerswitch import PowerSwitcher
from loguru import logger


# Ограничение на
async def set_time_getter(dialog_manager: DialogManager,
                          scheduler: AsyncIOScheduler,
                          switcher: PowerSwitcher,
                          *args, **kwargs):
    minutes = dialog_manager.current_context().dialog_data.get("minutes")
    hours = dialog_manager.current_context().dialog_data.get("hours")

    if isinstance(minutes, int) and isinstance(hours, int):
        run_date = datetime.now() + timedelta(hours=hours, minutes=minutes)
    elif isinstance(minutes, int):
        run_date = datetime.now() + timedelta(minutes=minutes)
    elif isinstance(hours, int):
        run_date = datetime.now() + timedelta(hours=hours)

    if isinstance(run_date, datetime):
        scheduler.add_job(switcher.shutdown, "date", run_date=run_date)

    await dialog_manager.done()
    return {}
