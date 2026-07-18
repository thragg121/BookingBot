from datetime import date

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.bookings import get_booked_intervals
from app.keyboards.times import get_times_keyboard
from app.states.booking import BookingState
from config import Config


router = Router()


@router.callback_query(
    BookingState.choosing_date,
    F.data.startswith("booking_date:"),
)
async def date_selected_handler(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    config: Config,
) -> None:
    if callback.data is None:
        return

    date_text = callback.data.split(":", maxsplit=1)[1]
    selected_date = date.fromisoformat(date_text)

    booking_data = await state.get_data()

    duration_minutes = int(
        booking_data["duration_minutes"]
    )

    booked_intervals = await get_booked_intervals(
        session=session,
        booking_date=selected_date,
    )

    keyboard = get_times_keyboard(
        booking_date=selected_date,
        service_duration_minutes=duration_minutes,
        booked_intervals=booked_intervals,
        working_hour_start=config.working_hour_start,
        working_hour_end=config.working_hour_end,
        minimum_booking_notice_minutes=(
            config.minimum_booking_notice_minutes
        ),
        slot_interval_minutes=(
            config.booking_slot_interval_minutes
        ),
    )

    if not keyboard.inline_keyboard:
        await callback.answer(
            "No available time slots for this date.",
            show_alert=True,
        )
        return

    await state.update_data(
        booking_date=selected_date.isoformat()
    )

    await state.set_state(
        BookingState.choosing_time
    )

    if callback.message is not None:
        await callback.message.edit_text(
            f"Selected date: "
            f"<b>{selected_date.strftime('%A, %d %B %Y')}</b>\n\n"
            "Choose an available time:",
            reply_markup=keyboard,
        )

    await callback.answer()
