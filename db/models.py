# ./VK-Vigil/database/models.py

from peewee import (
    BigIntegerField,
    CharField,
    ForeignKeyField,
    SmallIntegerField,
    DateTimeField,
    TextField,
)
from playhouse.signals import Model, post_save

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


DEFAULT_SETTINGS = [
    {
        "key": "video",
        "value": "inactive",
        "category": "content",
        "alias": "Видео",
    },
    {
        "key": "audio",
        "value": "inactive",
        "category": "content",
        "alias": "Аудио",
    },
    {
        "key": "audio_message",
        "value": "inactive",
        "category": "content",
        "alias": "Голосовые сообщения",
    },
    {
        "key": "link",
        "value": "inactive",
        "category": "content",
        "alias": "Ссылки",
    },
    {
        "key": "poll",
        "value": "inactive",
        "category": "content",
        "alias": "Опросы",
    },
    {
        "key": "wall",
        "value": "inactive",
        "category": "content",
        "alias": "Репосты",
    },
    {
        "key": "doc",
        "value": "inactive",
        "category": "content",
        "alias": "Файлы",
    },
    {
        "key": "app_action",
        "value": "inactive",
        "category": "content",
        "alias": "Мини-приложения",
    },
    {
        "key": "graffiti",
        "value": "inactive",
        "category": "content",
        "alias": "Граффити",
    },
    {
        "key": "stickker",
        "value": "inactive",
        "category": "content",
        "alias": "Стикеры",
    },
    {
        "key": "forward",
        "value": "inactive",
        "category": "content",
        "alias": "Пересланые сообщения",
    },
    {
        "key": "reply",
        "value": "inactive",
        "category": "content",
        "alias": "Ответы на сообщения",
    },
    {
        "key": "geo",
        "value": "inactive",
        "category": "content",
        "alias": "Геопозиция",
    },
    {
        "key": "urls_and_domains",
        "value": "inactive",
        "category": "content",
        "alias": "Ссылки и домены",
    },
    {
        "key": "forbidden_words",
        "value": "inactive",
        "category": "content",
        "alias": "Запрещенные слова",
    },
    {
        "key": "closed_pm",
        "value": "inactive",
        "category": "user",
        "alias": "Закрытое ЛС",
    },
    {
        "key": "message_queue",
        "value": "inactive",
        "category": "user",
        "alias": "Медленный режим сообещний",
    },
    {
        "key": "message_queue_interval",
        "value": "30",
        "category": "interval",
        "alias": "Интервал медленного режима",
    },
]


@post_save(sender=Peer)
def on_save_handler(model_class, instance, created):
    if created and instance.mark != "LOG":
        for payload in DEFAULT_SETTINGS:
            Setting.create(
                peer=instance,
                key=payload["key"],
                value=payload["value"],
                category=payload["category"],
                aliase=payload["alias"],
            )
