from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.users import get_user
from app.services.profile_service import build_profile_text


router = Router()


@router.message(F.text == "👤 Profile")
async def profile_handler(
    message: Message,
    session: AsyncSession,
) -> None:
    if message.from_user is None:
        return

    user = await get_user(
        session=session,
        user_id=message.from_user.id,
    )

    if user is None:
        await message.answer(
            "Profile not found. Send /start first."
        )
        return

    await message.answer(
        build_profile_text(user)
    )
