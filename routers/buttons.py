from bot.routers import ButtonRouter
from bot.context import Context
from typing import Dict

from bot.keyboards.responds import ShowSnackbar


router = ButtonRouter()


@router.register(name="close")
def close_button(ctx: Context, payload: Dict[str, int | str]) -> bool:
    ctx.api.messages.delete(
        peer_id=ctx.peer.id,
        cmids=ctx.button.cmid,
        delete_for_all=1,
    )

    ctx.api.messages.sendMessageEventAnswer(
        event_id=ctx.button.id,
        user_id=ctx.user.id,
        peer_id=ctx.peer.id,
        event_data=ShowSnackbar("❌ Closed.").json_str(),
    )

    # TODO: При необходимости рассмотреть вариант с удалением учтеной сессии из БД

    return True
