from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from config import Config


class IsAdmin(BaseFilter):
    """Real admins always pass; in demo mode every visitor may view the panel."""

    async def __call__(
        self,
        event: TelegramObject,
        config: Config,
    ) -> bool:
        user = getattr(event, "from_user", None)

        if user is None:
            return False

        return config.demo_mode or user.id in config.admin_ids


class IsDemoVisitor(BaseFilter):
    """True for non-admin users while the bot runs in demo mode."""

    async def __call__(
        self,
        event: TelegramObject,
        config: Config,
    ) -> bool:
        user = getattr(event, "from_user", None)

        if user is None or not config.demo_mode:
            return False

        return user.id not in config.admin_ids
