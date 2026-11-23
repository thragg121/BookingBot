"""Ukrainian UI texts, button labels and date helpers."""

from datetime import date

CURRENCY = "грн"

BTN_BOOK = "📅 Записатися"
BTN_MY_BOOKINGS = "📖 Мої записи"
BTN_PROFILE = "👤 Профіль"
BTN_OWNER_PANEL = "🛠 Панель власника (демо)"

BTN_STATS = "📊 Статистика"
BTN_CLIENTS = "👥 Клієнти"
BTN_SCHEDULE = "🗓 Розклад"
BTN_SERVICES = "⚙ Послуги"
BTN_BROADCAST = "📢 Розсилка"
BTN_BACK = "⬅ Назад"

WEEKDAYS_SHORT = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
WEEKDAYS_FULL = [
    "понеділок", "вівторок", "середа", "четвер",
    "пʼятниця", "субота", "неділя",
]
MONTHS_GENITIVE = [
    "січня", "лютого", "березня", "квітня", "травня", "червня",
    "липня", "серпня", "вересня", "жовтня", "листопада", "грудня",
]


def format_price(price) -> str:
    value = f"{float(price):.2f}".rstrip("0").rstrip(".")
    return f"{value} {CURRENCY}"


def format_date_short(value: date) -> str:
    return (
        f"{WEEKDAYS_SHORT[value.weekday()]}, "
        f"{value.day} {MONTHS_GENITIVE[value.month - 1]}"
    )


def format_date_full(value: date) -> str:
    return (
        f"{WEEKDAYS_FULL[value.weekday()].capitalize()}, "
        f"{value.day} {MONTHS_GENITIVE[value.month - 1]} {value.year}"
    )


def mask_name(name: str | None) -> str:
    if not name:
        return "Клієнт"
    return name[0] + "***"
