# ./VK-Vigil/database/db.py

from peewee import SqliteDatabase, PostgresqlDatabase, Database
from config import configs


DIALECT = configs.database.dialect
db_instance: Database

match DIALECT:
    case "sqlite":
        db_instance = SqliteDatabase("vigil.db")

    case "postgresql":
        dsn = "postgresql://{username}:{password}@{hostname}/vigil".format(
            username=configs.database.user,
            password=configs.database.password,
            hostname=configs.database.hostname,
        )
        db_instance = PostgresqlDatabase(database=dsn)

    case _:
        raise ValueError(
            f"Enable to create database isntance. Unknow\\Unsupported dialect '{DIALECT}'."
        )
