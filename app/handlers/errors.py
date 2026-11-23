from aiogram import Router
from aiogram.types import ErrorEvent

from app.core.logger import logger


router = Router()


@router.errors()
async def global_error_handler(
    event: ErrorEvent,
) -> bool:
    logger.exception(
        "Unhandled exception while processing Telegram update: {}",
        event.exception,
    )

    update = event.update

    if update.message is not None:
        await update.message.answer(
            "⚠️ Сталася помилка.\n"
            "Спробуйте ще раз пізніше."
        )

    elif update.callback_query is not None:
        await update.callback_query.answer(
            "Сталася помилка.",
            show_alert=True,
        )

    return True
