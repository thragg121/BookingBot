from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.my_bookings import get_booking_actions_keyboard
from app.services.booking_service import (
    cancel_user_booking,
    list_user_bookings,
)
from app.services.notification_service import (
    notify_admins_about_cancellation,
)
from config import Config


router = Router()


@router.message(F.text == "📖 My Bookings")
async def my_bookings_handler(
    message: Message,
    session: AsyncSession,
) -> None:
    if message.from_user is None:
        return

    bookings = await list_user_bookings(
        session=session,
        user_id=message.from_user.id,
    )

    if not bookings:
        await message.answer(
            "You don't have any bookings yet."
        )
        return

    await message.answer(
        "📖 <b>Your Bookings</b>"
    )

    for booking, service in bookings:
        await message.answer(
            f"<b>{service.name}</b>\n"
            f"Booking ID: <code>{booking.id}</code>\n"
            f"📅 {booking.booking_date}\n"
            f"🕒 {booking.booking_time.strftime('%H:%M')}",
            reply_markup=get_booking_actions_keyboard(
                booking.id
            ),
        )


@router.callback_query(
    F.data.startswith("cancel_booking:")
)
async def cancel_user_booking_handler(
    callback: CallbackQuery,
    session: AsyncSession,
    bot: Bot,
    config: Config,
) -> None:
    if callback.data is None:
        return

    booking_id = int(
        callback.data.split(":", maxsplit=1)[1]
    )

    cancelled_data = await cancel_user_booking(
        session=session,
        booking_id=booking_id,
        user_id=callback.from_user.id,
    )

    if cancelled_data is None:
        await callback.answer(
            "Booking not found.",
            show_alert=True,
        )
        return

    booking, service = cancelled_data

    await notify_admins_about_cancellation(
        bot=bot,
        config=config,
        user_id=callback.from_user.id,
        first_name=callback.from_user.first_name,
        username=callback.from_user.username,
        booking_id=booking.id,
        service_name=service.name,
        booking_date=booking.booking_date.isoformat(),
        booking_time=booking.booking_time.strftime("%H:%M"),
    )

    if callback.message is not None:
        await callback.message.edit_text(
            "❌ Booking cancelled successfully."
        )

    await callback.answer()
