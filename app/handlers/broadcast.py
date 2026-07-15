from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.admin import get_admin_menu
from app.keyboards.broadcast import (
    get_broadcast_confirmation_keyboard,
)
from app.services.broadcast_service import send_broadcast
from app.states.admin import BroadcastState
from config import load_config


router = Router()

config = load_config()


def is_admin(user_id: int) -> bool:
    return user_id in config.admin_ids


@router.message(F.text == "📢 Broadcast")
async def broadcast_start_handler(
    message: Message,
    state: FSMContext,
) -> None:
    if message.from_user is None:
        return

    if not is_admin(message.from_user.id):
        await message.answer("Access denied.")
        return

    await state.clear()
    await state.set_state(
        BroadcastState.waiting_for_message
    )

    await message.answer(
        "Send the message you want to broadcast.\n\n"
        "HTML formatting is supported."
    )


@router.message(BroadcastState.waiting_for_message)
async def broadcast_message_handler(
    message: Message,
    state: FSMContext,
) -> None:
    if message.from_user is None:
        return

    if not is_admin(message.from_user.id):
        return

    if not message.text:
        await message.answer(
            "Please send a text message."
        )
        return

    await state.update_data(
        broadcast_text=message.text
    )

    await state.set_state(
        BroadcastState.confirming
    )

    await message.answer(
        "📢 <b>Broadcast preview</b>\n\n"
        f"{message.text}",
        reply_markup=get_broadcast_confirmation_keyboard(),
    )


@router.callback_query(
    BroadcastState.confirming,
    F.data == "broadcast_confirm",
)
async def broadcast_confirm_handler(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    bot: Bot,
) -> None:
    if not is_admin(callback.from_user.id):
        return

    data = await state.get_data()
    broadcast_text = data.get("broadcast_text")

    if not broadcast_text:
        await state.clear()
        await callback.answer(
            "Broadcast text is missing.",
            show_alert=True,
        )
        return

    success_count, failed_count = await send_broadcast(
        bot=bot,
        session=session,
        text=broadcast_text,
    )

    await state.clear()

    await callback.message.edit_text(
        "✅ <b>Broadcast completed</b>\n\n"
        f"Delivered: <b>{success_count}</b>\n"
        f"Failed: <b>{failed_count}</b>"
    )

    await callback.message.answer(
        "Admin panel:",
        reply_markup=get_admin_menu(),
    )

    await callback.answer()


@router.callback_query(
    BroadcastState.confirming,
    F.data == "broadcast_cancel",
)
async def broadcast_cancel_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not is_admin(callback.from_user.id):
        return

    await state.clear()

    await callback.message.edit_text(
        "❌ Broadcast cancelled."
    )

    await callback.message.answer(
        "Admin panel:",
        reply_markup=get_admin_menu(),
    )

    await callback.answer()
