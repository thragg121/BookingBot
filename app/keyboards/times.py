from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


DEFAULT_TIME_SLOTS = [
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
]


def get_times_keyboard(
    booked_times: set[str],
) -> InlineKeyboardMarkup:
    available_times = [
        time_value
        for time_value in DEFAULT_TIME_SLOTS
        if time_value not in booked_times
    ]

    rows = []

    for index in range(0, len(available_times), 2):
        row = []

        for time_value in available_times[index:index + 2]:
            row.append(
                InlineKeyboardButton(
                    text=time_value,
                    callback_data=f"booking_time:{time_value}",
                )
            )

        rows.append(row)

    return InlineKeyboardMarkup(
        inline_keyboard=rows
    )
