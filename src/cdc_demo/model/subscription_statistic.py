from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from cdc_demo.model.subscription import Subscription
import holidays
import pycountry
import pycountry_convert as pc


class DayPart(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"


class SubscriptionStatistic(BaseModel):
    is_subscribed: bool
    country_name: str
    created_at: datetime
    subscribed_on_holiday: bool
    topics: list[str]
    continent: str
    day_part: DayPart
    country_code: str

    @classmethod
    def from_subscription(cls, sub: Subscription) -> "SubscriptionStatistic":
        country_code = "UNDEFINED"
        continent = "UNDEFINED"
        subscribed_on_holiday = False

        country = pycountry.countries.get(name=sub.country_name)
        if country:
            country_code = country.alpha_2
            try:
                continent_code = pc.country_alpha2_to_continent_code(country_code)
                continent = pc.convert_continent_code_to_continent_name(continent_code)
            except Exception:
                pass
            try:
                subscribed_on_holiday = sub.created_at.date() in holidays.country_holidays(country_code)
            except Exception:
                pass

        hour = sub.created_at.hour
        if 5 <= hour < 12:
            day_part = DayPart.MORNING
        elif 12 <= hour < 17:
            day_part = DayPart.AFTERNOON
        elif 17 <= hour < 21:
            day_part = DayPart.EVENING
        else:
            day_part = DayPart.NIGHT

        return cls(
            is_subscribed=sub.is_subscribed,
            country_name=sub.country_name,
            created_at=sub.created_at,
            subscribed_on_holiday=subscribed_on_holiday,
            topics=sub.topics,
            continent=continent,
            day_part=day_part,
            country_code=country_code,
        )
