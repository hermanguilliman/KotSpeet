from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class ScheduleMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, scheduler):
        super().__init__()
        self.scheduler = scheduler

    async def pre_process(self, obj, data, *args):
        scheduler = self.scheduler
        data["scheduler"] = scheduler

    async def post_process(self, obj, data, *args):
        del data["scheduler"]

