# Главное меню
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Group, Row
from aiogram_dialog.widgets.text import Const, Format
from tgbot.states.main_menu_states import MainState
from aiogram.types import CallbackQuery, ParseMode
from tgbot.states.reset_timer_state import ResetTimer
from tgbot.states.set_timer_states import TimerState
from tgbot.getters.main_menu_getter import get_main_menu_data
from loguru import logger
from .helper import bolder


async def set_off_timer(c: CallbackQuery,
                        button: Button,
                        manager: DialogManager,
                        *args, **kwargs):
    jobs = manager.current_context().dialog_data.get("jobs")
    if jobs and jobs > 0:
        await c.message.reply("🔒 Задача уже добавлена! Сначала удалите активную задачу 🔒")
    else:
        await manager.start(TimerState.preset_time_state)


async def set_reboot_timer(c: CallbackQuery,
                           button: Button,
                           manager: DialogManager,
                           *args, **kwargs):
    jobs = manager.current_context().dialog_data.get("jobs")
    if jobs and jobs > 0:
        await c.message.reply("🔒 Задача уже добавлена! Сначала удалите активную задачу 🔒")
    else:
        await manager.start(TimerState.preset_time_state)


async def reset_timer(c: CallbackQuery,
                      button: Button,
                      manager: DialogManager,
                      *args, **kwargs):
    jobs = manager.current_context().dialog_data.get("jobs")
    if jobs and jobs == 0:
        await c.message.reply('Нечего удалять')
        logger.debug('Попытка удалить пустой список задач')
    else:
        await manager.start(ResetTimer.reset_timer_request)


# Кнопки главного меню. Кнопка сброса появляется если есть задачи
buttons = Group(
    Row(
        Button(Const("⏱ Таймер выключения"), id='set_off_timer', on_click=set_off_timer),
        Button(Const("💻 Таймер перезагрузки"), id='set_reboot_timer', on_click=set_reboot_timer),

    ),
    Row(
        Button(Format("🙅‍♂️ Удалить таймеры"),
               id='reset_timer',
               when='jobs',
               on_click=reset_timer,
               ),
    )
)

main_menu = Dialog(
    Window(
        Const(bolder("Это главный экран. Что желаете? 😺")),
        Format(bolder('Запланировано задач: {jobs}'), when='jobs'),
        buttons,
        state=MainState.central_state,
        getter=get_main_menu_data,
        parse_mode=ParseMode.HTML
    ),
)
