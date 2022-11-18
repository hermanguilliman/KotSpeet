from aiogram_dialog import Dialog, Window, DialogManager, ChatEvent
from typing import Any
from aiogram_dialog.widgets.text import Const, Format
from tgbot.getters.reset_timer_getter import reset_timer_getter
from aiogram.types import ParseMode, CallbackQuery
from tgbot.states.reset_timer_state import ResetTimer
from aiogram_dialog.widgets.kbd import Cancel, Select, Button, Start, Next
from .helper import bolder
from loguru import logger


async def cancel_jobs(c: CallbackQuery,
                      button: Button,
                      manager: DialogManager,
                      *args, **kwargs):
    await manager.start(ResetTimer.reset_confirm)
    
    
# Диалог с установкой времени
reset_timer = Dialog(
    Window(
        Const(bolder('⏰Отмена активных заданий')),
        Next(Const("Сбросить все таймеры")),
        Cancel(Const("Вернуться назад")),
        state=ResetTimer.reset_timer_request,
        parse_mode=ParseMode.HTML,
    ),

    Window(
        Const("Таймер сброшен"),
        Cancel(Const("Завершить")),
        state=ResetTimer.reset_confirm,
        parse_mode=ParseMode.HTML,
        getter=reset_timer_getter,
    ),
)
