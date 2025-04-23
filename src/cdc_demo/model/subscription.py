from datetime import datetime

from pydantic import BaseModel


class Subscription(BaseModel):
    email: str
    first_name: str
    last_name: str
    is_subscribed: bool
    country_name: str
    topics: list[str]
    created_at: datetime
