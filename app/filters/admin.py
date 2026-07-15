from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject

from config import Config


class IsAdmin(BaseFilter):
    async def __call__(
        self,
        event: TelegramObject,
        config: Config,
    ) -> bool:
        user = getattr(event, "from_user", None)

        if user is None:
            return False

        return user.id in config.admin_ids
