from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.texts import (
    BTN_BACK,
    BTN_CLIENTS,
    BTN_OWNER_PANEL,
    BTN_SCHEDULE,
    BTN_STATS,
)
from app.filters.admin import IsAdmin
from app.keyboards.admin import get_admin_menu
from app.keyboards.main_menu import get_main_menu
from app.services.admin_service import (
    get_clients_text,
    get_schedule_text,
    get_statistics_text,
)
from config import Config


router = Router()

router.message.filter(IsAdmin())


@router.message(Command("admin"))
@router.message(F.text == BTN_OWNER_PANEL)
async def admin_panel_handler(
    message: Message,
    config: Config,
) -> None:
    text = "🛠 <b>Панель власника</b>"

    if config.demo_mode:
        text += (
            "\n\nТут власник бачить статистику, розклад і клієнтів, "
            "керує послугами та робить розсилки.\n"
            "<i>У демо редагування та розсилка вимкнені.</i>"
        )

    await message.answer(text, reply_markup=get_admin_menu())


@router.message(F.text == BTN_STATS)
async def statistics_handler(
    message: Message,
    session: AsyncSession,
) -> None:
    await message.answer(await get_statistics_text(session))


@router.message(F.text == BTN_CLIENTS)
async def clients_handler(
    message: Message,
    session: AsyncSession,
    config: Config,
) -> None:
    await message.answer(
        await get_clients_text(session, anonymize=config.demo_mode)
    )


@router.message(F.text == BTN_SCHEDULE)
async def schedule_handler(
    message: Message,
    session: AsyncSession,
    config: Config,
) -> None:
    await message.answer(
        await get_schedule_text(session, anonymize=config.demo_mode)
    )


@router.message(F.text == BTN_BACK)
async def admin_back_handler(
    message: Message,
    config: Config,
) -> None:
    await message.answer(
        "Головне меню:",
        reply_markup=get_main_menu(config.demo_mode),
    )
