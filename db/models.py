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
    peer_id = BigIntegerField()
    name = CharField(max_length=255)
    mark = CharField(max_length=16)

    class Meta:
        table_name = "conversations"
        database = db_instance


# For storing moderation staff
class Staff(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="staff",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    user_id = BigIntegerField()
    permission_lvl = SmallIntegerField()

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
    user_id = BigIntegerField()
    warns_count = SmallIntegerField()
    expiration = DateTimeField()

    class Meta:
        table_name = "sanctions"
        database = db_instance


# To store active menus (keyboards)
class Menu(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="staff",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    message_id = BigIntegerField()
    expiration = DateTimeField()

    class Meta:
        table_name = "menus"
        database = db_instance


# To store a message queue
class Queue(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="staff",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    user_id = BigIntegerField()
    message_id = BigIntegerField()
    expiration = DateTimeField()

    class Meta:
        table_name = "queue"
        database = db_instance


# To store conversation content filtering settings
class Filter(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="staff",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    name = CharField()
    warns_count = SmallIntegerField()
    is_enabled = BooleanField()

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
    name = CharField()
    count = IntegerField()

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
    value = TextField()

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
    value = TextField()
    is_allowed = BooleanField()

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
    value = TextField()
    is_allowed = BooleanField()

    class Meta:
        table_name = "hosts"
        database = db_instance
