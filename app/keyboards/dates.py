from datetime import date, timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_dates_keyboard(
    working_days: tuple[int, ...],
    days_ahead: int,
) -> InlineKeyboardMarkup:
    today = date.today()
    buttons: list[list[InlineKeyboardButton]] = []

    offset = 0

    while len(buttons) < days_ahead:
        booking_date = today + timedelta(days=offset)

        if booking_date.weekday() in working_days:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=booking_date.strftime(
                            "%a, %d %b"
                        ),
                        callback_data=(
                            "booking_date:"
                            f"{booking_date.isoformat()}"
                        ),
                    )
                ]
            )

        offset += 1

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
