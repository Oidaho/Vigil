from playhouse.signals import post_save
from .models import Peer, Setting

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
                aliase=payload["aliase"],
            )
