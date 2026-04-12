from slowapi import Limiter
from slowapi.util import get_remote_address
from ..config import get_settings


def get_rate_limit_key():
    settings = get_settings()
    return f"{settings.rate_limit_requests}/second"


limiter = Limiter(key_func=get_remote_address)
