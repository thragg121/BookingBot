from datetime import date, timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_dates_keyboard(
    days_count: int = 7,
) -> InlineKeyboardMarkup:
    today = date.today()

    buttons = []

    for offset in range(days_count):
        booking_date = today + timedelta(days=offset)

        buttons.append(
            [
                InlineKeyboardButton(
                    text=booking_date.strftime("%a, %d %b"),
                    callback_data=(
                        f"booking_date:{booking_date.isoformat()}"
                    ),
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
