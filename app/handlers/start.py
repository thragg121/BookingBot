from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.main_menu import get_main_menu
from app.services.user_service import register_user
from config import Config


router = Router()


DEMO_NOTE = (
    "\n\n<i>🧪 Це демо-версія. Запишіться на будь-яку послугу — "
    "і ви одразу отримаєте сповіщення так, як його бачить власник. "
    "Також відкрийте «Панель власника», щоб побачити розклад і статистику.</i>"
)


@router.message(CommandStart())
async def start_handler(
    message: Message,
    session: AsyncSession,
    config: Config,
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

    text = (
        f"👋 Вітаємо, <b>{telegram_user.first_name}</b>!\n\n"
        "Це бот для онлайн-запису до салону <b>Beauty Studio</b>.\n\n"
        "Тут ви можете:\n"
        "• записатися на послугу за 30 секунд\n"
        "• переглянути свої записи\n"
        "• скасувати запис\n\n"
        "Оберіть дію нижче."
    )

    if config.demo_mode:
        text += DEMO_NOTE

    await message.answer(
        text,
        reply_markup=get_main_menu(config.demo_mode),
    )
