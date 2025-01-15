# ./VK-Vigil/database/db.py

from typing import NoReturn
from peewee import PostgresqlDatabase
from config import configs


dsn = "postgresql://{username}:{password}@{hostname}/bot".format(
    username=configs.database.user,
    password=configs.database.password,
    hostname=configs.database.hostname,
)

db_instance = PostgresqlDatabase(database=dsn)
