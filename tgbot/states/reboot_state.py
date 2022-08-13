from aiogram.dispatcher.filters.state import StatesGroup, State


class RebootState(StatesGroup):
    preset_time_state = State()
    add_job_state = State()
