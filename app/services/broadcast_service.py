from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.users import get_all_user_ids


async def send_broadcast(
    bot: Bot,
    session: AsyncSession,
    text: str,
) -> tuple[int, int]:
    user_ids = await get_all_user_ids(session)

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
