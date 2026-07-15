from aiogram import Router

from app.handlers.admin_services_flow.create import (
    router as create_router,
)
from app.handlers.admin_services_flow.delete import (
    router as delete_router,
)
from app.handlers.admin_services_flow.duration import (
    router as duration_router,
)
from app.handlers.admin_services_flow.list import (
    router as list_router,
)
from app.handlers.admin_services_flow.price import (
    router as price_router,
)
from app.handlers.admin_services_flow.rename import (
    router as rename_router,
)
from app.handlers.admin_services_flow.toggle import (
    router as toggle_router,
)


router = Router()

router.include_router(list_router)
router.include_router(create_router)
router.include_router(toggle_router)
router.include_router(price_router)
router.include_router(duration_router)
router.include_router(rename_router)
router.include_router(delete_router)


__all__ = [
    "router",
]
