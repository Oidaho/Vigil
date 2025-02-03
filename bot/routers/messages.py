import re
from datetime import datetime, timedelta

import tldextract
from rules.messages import FromChatOnly, IgnorePermitted
from src.context import Context, Message
from src.routers import MessageRouter
from urlextract import URLExtract

from db.models import ForbiddenHost, ForbiddenLink, ForbiddenWord, Peer, Queue, Setting

from .utils import execute_conditional_warning, quiet_delete

router = MessageRouter(
    routing_ruleset=[
        FromChatOnly(),
        IgnorePermitted(),
    ]
)


attechments_map = {
    "video": "video_in_attachemnts",
    "audio": "audio_in_attachemnts",
    "audio_message": "audio_message_in_attachemnts",
    "link": "link_in_attachemnts",
    "poll": "poll_in_attachemnts",
    "wall": "wall_in_attachemnts",
    "doc": "doc_in_attachemnts",
    "app_action": "app_action_in_attachemnts",
    "graffiti": "graffiti_in_attachemnts",
    "sticker": "stickker_in_attachemnts",
    "forward": "forward_in_attachemnts",
    "geo": "geo_in_attachemnts",
    "photo": "photo_in_attachemnts",
    "reply": "reply_in_attachemnts",
}


@router.register(name="pm_check")
def check_private_messages(ctx: Context, msg: Message) -> bool:
    setting = (
        Setting.select()
        .join(Peer)
        .where((Setting.key == "check_closed_pm") & (Peer.id == ctx.peer.id))
        .get_or_none()
    )
    if setting and setting.value != "inactive":
        is_opened = ctx.api.users.get(
            user_ids=ctx.user.id,
            fields=["can_write_private_message"],
        )[0].get("can_write_private_message")
        if not is_opened:
            if setting.value == "active_quiet_delete":
                quiet_delete(ctx)

            else:
                execute_conditional_warning(
                    ctx, "Личные сообщения пользователя закрыты."
                )
            return True

    return False


@router.register(name="attachments_check")
def check_forbidden_attachments(ctx: Context, msg: Message) -> bool:
    attechments = msg.attachments
    to_check = [attechments_map.get(x) for x in attechments]
    settings = (
        Setting.select()
        .join(Peer)
        .where((Setting.key.in_(to_check)) & (Peer.id == ctx.peer.id))
    )
    for setting in settings:
        if setting.value != "allowed":
            if setting.value == "disallowed_quiet_delete":
                quiet_delete(ctx)

            else:
                execute_conditional_warning(
                    ctx, "Обнаружен запрещенный контент.", forward=True
                )

            return True

    return False


@router.register(name="links_check")
def check_forbidden_links(ctx: Context, msg: Message) -> bool:
    setting = (
        Setting.select()
        .join(Peer)
        .where((Setting.key == "check_forbidden_links") & (Peer.id == ctx.peer.id))
        .get_or_none()
    )
    if setting and setting.value != "inactive":
        extractor = URLExtract()
        links = extractor.find_urls(msg.text, only_unique=True)

        forbidden = (
            ForbiddenLink.select()
            .join(Peer)
            .where((ForbiddenLink.value.in_(links)) & (Peer.id == ctx.peer.id))
        )
        if forbidden:
            if setting.value == "active_quiet_delete":
                quiet_delete(ctx)

            else:
                execute_conditional_warning(
                    ctx, "Обнаружена запрещенная ссылка.", forward=True
                )

            return True

    return False


@router.register(name="domains_check")
def check_forbidden_domains(ctx: Context, msg: Message) -> bool:
    setting = (
        Setting.select()
        .join(Peer)
        .where((Setting.key == "check_forbidden_domains") & (Peer.id == ctx.peer.id))
        .get_or_none()
    )
    if setting and setting.value != "inactive":
        extractor = URLExtract()
        links = extractor.find_urls(msg.text, only_unique=True)

        hosts = set()
        for link in links:
            ext = tldextract.extract(link)
            hosts.add(f"{ext.subdomain}.{ext.domain}.{ext.suffix}")

        forbidden = (
            ForbiddenHost.select()
            .join(Peer)
            .where((ForbiddenHost.value.in_(hosts)) & (Peer.id == ctx.peer.id))
        )
        if forbidden:
            if setting.value == "active_quiet_delete":
                quiet_delete(ctx)

            else:
                execute_conditional_warning(
                    ctx, "Обнаружена ссылка на запрещенный домен.", forward=True
                )

            return True

    return False


@router.register(name="words_check")
def check_forbidden_words(ctx: Context, msg: Message) -> bool:
    setting = (
        Setting.select()
        .join(Peer)
        .where((Setting.key == "check_forbidden_words") & (Peer.id == ctx.peer.id))
        .get_or_none()
    )
    if setting and setting.value != "inactive":
        patterns = ForbiddenWord.select().join(Peer).where(Peer.id == ctx.peer.id)
        text = msg.text.lower()
        for pattern in patterns:
            if re.search(pattern.value, text, re.IGNORECASE):
                if setting.value == "active_quiet_delete":
                    quiet_delete(ctx)

                else:
                    execute_conditional_warning(
                        ctx, "Обнаружено запрещенное слово.", forward=True
                    )

                return True

    return False


@router.register(name="queue_check")
def check_message_queue(ctx: Context, msg: Message) -> bool:
    setting = (
        Setting.select()
        .join(Peer)
        .where((Setting.key == "check_message_queue") & (Peer.id == ctx.peer.id))
        .get_or_none()
    )
    if setting and setting.value != "inactive":
        peer = Peer.get_or_none(Peer.id == ctx.peer.id)
        item = (
            Queue.select()
            .where((Queue.user_id == ctx.user.id) & (Queue.peer == peer))
            .get_or_none()
        )

        interval = (
            Setting.select()
            .where((Setting.key == "message_queue_interval") & (Setting.peer == peer))
            .get_or_none()
        )

        now = datetime.utcnow()
        exp = now + timedelta(minutes=int(interval.value))
        if item:
            if item.expiration > now:
                if setting.value == "active_quiet_delete":
                    quiet_delete(ctx)

                else:
                    execute_conditional_warning(ctx, "Нарушен интервал сообщений.")

                return True

            else:
                item.expiration = exp
                item.message_cmid = msg.cmid
                item.save()

        else:
            new_item = Queue(
                peer=peer,
                user_id=ctx.user.id,
                message_cmid=msg.cmid,
                expiration=exp,
            )
            new_item.save()

    return False
