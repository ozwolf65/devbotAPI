import pydantic


class RequestBody(pydantic.BaseModel):
    name: str


class Subscription(pydantic.BaseModel):
    """
    Represents a subscription registration for a service worker
    """

    endpoint: str
    """Endpoint URL for the subscription"""
    expirationTime: int | None
    """Expiration time for the subscription"""
    keys: dict[str, str]
    """Auth keys for the subscription"""


class ResponseBody(pydantic.BaseModel):
    queue: list[str]


class UsageResponseBody(pydantic.BaseModel):
    usages: dict[str, int]
