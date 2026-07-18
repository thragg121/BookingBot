from datetime import date, time

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.main_menu import get_main_menu
from app.services.booking_save import save_booking
from app.services.notification_service import (
    notify_admins_about_booking,
)
from app.states.booking import BookingState
from config import Config


router = Router()


@router.callback_query(
    BookingState.confirming,
    F.data == "booking_confirm",
)
async def booking_confirm_handler(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    bot: Bot,
    config: Config,
) -> None:
    booking_data = await state.get_data()

    required_fields = {
        "service_id",
        "service_name",
        "service_price",
        "booking_date",
        "booking_time",
    }

    if not required_fields.issubset(booking_data):
        await state.clear()

        await callback.answer(
            "Booking data is incomplete. Please start again.",
            show_alert=True,
        )
        return

    booking = await save_booking(
        session=session,
        user_id=callback.from_user.id,
        service_id=int(booking_data["service_id"]),
        booking_date=date.fromisoformat(
            booking_data["booking_date"]
        ),
        booking_time=time.fromisoformat(
            booking_data["booking_time"]
        ),
    )

    if booking is None:
        await state.clear()

        await callback.answer(
            "This time slot has just been booked by another client.",
            show_alert=True,
        )

        if callback.message is not None:
            await callback.message.edit_text(
                "⚠️ This time slot is no longer available.\n\n"
                "Please start a new booking and choose another time."
            )

            await callback.message.answer(
                "Choose an action:",
                reply_markup=get_main_menu(),
            )

        return

    await notify_admins_about_booking(
        bot=bot,
        config=config,
        user_id=callback.from_user.id,
        first_name=callback.from_user.first_name,
        username=callback.from_user.username,
        booking_id=booking.id,
        service_name=booking_data["service_name"],
        booking_date=booking_data["booking_date"],
        booking_time=booking_data["booking_time"],
        price=booking_data["service_price"],
    )

    await state.clear()

    if callback.message is not None:
        await callback.message.edit_text(
            "✅ <b>Booking confirmed!</b>\n\n"
            f"Booking ID: <code>{booking.id}</code>\n"
            f"Service: <b>{booking_data['service_name']}</b>\n"
            f"Date: <b>{booking_data['booking_date']}</b>\n"
            f"Time: <b>{booking_data['booking_time']}</b>\n"
            f"Price: <b>${booking_data['service_price']}</b>"
        )

        await callback.message.answer(
            "Choose another action:",
            reply_markup=get_main_menu(),
        )

    await callback.answer()


@router.callback_query(
    BookingState.confirming,
    F.data == "booking_cancel",
)
async def booking_cancel_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.clear()

    if callback.message is not None:
        await callback.message.edit_text(
            "❌ Booking creation cancelled."
        )

        await callback.message.answer(
            "Choose an action:",
            reply_markup=get_main_menu(),
        )

    await callback.answer()
