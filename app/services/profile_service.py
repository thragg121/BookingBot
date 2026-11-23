from app.models.user import User


def build_profile_text(user: User) -> str:
    username = f"@{user.username}" if user.username else "не вказано"

    return (
        "👤 <b>Ваш профіль</b>\n\n"
        f"Імʼя: <b>{user.first_name}</b>\n"
        f"Telegram: {username}\n"
        f"З нами з: {user.created_at.strftime('%d.%m.%Y')}"
    )
