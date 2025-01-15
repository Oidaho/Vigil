from .auth import router as auth_router
from .pages import router as pages_router
from .health import router as health_rouret


__all__ = ("auth_router", "pages_router", "health_rouret")
