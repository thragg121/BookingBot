from sqlalchemy.ext.asyncio import AsyncSession

from app.database.users import create_or_update_user
from app.models.user import User


async def register_user(
    session: AsyncSession,
    user_id: int,
    first_name: str,
    username: str | None,
    language_code: str | None,
) -> User:
    return await create_or_update_user(
        session=session,
        user_id=user_id,
        first_name=first_name,
        username=username,
        language_code=language_code,
    )
