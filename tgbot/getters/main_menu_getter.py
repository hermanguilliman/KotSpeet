from aiogram_dialog import DialogManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tgbot.services.powerswitch import PowerSwitcher
from loguru import logger


# геттер главного меню
async def get_main_menu_data(dialog_manager: DialogManager,
                             scheduler: AsyncIOScheduler,
                             *args, **kwargs):
    jobs = scheduler.get_jobs()
    logger.debug(jobs)

    return {
        "jobs": len(jobs),
    }
