# ./VK-Vigil/database/db.py

from peewee import PostgresqlDatabase
from config import configs


dsn = "postgresql://{username}:{password}@{hostname}:{port}/{database}".format(
    username=configs.database.user,
    password=configs.database.password,
    database=configs.database.database,
    hostname=configs.database.hostname,
    port=configs.database.port,
)

instance = PostgresqlDatabase(database=dsn)
