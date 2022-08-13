from loguru import logger
from aiogram import Dispatcher
from aiogram.types import Message, ChatType
from aiogram_dialog import DialogManager, StartMode
from tgbot.models.role import UserRole
from tgbot.services.repository import Repo
from tgbot.models.database import User

from tgbot.states.main_menu_states import MainState

async def admin_start(m: Message,
                      repo: Repo,
                      dialog_manager: DialogManager,
                      *args, **kwargs):
    user: User | None = await repo.get_user(m.from_user.id)
    if isinstance(user, User):
        if user.full_name != m.from_user.full_name:
            await repo.update_user_full_name(
                user_id=m.from_user.id,
                full_name=m.from_user.full_name)

    else: # register new user
        await repo.add_user(
            user_id=m.from_user.id,
            full_name=m.from_user.full_name,
            language_code=m.from_user.language_code,
        )
    
    await dialog_manager.start(MainState.central_state, mode=StartMode.RESET_STACK)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start,
                                commands=["start"],
                                state="*",
                                role=UserRole.ADMIN,
                                chat_type=ChatType.PRIVATE,
                                )