from aiogram.dispatcher.filters.state import StatesGroup, State


class MainState(StatesGroup):
    central_state = State()