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
    key = CharField(unique=True, null=False)
    value = CharField(null=False)
    category = CharField(null=True)
    aliase = CharField(null=True)

    class Meta:
        table_name = "settings"


DEFAULT_SETTINGS = [
    {
        "key": "filter_video",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Видео",
    },
    {
        "key": "filter_audio",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Аудио",
    },
    {
        "key": "filter_audio",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Голосовые сообщения",
    },
    {
        "key": "filter_link",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Ссылки",
    },
    {
        "key": "filter_poll",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Опросы",
    },
    {
        "key": "filter_wall",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Репосты",
    },
    {
        "key": "filter_doc",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Файлы",
    },
    {
        "key": "filter_app_action",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Мини-приложения",
    },
    {
        "key": "filter_graffiti",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Граффити",
    },
    {
        "key": "filter_stickker",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Стикеры",
    },
    {
        "key": "filter_forward",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Пересланые сообщения",
    },
    {
        "key": "filter_reply",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Ответы на сообщения",
    },
    {
        "key": "filter_geo",
        "value": "inactive",
        "category": "Фильтрация контента сообщений",
        "alias": "Геопозиция",
    },
    {
        "key": "check_urls_and_domains",
        "value": "inactive",
        "category": "Системы защиты",
        "alias": "Запрет определленных ссылок и доменов",
    },
    {
        "key": "check_forbidden_words",
        "value": "inactive",
        "category": "Системы защиты",
        "alias": "Запрет определленных слов",
    },
    {
        "key": "check_closed_pm",
        "value": "inactive",
        "category": "Критерии пользователей",
        "alias": "Закрытые ЛС",
    },
    {
        "key": "check_message_queue",
        "value": "inactive",
        "category": "Критерии пользователей",
        "alias": "Медленный режим сообещний",
    },
    {
        "key": "message_queue_interval",
        "value": "30",
        "category": "Временные интервалы",
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
