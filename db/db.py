# ./VK-Vigil/database/db.py

from peewee import SqliteDatabase, PostgresqlDatabase, Database
from config import configs


DIALECT = configs.database.dialect
db_instance: Database

match DIALECT:
    case "sqlite":
        db_instance = SqliteDatabase(f"{configs.project_name}.db")

    case "postgresql":
        dsn = "postgresql://{username}:{password}@{hostname}/{database}".format(
            username=configs.database.user,
            password=configs.database.password,
            hostname=configs.database.hostname,
            database=configs.project_name,
        )
        db_instance = PostgresqlDatabase(database=dsn)

    case _:
        raise ValueError(
            f"Enable to create database isntance. Unknow\\Unsupported dialect '{DIALECT}'."
        )
