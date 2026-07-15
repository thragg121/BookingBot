from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_user(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    result = await session.execute(
        select(User).where(User.id == user_id)
    )

    return result.scalar_one_or_none()


async def create_or_update_user(
    session: AsyncSession,
    user_id: int,
    first_name: str,
    username: str | None,
    language_code: str | None,
) -> User:
    user = await get_user(
        session=session,
        user_id=user_id,
    )

    if user is None:
        user = User(
            id=user_id,
            first_name=first_name,
            username=username,
            language_code=language_code,
        )
        session.add(user)
    else:
        user.first_name = first_name
        user.username = username
        user.language_code = language_code

    await session.commit()
    await session.refresh(user)

    return user


async def count_users(
    session: AsyncSession,
) -> int:
    result = await session.execute(
        select(func.count(User.id))
    )

    return int(result.scalar_one())

async def get_all_users(
    session: AsyncSession,
) -> list[User]:
    result = await session.execute(
        select(User).order_by(User.created_at.desc())
    )

    return list(result.scalars().all())

async def get_all_user_ids(
    session: AsyncSession,
) -> list[int]:
    result = await session.execute(
        select(User.id)
    )

    return list(result.scalars().all())
