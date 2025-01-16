# ./VK-Vigil/database/models.py

from peewee import (
    BigIntegerField,
    CharField,
    ForeignKeyField,
    SmallIntegerField,
    DateTimeField,
    TextField,
)
from playhouse.signals import Model

from .db import instance


class BaseModel(Model):
    class Meta:
        database = instance
        abstract = True


class Staff(BaseModel):
    id = BigIntegerField(primary_key=True)
    permission = SmallIntegerField(default=1, null=False)
    password_hash = TextField(unique=True, null=False)

    class Meta:
        table_name = "staff"


class Peer(BaseModel):
    id = BigIntegerField(primary_key=True)
    mark = CharField(max_length=10, null=False)
    name = CharField(max_length=255, null=True)

    class Meta:
        database = instance
        table_name = "peers"


class Sanction(BaseModel):
    peer = ForeignKeyField(
        model=Peer,
        backref="sanctions",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    user_id = BigIntegerField(null=False)
    points = SmallIntegerField(default=1, null=False)

    class Meta:
        table_name = "sanctions"


class Queue(BaseModel):
    peer = ForeignKeyField(
        model=Peer,
        backref="queue",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    user_id = BigIntegerField(null=False)
    message_cmid = BigIntegerField(null=False)
    expiration = DateTimeField(null=False)

    class Meta:
        table_name = "queue"


class ForbiddenWord(BaseModel):
    peer = ForeignKeyField(
        model=Peer,
        backref="forbidden_words",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    value = TextField(null=False)

    class Meta:
        table_name = "words"


class ForbiddenLink(BaseModel):
    peer = ForeignKeyField(
        model=Peer,
        backref="forbidden_links",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    value = TextField(null=False)

    class Meta:
        table_name = "forbidden_links"


class ForbiddenHost(BaseModel):
    peer = ForeignKeyField(
        model=Peer,
        backref="forbidden_hosts",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    value = TextField(null=False)

    class Meta:
        table_name = "forbidden_hosts"


class Setting(BaseModel):
    peer = ForeignKeyField(
        model=Peer,
        backref="settings",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    key = CharField(null=False)
    value = CharField(null=False)
    category = CharField(null=True)
    aliase = CharField(null=True)

    class Meta:
        table_name = "settings"
