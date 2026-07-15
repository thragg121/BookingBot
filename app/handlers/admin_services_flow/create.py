from decimal import Decimal, InvalidOperation

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.keyboards.admin_services import get_services_admin_keyboard
from app.services.service_admin import (
    create_new_service,
    list_services_for_admin,
)
from app.states.service_management import ServiceManagementState


router = Router()

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(F.data == "add_service")
async def add_service_start_handler(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.clear()
    await state.set_state(
        ServiceManagementState.waiting_for_name
    )

    if callback.message is not None:
        await callback.message.answer(
            "Send the service name.\n\n"
            "Example: <code>Hair Coloring</code>"
        )

    await callback.answer()


@router.message(
    ServiceManagementState.waiting_for_name
)
async def add_service_name_handler(
    message: Message,
    state: FSMContext,
) -> None:
    if not message.text:
        await message.answer(
            "Send the service name as text."
        )
        return

    service_name = message.text.strip()

    if len(service_name) < 2:
        await message.answer(
            "The service name is too short."
        )
        return

    if len(service_name) > 150:
        await message.answer(
            "The service name is too long."
        )
        return

    await state.update_data(
        service_name=service_name
    )

    await state.set_state(
        ServiceManagementState.waiting_for_description
    )

    await message.answer(
        "Send a short service description.\n\n"
        "Send <code>-</code> to leave it empty."
    )


@router.message(
    ServiceManagementState.waiting_for_description
)
async def add_service_description_handler(
    message: Message,
    state: FSMContext,
) -> None:
    if not message.text:
        await message.answer(
            "Send the description as text."
        )
        return

    description_text = message.text.strip()

    description = (
        None
        if description_text == "-"
        else description_text
    )

    if description and len(description) > 500:
        await message.answer(
            "The description is too long."
        )
        return

    await state.update_data(
        service_description=description
    )

    await state.set_state(
        ServiceManagementState.waiting_for_new_duration
    )

    await message.answer(
        "Send the service duration in minutes.\n\n"
        "Example: <code>60</code>"
    )


@router.message(
    ServiceManagementState.waiting_for_new_duration
)
async def add_service_duration_handler(
    message: Message,
    state: FSMContext,
) -> None:
    if not message.text:
        await message.answer(
            "Send the duration as a whole number."
        )
        return

    try:
        duration_minutes = int(message.text.strip())
    except ValueError:
        await message.answer(
            "Invalid duration.\n"
            "Example: <code>60</code>"
        )
        return

    if duration_minutes < 5:
        await message.answer(
            "Duration must be at least 5 minutes."
        )
        return

    if duration_minutes > 1440:
        await message.answer(
            "Duration cannot exceed 1440 minutes."
        )
        return

    await state.update_data(
        service_duration=duration_minutes
    )

    await state.set_state(
        ServiceManagementState.waiting_for_new_price
    )

    await message.answer(
        "Send the service price.\n\n"
        "Example: <code>45.50</code>"
    )


@router.message(
    ServiceManagementState.waiting_for_new_price
)
async def add_service_price_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    if not message.text:
        await message.answer(
            "Send the price as a number."
        )
        return

    normalized_price = (
        message.text
        .strip()
        .replace(",", ".")
        .replace("$", "")
    )

    try:
        price = Decimal(normalized_price)
    except InvalidOperation:
        await message.answer(
            "Invalid price.\n"
            "Example: <code>45.50</code>"
        )
        return

    if price <= 0:
        await message.answer(
            "The price must be greater than zero."
        )
        return

    if price > Decimal("999999.99"):
        await message.answer(
            "The price is too high."
        )
        return

    state_data = await state.get_data()

    service = await create_new_service(
        session=session,
        name=state_data["service_name"],
        description=state_data.get(
            "service_description"
        ),
        duration_minutes=int(
            state_data["service_duration"]
        ),
        price=price,
    )

    await state.clear()

    services = await list_services_for_admin(session)

    await message.answer(
        "✅ <b>Service created</b>\n\n"
        f"Name: <b>{service.name}</b>\n"
        f"Duration: "
        f"<b>{service.duration_minutes} minutes</b>\n"
        f"Price: <b>${service.price:.2f}</b>",
        reply_markup=get_services_admin_keyboard(
            services
        ),
    )
