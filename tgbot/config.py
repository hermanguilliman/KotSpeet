import configparser
from dataclasses import dataclass
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import ast

@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_list: list[int]
    use_redis: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin_list=ast.literal_eval(tg_bot["admin_list"]),
            use_redis=tg_bot.getboolean("use_redis"),
        ),
        db=DbConfig(**config["db"]),
    )


jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///database.db')
    }