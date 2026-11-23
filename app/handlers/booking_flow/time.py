from datetime import date

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.core.texts import format_date_full
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

    formatted_date = format_date_full(
        date.fromisoformat(booking_data["booking_date"])
    )

    if callback.message is not None:
        await callback.message.edit_text(
            "📋 <b>Перевірте запис</b>\n\n"
            f"Послуга: <b>{booking_data['service_name']}</b>\n"
            f"Дата: <b>{formatted_date}</b>\n"
            f"Час: <b>{selected_time}</b>\n"
            f"Тривалість: "
            f"<b>{booking_data['duration_minutes']} хв</b>\n"
            f"Вартість: <b>{booking_data['service_price']}</b>",
            reply_markup=get_booking_confirmation_keyboard(),
        )

    await callback.answer()
