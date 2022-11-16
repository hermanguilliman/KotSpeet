from aiogram_dialog import Dialog, Window, DialogManager, ChatEvent
from typing import Any
from aiogram_dialog.widgets.text import Const, Format
from tgbot.getters.set_timer_getter import set_time_getter
from aiogram.types import ParseMode, CallbackQuery
from tgbot.states.reset_timer_state import ResetTimer
from aiogram_dialog.widgets.kbd import Cancel, Select, Button
from .helper import bolder
from loguru import logger


async def cancel_jobs(c: CallbackQuery,
                      button: Button,
                      manager: DialogManager,
                      *args, **kwargs):
    jobs = manager.current_context().dialog_data.get("jobs")
    if jobs and jobs > 0:
        await c.message.reply("🔒 Задача уже добавлена! Сначала удалите активную задачу 🔒")
    else:
        await manager.start(ResetTimer.preset_time_state)


# Диалог с установкой времени
reset_timer = Dialog(
    Window(
        Const(bolder('⏰ Отмена задания:')),
        Button(Const("Отменить"), id='reset_timer', on_click=cancel_jobs),
        Cancel(Const("Вернуться назад")),
        state=ResetTimer.reset_timer_request,
        parse_mode=ParseMode.HTML,
    ),

    Window(
        Const("Таймер сброшен"),
        Cancel(Const("Завершить")),
        state=ResetTimer.reset_confirm,
        parse_mode=ParseMode.HTML,
        getter=set_time_getter,
    ),
)
