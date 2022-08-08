import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, DateTime, String

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = Column(BigInteger, primary_key=True, unique=True)
    full_name = Column(String(250))
    registration_date = Column(DateTime, default=datetime.datetime.now())
    language_code = Column(String(3))

    def is_new_user(self) -> bool:
        return self.registration_date >= (datetime.datetime.now() - datetime.timedelta(minutes=10))

    def __str__(self):
        return f"ID: {self.id} User: {self.full_name} Join date: {self.registration_date}"

    def __repr__(self):
        return f"ID: {self.id} User: {self.full_name} Join date: {self.registration_date}"