from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.main_menu import get_main_menu
from app.services.user_service import register_user


router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
    session: AsyncSession,
) -> None:
    telegram_user = message.from_user

    if telegram_user is None:
        return

    await register_user(
        session=session,
        user_id=telegram_user.id,
        first_name=telegram_user.first_name,
        username=telegram_user.username,
        language_code=telegram_user.language_code,
    )

    await message.answer(
        f"👋 Hello, <b>{telegram_user.first_name}</b>!\n\n"
        "Welcome to <b>BookingBot</b>.\n\n"
        "Here you can:\n"
        "• book an appointment\n"
        "• view your bookings\n"
        "• cancel an appointment\n"
        "• check your profile\n\n"
        "Choose an action below.",
        reply_markup=get_main_menu(),
    )
