from .auth import router as auth_router
from .health import router as health_router
from .index import router as index_router
from .peers import router as peers_router
from .staff import router as staff_router


__all__ = (
    "auth_router",
    "health_router",
    "index_router",
    "peers_router",
    "staff_router",
)
