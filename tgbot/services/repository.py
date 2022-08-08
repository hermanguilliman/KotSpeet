from typing import List
from sqlalchemy.orm import Session
from tgbot.models.database import User
from sqlalchemy import update, delete

class Repo:
    def __init__(self, session: Session):
        self.session = session

    # users
    async def add_user(self,
                       user_id: int,
                       full_name: str,
                       language_code: str) -> None:
        """add new user / создаём пользователя"""
        user = User(user_id=user_id,
                    full_name=full_name,
                    language_code=language_code,
                    )
        self.session.add(user)
        await self.session.commit()

    async def get_user(self, user_id: int) -> User | None:
        """return user by id / получить все данные о пользователе по id"""
        return await self.session.get(User, user_id)

    async def update_user_full_name(self, user_id: int, full_name: str) -> None:
        """update full_name of exist user / обновляет """
        stmt = (
            update(User).
            where(User.id == user_id).
            values(full_name=full_name)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_user(self, user_id):
        """ delete user by id / удаляем пользователя по id"""
        stmt = delete(User).where(User.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()