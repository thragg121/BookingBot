from aiogram import Router

from app.handlers.booking_flow.confirm import (
    router as confirm_router,
)
from app.handlers.booking_flow.date import (
    router as date_router,
)
from app.handlers.booking_flow.my_bookings import (
    router as my_bookings_router,
)
from app.handlers.booking_flow.service import (
    router as service_router,
)
from app.handlers.booking_flow.start import (
    router as start_router,
)
from app.handlers.booking_flow.time import (
    router as time_router,
)


router = Router()

router.include_router(start_router)
router.include_router(service_router)
router.include_router(date_router)
router.include_router(time_router)
router.include_router(confirm_router)
router.include_router(my_bookings_router)


__all__ = [
    "router",
]
