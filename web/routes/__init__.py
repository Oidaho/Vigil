from .auth import router as auth_
from .health import router as health_
from .index import router as index_
from .peers import router as peers_
from .queue import router as queue_
from .sanctions import router as sanctions_
from .staff import router as staff_


__all__ = (
    "auth_",
    "health_",
    "index_",
    "peers_",
    "queue_",
    "sanctions_",
    "staff_",
)
