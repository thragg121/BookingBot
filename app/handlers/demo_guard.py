"""Blocks destructive owner actions for demo visitors."""

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.core.texts import BTN_BROADCAST
from app.filters.admin import IsDemoVisitor


router = Router()

router.message.filter(IsDemoVisitor())
router.callback_query.filter(IsDemoVisitor())

BLOCKED_CALLBACKS = (
    "add_service",
    "toggle_service:",
    "rename_service:",
    "edit_service_price:",
    "edit_service_duration:",
    "delete_service:",
)


@router.message(F.text == BTN_BROADCAST)
async def demo_broadcast_handler(message: Message) -> None:
    await message.answer(
        "📢 Тут власник надсилає повідомлення всім клієнтам: "
        "акції, вільні вікна, нагадування.\n\n"
        "<i>У демо розсилка вимкнена.</i>"
    )


@router.callback_query(F.data.startswith(BLOCKED_CALLBACKS))
async def demo_edit_handler(callback: CallbackQuery) -> None:
    await callback.answer(
        "У демо редагування послуг вимкнене. "
        "У вашій версії ви змінюєте назви, ціни та тривалість самі.",
        show_alert=True,
    )
