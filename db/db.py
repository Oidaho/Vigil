# ./VK-Vigil/database/db.py

from typing import NoReturn
from peewee import SqliteDatabase, PostgresqlDatabase, Database
from config import configs


DIALECT = configs.database.dialect
db_instance: Database = None


def get_db_isntanse() -> Database | NoReturn:
    match DIALECT:
        case "sqlite":
            return SqliteDatabase("/app/db/bot.sqlite3")

        case "postgresql":
            dsn = "postgresql://{username}:{password}@{hostname}/bot".format(
                username=configs.database.user,
                password=configs.database.password,
                hostname=configs.database.hostname,
            )
            return PostgresqlDatabase(database=dsn)

        case _:
            raise ValueError(
                f"Enable to create database isntance. Unknow\\Unsupported dialect '{DIALECT}'."
            )
    