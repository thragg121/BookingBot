from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.keyboards.admin_services import (
    get_services_admin_keyboard,
)
from app.services.service_admin import (
    list_services_for_admin,
    switch_service_status,
)


router = Router()

router.callback_query.filter(IsAdmin())


@router.callback_query(
    F.data.startswith("toggle_service:")
)
async def toggle_service_handler(
    callback: CallbackQuery,
    session: AsyncSession,
) -> None:
    if callback.data is None:
        return

    service_id = int(
        callback.data.split(":", maxsplit=1)[1]
    )

    updated = await switch_service_status(
        session=session,
        service_id=service_id,
    )

    if not updated:
        await callback.answer(
            "Service not found.",
            show_alert=True,
        )
        return

    services = await list_services_for_admin(session)

    if callback.message is not None:
        await callback.message.edit_reply_markup(
            reply_markup=get_services_admin_keyboard(
                services
            )
        )

    await callback.answer("Service updated.")
