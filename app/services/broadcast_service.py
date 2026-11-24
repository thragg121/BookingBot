from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.users import get_all_user_ids, get_booked_user_ids
from app.keyboards.broadcast import AUDIENCE_BOOKED


async def get_audience_ids(
    session: AsyncSession,
    audience: str,
) -> list[int]:
    if audience == AUDIENCE_BOOKED:
        return await get_booked_user_ids(session)

    return await get_all_user_ids(session)


async def send_broadcast(
    bot: Bot,
    user_ids: list[int],
    text: str,
) -> tuple[int, int]:
    success_count = 0
    failed_count = 0

    for user_id in user_ids:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=text,
            )
            success_count += 1
        except Exception:
            failed_count += 1

    return success_count, failed_count
