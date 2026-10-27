from fastapi import Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import TRUSTED_PROXIES
from app.logger import get_logger

log = get_logger(__name__)


def get_client_ip(request: Request) -> str:
    direct_ip = request.client.host if request.client else "unknown"
    if direct_ip in TRUSTED_PROXIES:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
    return direct_ip


limiter = Limiter(key_func=get_client_ip)


def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    log.warning(
        "rate limit exceeded: ip=%s path=%s limit=%s",
        get_client_ip(request),
        request.url.path,
        exc.detail,
    )
    return _rate_limit_exceeded_handler(request, exc)
