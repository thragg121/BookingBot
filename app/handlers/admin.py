from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.keyboards.admin import get_admin_menu
from app.keyboards.main_menu import get_main_menu
from app.services.admin_service import (
    get_clients_text,
    get_schedule_text,
    get_statistics_text,
)


router = Router()

router.message.filter(IsAdmin())


@router.message(Command("admin"))
async def admin_panel_handler(
    message: Message,
) -> None:
    await message.answer(
        "🛠 <b>Admin Panel</b>",
        reply_markup=get_admin_menu(),
    )


@router.message(F.text == "📊 Statistics")
async def statistics_handler(
    message: Message,
    session: AsyncSession,
) -> None:
    await message.answer(
        await get_statistics_text(session)
    )


@router.message(F.text == "👥 Clients")
async def clients_handler(
    message: Message,
    session: AsyncSession,
) -> None:
    await message.answer(
        await get_clients_text(session)
    )


@router.message(F.text == "🗓 Schedule")
async def schedule_handler(
    message: Message,
    session: AsyncSession,
) -> None:
    await message.answer(
        await get_schedule_text(session)
    )


@router.message(F.text == "⬅ Back")
async def admin_back_handler(
    message: Message,
) -> None:
    await message.answer(
        "Main menu:",
        reply_markup=get_main_menu(),
    )
