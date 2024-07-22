from typing import Dict, Optional

import redis
from decouple import config as env


redis_client = redis.Redis(
    host=env("REDIS_HOST", default="localhost"),
    port=env("REDIS_PORT", default=6379),
    db=env("REDIS_DB", default=0),
)

# Почему-то с апишки не приходит эта информация.
# Но 1 рубль всегда равен одному рублю)
redis_client.set("rates:RUB", "1.0")


def get_rate(charcode: str) -> Optional[float]:
    """
    Get the current VunitRate of a currency based on charcode.

    Uses `rates:{charcode}`.

    Returns:
        `float` if currency exists, otherwise returns `None`.
    """

    value_str = redis_client.get(f"rates:{charcode}")
    if value_str == None:
        return None
    return float(value_str)


def get_all_rates() -> Dict[str, float]:
    """
    Retrieve the `VunitRate` for all currencies from Redis.

    Scans Redis for keys matching the pattern `rates:*`.

    Returns:
        Dictionary formatted as this:
        `dict[charcode] -> VunitRate (float)`.
    """

    rates = {}
    keys = redis_client.keys("rates:*")
    for key in keys:
        str_key = key.decode()
        value_str = redis_client.get(str_key)
        if value_str == None:
            continue
        rates[str_key] = float(value_str)
    return rates
