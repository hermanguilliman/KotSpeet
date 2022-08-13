import asyncio
from aiogram_dialog import DialogManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tgbot.services.powerswitch import PowerSwitcher


async def reset_timer_getter(dialog_manager: DialogManager,
                             scheduler: AsyncIOScheduler,
                             *args, **kwargs):
    scheduler.remove_all_jobs()
    jobs: list = scheduler.get_jobs()
    if len(jobs) > 0:
        dialog_manager.current_context().dialog_data["error"] = 1
    else:
        dialog_manager.current_context().dialog_data["success"] = 1
    return {}

