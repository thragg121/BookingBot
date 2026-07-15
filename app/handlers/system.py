from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.core.logger import logger


router = Router()

VERSION = "0.1.0"


@router.message(Command("ping"))
async def ping_handler(
    message: Message,
) -> None:
    await message.answer("🏓 Pong")


@router.message(Command("version"))
async def version_handler(
    message: Message,
) -> None:
    await message.answer(
        f"<b>BookingBot</b>\n"
        f"Version: <code>{VERSION}</code>"
    )


@router.message(Command("health"))
async def health_handler(
    message: Message,
) -> None:
    logger.info("Health check requested")

    await message.answer(
        "✅ Bot status: <b>Healthy</b>\n"
        f"Version: <code>{VERSION}</code>"
    )
