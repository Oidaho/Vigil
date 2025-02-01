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
        indexes = ((("peer", "user_id"), True),)


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
        indexes = ((("peer", "user_id"), True),)


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
        indexes = ((("peer", "value"), True),)


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
        indexes = ((("peer", "value"), True),)


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
        indexes = ((("peer", "value"), True),)


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
    alias_ = CharField(null=True)

    class Meta:
        table_name = "settings"
        indexes = ((("peer", "key"), True),)


DEFAULT_SETTINGS = [
    {
        "key": "video_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Видео",
    },
    {
        "key": "audio_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Аудио",
    },
    {
        "key": "audio_message_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Голосовые сообщения",
    },
    {
        "key": "photo_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Фотографии",
    },
    {
        "key": "link_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Ссылки",
    },
    {
        "key": "poll_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Опросы",
    },
    {
        "key": "wall_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Репосты",
    },
    {
        "key": "doc_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Файлы",
    },
    {
        "key": "app_action_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Мини-приложения",
    },
    {
        "key": "graffiti_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Граффити",
    },
    {
        "key": "stickker_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Стикеры",
    },
    {
        "key": "forward_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Пересланые сообщения",
    },
    {
        "key": "reply_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Ответы на сообщения",
    },
    {
        "key": "geo_in_attachemnts",
        "value": "allowed",
        "category": "Фильтрация вложений сообщения",
        "alias": "Геопозиция",
    },
    {
        "key": "check_forbidden_links",
        "value": "inactive",
        "category": "Системы защиты",
        "alias": "Обнаружение запрещенных ссылок",
    },
    {
        "key": "check_forbidden_domains",
        "value": "inactive",
        "category": "Системы защиты",
        "alias": "Обнаружение запрещенных доменов",
    },
    {
        "key": "check_forbidden_words",
        "value": "inactive",
        "category": "Системы защиты",
        "alias": "Обнаружение запрещенных слов",
    },
    {
        "key": "check_closed_pm",
        "value": "inactive",
        "category": "Критерии пользователей",
        "alias": "Проверка закрытых ЛС",
    },
    {
        "key": "check_message_queue",
        "value": "inactive",
        "category": "Критерии пользователей",
        "alias": "Медленный режим сообщений",
    },
    {
        "key": "message_queue_interval",
        "value": "30",
        "category": "Временные интервалы",
        "alias": "Интервал медленного режима (мин.)",
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
                alias_=payload["alias"],
            )
