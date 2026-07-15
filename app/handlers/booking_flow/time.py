from datetime import date

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.keyboards.confirmation import get_booking_confirmation_keyboard
from app.states.booking import BookingState


router = Router()


@router.callback_query(
    BookingState.choosing_time,
    F.data.startswith("booking_time:"),
)
async def time_selected_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if callback.data is None:
        return

    selected_time = callback.data.split(":", maxsplit=1)[1]

    await state.update_data(
        booking_time=selected_time
    )

    booking_data = await state.get_data()

    await state.set_state(
        BookingState.confirming
    )

    formatted_date = date.fromisoformat(
        booking_data["booking_date"]
    ).strftime("%A, %d %B %Y")

    if callback.message is not None:
        await callback.message.edit_text(
            "📋 <b>Please confirm your booking</b>\n\n"
            f"Service: <b>{booking_data['service_name']}</b>\n"
            f"Date: <b>{formatted_date}</b>\n"
            f"Time: <b>{selected_time}</b>\n"
            f"Duration: "
            f"<b>{booking_data['duration_minutes']} minutes</b>\n"
            f"Price: <b>${booking_data['service_price']}</b>",
            reply_markup=get_booking_confirmation_keyboard(),
        )

    await callback.answer()
