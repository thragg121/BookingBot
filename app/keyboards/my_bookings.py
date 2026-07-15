from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_booking_actions_keyboard(
    booking_id: int,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Cancel Booking",
                    callback_data=f"cancel_booking:{booking_id}",
                )
            ]
        ]
    )
