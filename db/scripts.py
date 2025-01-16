from peewee import signals
from .models import Delay, Setting, Conversation

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


@signals.post_save(sender=Conversation)
def add_default_settings_and_delays(model_class, instance, created):
    if created:
        for setting_data in DEFAULT_SETTINGS:
            Setting.create(
                conversation=instance,
                name=setting_data["name"],
                is_enabled=setting_data["is_enabled"],
            )

        for delay_data in DEFAULT_DELAYS:
            Delay.create(
                conversation=instance,
                name=delay_data["name"],
                count=delay_data["count"],
            )
