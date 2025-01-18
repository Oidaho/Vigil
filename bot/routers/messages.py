from src.context import Context, Message
from src.routers import MessageRouter
from db.models import Setting, Peer, ForbiddenLink, ForbiddenHost, ForbiddenWord
from loguru import logger
from urlextract import URLExtract
import tldextract

router = MessageRouter()


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
    is_opened = ctx.api.users.get(
        user_ids=ctx.user.id,
        fields=["can_write_private_message"],
    )[0].get("can_write_private_message")
    logger.debug(f"{is_opened=}")
    if is_opened:
        return False

    return True


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
        if setting.value == "disallowed":
            # TODO: exec delete
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
    logger.debug(f"{setting=}")
    logger.debug(f"{setting.value=}")
    if setting and setting.value == "active":
        extractor = URLExtract()
        links = extractor.find_urls(msg.text, only_unique=True)

        forbidden = (
            ForbiddenLink.select()
            .join(Peer)
            .where((ForbiddenLink.value.in_(links)) & (Peer.id == ctx.peer.id))
        )
        if forbidden:
            # TODO: exec delete
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
    logger.debug(f"{setting=}")
    logger.debug(f"{setting.value=}")
    if setting and setting.value == "active":
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
            # TODO: exec delete
            return True

    return False


# @router.register(name="words_check")
# def check_forbidden_words(ctx: Context, msg: Message) -> bool:
#     return True


# @router.register(name="queue_check")
# def check_message_queue(ctx: Context, msg: Message) -> bool:
#     return True
