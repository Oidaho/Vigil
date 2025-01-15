# ./VK-Vigil/database/db.py

from typing import NoReturn
from peewee import SqliteDatabase, PostgresqlDatabase, Database
from config import configs


def get_db_isntanse(dialect: str) -> Database | NoReturn:
    match dialect.lower():
        case "sqlite":
            db_instance = SqliteDatabase("/app/db/bot.sqlite3")

        case "postgresql":
            dsn = "postgresql://{username}:{password}@{hostname}/bot".format(
                username=configs.database.user,
                password=configs.database.password,
                hostname=configs.database.hostname,
            )
            db_instance = PostgresqlDatabase(database=dsn)

        case _:
            raise ValueError(
                f"Enable to create database isntance. Unknow\\Unsupported dialect '{dialect}'."
            )

    return db_instance
