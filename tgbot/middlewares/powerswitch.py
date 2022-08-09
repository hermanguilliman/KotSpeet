from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from tgbot.services.powerswitch import PowerSwitcher


class PowerSwitcherMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, switcher: PowerSwitcher):
        super().__init__()
        self.switcher = switcher

    async def pre_process(self, obj, data, *args):
        switcher = self.switcher
        data["switcher"] = switcher

    async def post_process(self, obj, data, *args):
        del data["switcher"]
