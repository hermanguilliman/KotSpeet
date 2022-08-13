from aiogram.dispatcher.filters.state import StatesGroup, State


class ResetTimer(StatesGroup):
    reset_timer_request = State()
    reset_confirm = State()
