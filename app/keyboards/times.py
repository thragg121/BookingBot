from datetime import date, datetime, time, timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_time_slots(
    working_hour_start: int,
    working_hour_end: int,
    slot_interval_minutes: int,
) -> list[str]:
    current_slot = datetime.combine(
        date.today(),
        time(
            hour=working_hour_start,
            minute=0,
        ),
    )

    workday_end = datetime.combine(
        date.today(),
        time(
            hour=working_hour_end % 24,
            minute=0,
        ),
    )

    if working_hour_end == 24:
        workday_end += timedelta(days=1)

    slots: list[str] = []

    while current_slot < workday_end:
        slots.append(
            current_slot.strftime("%H:%M")
        )

        current_slot += timedelta(
            minutes=slot_interval_minutes
        )

    return slots


def _slot_is_available(
    slot_value: str,
    booking_date: date,
    service_duration_minutes: int,
    booked_intervals: list[tuple[str, int]],
    working_hour_end: int,
    minimum_booking_notice_minutes: int,
) -> bool:
    slot_start = datetime.combine(
        booking_date,
        time.fromisoformat(slot_value),
    )

    slot_end = slot_start + timedelta(
        minutes=service_duration_minutes
    )

    earliest_allowed_start = datetime.now() + timedelta(
        minutes=minimum_booking_notice_minutes
    )

    if slot_start < earliest_allowed_start:
        return False

    workday_end = datetime.combine(
        booking_date,
        time(
            hour=working_hour_end % 24,
            minute=0,
        ),
    )

    if working_hour_end == 24:
        workday_end += timedelta(days=1)

    if slot_end > workday_end:
        return False

    for booked_time, booked_duration in booked_intervals:
        booked_start = datetime.combine(
            booking_date,
            time.fromisoformat(booked_time),
        )

        booked_end = booked_start + timedelta(
            minutes=booked_duration
        )

        overlaps = (
            slot_start < booked_end
            and slot_end > booked_start
        )

        if overlaps:
            return False

    return True


def get_times_keyboard(
    booking_date: date,
    service_duration_minutes: int,
    booked_intervals: list[tuple[str, int]],
    working_hour_start: int,
    working_hour_end: int,
    minimum_booking_notice_minutes: int,
    slot_interval_minutes: int,
) -> InlineKeyboardMarkup:
    all_time_slots = build_time_slots(
        working_hour_start=working_hour_start,
        working_hour_end=working_hour_end,
        slot_interval_minutes=slot_interval_minutes,
    )

    available_times = [
        slot_value
        for slot_value in all_time_slots
        if _slot_is_available(
            slot_value=slot_value,
            booking_date=booking_date,
            service_duration_minutes=(
                service_duration_minutes
            ),
            booked_intervals=booked_intervals,
            working_hour_end=working_hour_end,
            minimum_booking_notice_minutes=(
                minimum_booking_notice_minutes
            ),
        )
    ]

    rows: list[list[InlineKeyboardButton]] = []

    for index in range(0, len(available_times), 2):
        row = [
            InlineKeyboardButton(
                text=time_value,
                callback_data=f"booking_time:{time_value}",
            )
            for time_value in available_times[
                index:index + 2
            ]
        ]

        rows.append(row)

    return InlineKeyboardMarkup(
        inline_keyboard=rows
    )
