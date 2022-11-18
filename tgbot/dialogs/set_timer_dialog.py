from aiogram_dialog import Dialog, Window, DialogManager, ChatEvent
from typing import Any
from aiogram_dialog.widgets.text import Const, Format
from tgbot.getters.set_timer_getter import set_time_getter
from aiogram.types import ParseMode
from tgbot.states.set_timer_states import TimerState
from aiogram_dialog.widgets.kbd import Cancel, Select
from .helper import bolder
from loguru import logger


# sending hours to next window
async def hours_changed(c: ChatEvent,
                        select: Any,
                        manager: DialogManager,
                        item_id: str,
                        ):
    manager.current_context().dialog_data["hours"] = int(item_id)
    await manager.dialog().next()


# sending minutes to next window
async def minutes_changed(c: ChatEvent,
                          select: Any,
                          manager: DialogManager,
                          item_id: str,
                          ):
    manager.current_context().dialog_data["minutes"] = int(item_id)
    await manager.dialog().next()


# Диалог с установкой времени
timer = Dialog(
    Window(
        Const(bolder('⏰ Установите таймер:')),
        Const(bolder("Верхняя строка - часы")),
        Select(
            Format("{item}"),
            items=[1, 2, 3, 4, 5, ],
            item_id_getter=lambda x: x,
            id="hours",
            on_click=hours_changed,
        ),
        Const(bolder("Нижняя строка - минуты")),
        Select(
            Format("{item}"),
            items=[10, 20, 30, 40, 50],
            item_id_getter=lambda x: x,
            id="minutes",
            on_click=minutes_changed,
        ),

        Cancel(Const("Отмена 🙅‍♂️")),
        state=TimerState.preset_time_state,
        parse_mode=ParseMode.HTML,
    ),

    Window(
        Const("Время установлено"),
        Cancel(Const("Завершить")),
        state=TimerState.add_job_state,
        parse_mode=ParseMode.HTML,
        getter=set_time_getter,
    ),
)
