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


DEFAULT_SETTINGS = [
    {"name": "filter_video", "is_enabled": False},
    {"name": "filter_audio", "is_enabled": False},
    {"name": "filter_audio_message", "is_enabled": False},
    {"name": "filter_link", "is_enabled": False},
    {"name": "filter_poll", "is_enabled": False},
    {"name": "filter_wall", "is_enabled": False},
    {"name": "filter_doc", "is_enabled": False},
    {"name": "filter_app_action", "is_enabled": False},
    {"name": "filter_graffiti", "is_enabled": False},
    {"name": "filter_sticker", "is_enabled": False},
    {"name": "filter_forward", "is_enabled": False},
    {"name": "filter_reply", "is_enabled": False},
    {"name": "filter_geo", "is_enabled": False},
    {"name": "check_curse_words", "is_enabled": False},
    {"name": "check_account_age", "is_enabled": False},
    {"name": "check_open_pm", "is_enabled": False},
    {"name": "check_message_queue", "is_enabled": False},
    {"name": "check_urls", "is_enabled": False},
    {"name": "check_urls_hard", "is_enabled": False},
]


DEFAULT_DELAYS = [
    {"name": "queue_mode_delay_minutes", "count": 30},
    {"name": "account_age_days", "count": 7},
]


class Conversation(Model):
    peer_id = BigIntegerField(unique=True, null=False)
    name = CharField(max_length=255)
    mark = CharField(max_length=16, null=False)

    class Meta:
        table_name = "conversations"
        database = db_instance

    def save(self, *args, **kwargs):
        created = not bool(self.id)
        super().save(*args, **kwargs)

        if created and self.mark != "LOG":
            for setting_data in DEFAULT_SETTINGS:
                Setting.create(
                    conversation=self,
                    name=setting_data["name"],
                    is_enabled=setting_data["is_enabled"],
                )

            for delay_data in DEFAULT_DELAYS:
                Delay.create(
                    conversation=self,
                    name=delay_data["name"],
                    count=delay_data["count"],
                )


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
        backref="sanctions",
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
        backref="queue",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    user_id = BigIntegerField(null=False)
    message_id = BigIntegerField(null=False)
    expiration = DateTimeField(null=False)

    class Meta:
        table_name = "queue"
        database = db_instance


class Setting(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="settings",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    name = CharField(null=False)
    is_enabled = BooleanField(default=False, null=False)

    class Meta:
        table_name = "settings"
        database = db_instance


# To store time intervals between certain actions
class Delay(Model):
    conversation = ForeignKeyField(
        model=Conversation,
        backref="delays",
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
        backref="words",
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
        backref="links",
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
        backref="hosts",
        on_delete="CASCADE",
        on_update="CASCADE",
    )
    value = TextField(null=False)
    is_allowed = BooleanField(default=False, null=False)

    class Meta:
        table_name = "hosts"
        database = db_instance
