from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from sqlalchemy.orm import sessionmaker

from tgbot.services.repository import Repo


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, session: sessionmaker):
        super().__init__()
        self.session = session

    async def pre_process(self, obj, data, *args):
        db = self.session()
        data["db"] = db
        data["repo"] = Repo(db)

    async def post_process(self, obj, data, *args):
        del data["repo"]
        db = data.get("db")
        if db:
            await db.close()
