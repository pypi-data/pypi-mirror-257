import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SubscriptionPlan:
    id: str
    subscription: str
    created_at: str
    last_updated_at: str
    name: str
    length: int
    price_usd: str
    display_publicly: bool
    allow_more_subscriptions: bool

    @property
    def created_at_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.created_at)

    @property
    def last_updated_at_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.last_updated_at)

    @property
    def length_timedelta(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self.length)

    @property
    def price_usd_decimal(self) -> Decimal:
        return Decimal(self.price_usd)
