import json
from dataclasses import dataclass
from datetime import (datetime, timedelta)
from requests import Response
from .. import constants
from ..http_requests import signed_requests
from ..utils.caching import CacheSystem


SUBSCRIPTION_CACHE: CacheSystem = CacheSystem(default_expiry_time=600)


@dataclass
class Subscription:
    id: str
    created_at: str
    last_updated_at: str
    name: str
    description: str | None
    owner: str
    length: int
    display_publicly: bool
    allow_more_subscriptions: bool

    @property
    def created_at_datetime(self) -> datetime:
        return datetime.fromisoformat(self.created_at)

    @property
    def last_updated_at_datetime(self) -> datetime:
        return datetime.fromisoformat(self.last_updated_at)

    @property
    def length_timedelta(self) -> timedelta:
        return timedelta(seconds=self.length)

    @classmethod
    def retrieve(cls, id: str) -> 'Subscription':
        def get_subscription() -> 'Subscription':
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.SUBSCRIPTIONS_BASE_URL}{constants.SUBSCRIPTIONS_RETRIEVE_SUBSCRIPTION}"
                .replace('<str:subscription_id>', id)
            )
            if api_response.status_code == 200:
                return cls(**api_response.json())
            raise Exception(f"Error retrieving subscription: {api_response.text}")
        return SUBSCRIPTION_CACHE.get(cache_key_name=f'subscription-{id}', specialized_fetch_function=get_subscription)

    @classmethod
    def retrieve_ids(cls, **filters: dict[str, any]) -> list[str]:
        ALLOWED_FILTERS: dict[str, type] = {"display_publicly": bool, "allow_more_subscriptions": bool, "owner_id": str}
        new_params: dict[str, str] = {}
        for param_key, param_value in filters.items():
            if param_key not in ALLOWED_FILTERS:
                raise ValueError(
                    f"Invalid filter parameter: {param_key}. Must be one of {list(ALLOWED_FILTERS.keys())}"
                )
            if not isinstance(param_value, ALLOWED_FILTERS[param_key]):
                raise TypeError(f"Invalid type for filter parameter: {param_key}. Must be {ALLOWED_FILTERS[param_key]}")
            new_params[param_key] = str(param_value)


        def get_subscriptions() -> list[str]:
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.SUBSCRIPTIONS_BASE_URL}{constants.SUBSCRIPTIONS_RETRIEVE_SUBSCRIPTIONS}",
                params=new_params
            )
            if api_response.status_code == 200:
                return api_response.json()
            raise Exception(f"Error retrieving subscription: {api_response.text}")
        return SUBSCRIPTION_CACHE.get(
            cache_key_name=f'subscriptions-{json.dumps(new_params)}', specialized_fetch_function=get_subscriptions
        )
