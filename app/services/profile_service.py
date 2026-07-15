from app.models.user import User


def build_profile_text(user: User) -> str:
    username = (
        f"@{user.username}"
        if user.username
        else "Not specified"
    )

    language = (
        user.language_code
        if user.language_code
        else "Not specified"
    )

    return (
        "👤 <b>Your Profile</b>\n\n"
        f"ID: <code>{user.id}</code>\n"
        f"Name: <b>{user.first_name}</b>\n"
        f"Username: {username}\n"
        f"Language: {language}\n"
        f"Registered: {user.created_at.strftime('%Y-%m-%d')}"
    )
