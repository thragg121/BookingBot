from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.texts import BTN_BROADCAST
from app.database.users import get_all_user_ids, get_booked_user_ids
from app.keyboards.admin import get_admin_menu
from app.keyboards.broadcast import (
    AUDIENCE_BOOKED,
    get_broadcast_audience_keyboard,
    get_broadcast_confirmation_keyboard,
)
from app.services.broadcast_service import get_audience_ids, send_broadcast
from app.states.admin import BroadcastState
from config import load_config


router = Router()

config = load_config()

AUDIENCE_LABELS = {
    "all": "усім клієнтам",
    AUDIENCE_BOOKED: "тим, хто має запис",
}


def is_admin(user_id: int) -> bool:
    return user_id in config.admin_ids


def can_broadcast(user_id: int) -> bool:
    # In demo mode visitors walk through the whole flow,
    # but the message is delivered only to themselves.
    return config.demo_mode or is_admin(user_id)


def is_demo_visitor(user_id: int) -> bool:
    return config.demo_mode and not is_admin(user_id)


@router.message(F.text == BTN_BROADCAST)
async def broadcast_start_handler(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if message.from_user is None:
        return

    if not can_broadcast(message.from_user.id):
        await message.answer("Доступ заборонено.")
        return

    all_count = len(await get_all_user_ids(session))
    booked_count = len(await get_booked_user_ids(session))

    await state.clear()
    await state.set_state(BroadcastState.choosing_audience)

    await message.answer(
        "📢 <b>Розсилка</b>\n\nКому надіслати повідомлення?",
        reply_markup=get_broadcast_audience_keyboard(
            all_count=all_count,
            booked_count=booked_count,
        ),
    )


@router.callback_query(
    BroadcastState.choosing_audience,
    F.data.startswith("broadcast_aud:"),
)
async def broadcast_audience_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not can_broadcast(callback.from_user.id):
        return

    audience = callback.data.split(":", 1)[1]
    await state.update_data(audience=audience)
    await state.set_state(BroadcastState.waiting_for_message)

    await callback.message.edit_text(
        f"Отримувачі: <b>{AUDIENCE_LABELS.get(audience, audience)}</b>.\n\n"
        "Надішліть текст розсилки. "
        "Наприклад: «Є вільні віконця на суботу» або «Знижка 10% цього тижня»."
    )
    await callback.answer()


@router.message(BroadcastState.waiting_for_message)
async def broadcast_message_handler(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if message.from_user is None:
        return

    if not can_broadcast(message.from_user.id):
        return

    if not message.text:
        await message.answer("Надішліть текстове повідомлення.")
        return

    data = await state.get_data()
    audience = data.get("audience", "all")
    recipients = len(await get_audience_ids(session, audience))

    await state.update_data(broadcast_text=message.html_text)
    await state.set_state(BroadcastState.confirming)

    await message.answer(
        "📢 <b>Попередній перегляд</b>\n"
        f"Отримувачі: {AUDIENCE_LABELS.get(audience, audience)} ({recipients})\n\n"
        f"{message.html_text}",
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
    user_id = callback.from_user.id

    if not can_broadcast(user_id):
        return

    data = await state.get_data()
    broadcast_text = data.get("broadcast_text")
    audience = data.get("audience", "all")

    if not broadcast_text:
        await state.clear()
        await callback.answer("Текст розсилки відсутній.", show_alert=True)
        return

    await state.clear()

    if is_demo_visitor(user_id):
        recipients = len(await get_audience_ids(session, audience))
        await callback.message.edit_text(
            "✅ <b>Розсилку надіслано</b> (демо)\n\n"
            f"У справжньому боті її отримали б {recipients} клієнтів "
            f"({AUDIENCE_LABELS.get(audience, audience)}). "
            "У демо повідомлення приходить тільки вам:"
        )
        await bot.send_message(
            chat_id=user_id,
            text=f"📣 <b>Beauty Studio:</b>\n{broadcast_text}",
        )
    else:
        user_ids = await get_audience_ids(session, audience)
        success_count, failed_count = await send_broadcast(
            bot=bot,
            user_ids=user_ids,
            text=broadcast_text,
        )
        await callback.message.edit_text(
            "✅ <b>Розсилку завершено</b>\n\n"
            f"Отримувачі: {AUDIENCE_LABELS.get(audience, audience)}\n"
            f"Доставлено: <b>{success_count}</b>\n"
            f"Не доставлено: <b>{failed_count}</b>"
        )

    await callback.message.answer(
        "Панель власника:",
        reply_markup=get_admin_menu(),
    )
    await callback.answer()


@router.callback_query(F.data == "broadcast_cancel")
async def broadcast_cancel_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if not can_broadcast(callback.from_user.id):
        return

    await state.clear()

    await callback.message.edit_text("❌ Розсилку скасовано.")

    await callback.message.answer(
        "Панель власника:",
        reply_markup=get_admin_menu(),
    )

    await callback.answer()
