# ./VK-Vigil/database/db.py

from peewee import PostgresqlDatabase
from config import configs


dsn = "postgresql://{username}:{password}@{hostname}:{port}/bot".format(
    username=configs.database.user,
    password=configs.database.password,
    hostname=configs.database.hostname,
    port=configs.database.port,
)

db_instance = PostgresqlDatabase(database=dsn)
