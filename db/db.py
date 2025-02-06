# ./VK-Vigil/database/db.py

from peewee import PostgresqlDatabase
from config import configs


dsn = "postgresql://{username}:{password}@{hostname}:{port}/{database}".format(
    username=configs.database.POSGRES_USER,
    password=configs.database.POSGRES_PASSWORD,
    database=configs.database.POSGRES_NAME,
    hostname=configs.database.POSGRES_HOST,
    port=configs.database.POSGRES_PORT,
)

instance = PostgresqlDatabase(database=dsn)
