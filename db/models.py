# ./VK-Vigil/database/models.py

from peewee import (
    BigIntegerField,
    CharField,
    ForeignKeyField,
    Model,
    SmallIntegerField,
    DateTimeField,
    BooleanField,
    IntegerField,
    TextField,
)

from .db import db_instance


# For storing moderated conversations
class Conversation(Model):
    peer_id = BigIntegerField(unique=True, null=False)
    name = CharField(max_length=255)
    mark = CharField(max_length=16, null=False)

    class Meta:
        table_name = "conversations"
        database = db_instance


# For storing moderation staff
class Staff(Model):
    user_id = BigIntegerField(unique=True, null=False)
    permission_lvl = SmallIntegerField(null=False)
    password_hash = TextField(unique=True, null=False)

    class Meta:
        table_name = "staff"
        database = db_instance


# To store sanctions against users
class Sanction(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="staff",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    user_id = BigIntegerField(null=False)
    warns_count = SmallIntegerField(default=1, null=False)

    class Meta:
        table_name = "sanctions"
        database = db_instance


# To store a message queue
class Queue(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="staff",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    user_id = BigIntegerField(null=False)
    message_id = BigIntegerField(null=False)
    expiration = DateTimeField(null=False)

    class Meta:
        table_name = "queue"
        database = db_instance


class Filter(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="staff",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    name = CharField(null=False)
    is_enabled = BooleanField(default=False, null=False)

    class Meta:
        table_name = "filters"
        database = db_instance


# To store time intervals between certain actions
class Delay(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="staff",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    name = CharField(null=False)
    count = IntegerField(null=False)

    class Meta:
        table_name = "delays"
        database = db_instance


# For storing forbidden words in conversations
class Word(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="staff",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    value = TextField(null=False)

    class Meta:
        table_name = "words"
        database = db_instance


# For storing forbidden/allowed links in conversations
class Link(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="staff",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    value = TextField(null=False)
    is_allowed = BooleanField(default=False, null=False)

    class Meta:
        table_name = "links"
        database = db_instance


# To store sites that are prohibited\allowed in conversations (by host name)
class Host(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="staff",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    value = TextField(null=False)
    is_allowed = BooleanField(default=False, null=False)

    class Meta:
        table_name = "hosts"
        database = db_instance
