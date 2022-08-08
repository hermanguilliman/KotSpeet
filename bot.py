import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user
from tgbot.handlers.jobs import register_job_list
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from tgbot.models.database import Base

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tgbot.middlewares.schedule import ScheduleMiddleware


logger = logging.getLogger(__name__)


async def create_pool(user, password, database, host, echo):
    url = "sqlite+aiosqlite:///database.db"
    engine = create_async_engine(url, echo=echo, future=True)
    # create metadata
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # session
    session = sessionmaker(engine,
                           expire_on_commit=False,
                           class_=AsyncSession,
                           )
    return session


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config("bot.ini")

    if config.tg_bot.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        echo=False,
    )

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)
    scheduler = AsyncIOScheduler()
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(ScheduleMiddleware(scheduler))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_user(dp)
    register_job_list(dp)

    # start
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
