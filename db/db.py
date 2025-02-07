# ./VK-Vigil/database/db.py

from peewee import PostgresqlDatabase
from config import configs


dsn = "postgresql://{username}:{password}@{hostname}:{port}/{database}".format(
    username=configs.database.POSTGRES_USER,
    password=configs.database.POSTGRES_PASSWORD,
    database=configs.database.POSTGRES_NAME,
    hostname=configs.database.POSTGRES_HOST,
    port=configs.database.POSTGRES_PORT,
)

instance = PostgresqlDatabase(database=dsn)
