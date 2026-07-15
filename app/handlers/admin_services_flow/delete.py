from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.keyboards.admin_services import get_services_admin_keyboard
from app.services.service_admin import (
    delete_admin_service,
    get_admin_service,
    list_services_for_admin,
)


router = Router()

router.callback_query.filter(IsAdmin())


@router.callback_query(
    F.data.startswith("delete_service:")
)
async def delete_service_handler(
    callback: CallbackQuery,
    session: AsyncSession,
) -> None:
    if callback.data is None:
        return

    service_id = int(
        callback.data.split(":", maxsplit=1)[1]
    )

    service = await get_admin_service(
        session=session,
        service_id=service_id,
    )

    if service is None:
        await callback.answer(
            "Service not found.",
            show_alert=True,
        )
        return

    try:
        deleted = await delete_admin_service(
            session=session,
            service_id=service_id,
        )
    except IntegrityError:
        await session.rollback()

        await callback.answer(
            "This service cannot be deleted because it has bookings. "
            "Disable it instead.",
            show_alert=True,
        )
        return

    if not deleted:
        await callback.answer(
            "Service not found.",
            show_alert=True,
        )
        return

    services = await list_services_for_admin(session)

    if callback.message is not None:
        if services:
            await callback.message.edit_text(
                f"🗑 Service deleted: <b>{service.name}</b>",
                reply_markup=get_services_admin_keyboard(
                    services
                ),
            )
        else:
            await callback.message.edit_text(
                f"🗑 Service deleted: <b>{service.name}</b>\n\n"
                "No services remain."
            )

    await callback.answer("Service deleted.")
