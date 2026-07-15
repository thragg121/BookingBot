from datetime import date

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.bookings import get_booked_times
from app.keyboards.times import get_times_keyboard
from app.states.booking import BookingState


router = Router()


@router.callback_query(
    BookingState.choosing_date,
    F.data.startswith("booking_date:"),
)
async def date_selected_handler(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if callback.data is None:
        return

    date_text = callback.data.split(":", maxsplit=1)[1]
    selected_date = date.fromisoformat(date_text)

    booked_times = await get_booked_times(
        session=session,
        booking_date=selected_date,
    )

    if len(booked_times) >= 8:
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
            reply_markup=get_times_keyboard(booked_times),
        )

    await callback.answer()
