import json
from dataclasses import dataclass
from datetime import datetime
from requests import Response
from .. import constants
from ..http_requests import signed_requests
from ..utils.caching import CacheSystem


USER_SUBSCRIPTION_CACHE: CacheSystem = CacheSystem(default_expiry_time=60)


@dataclass
class UserSubscription:
    id: str
    user: str
    subscription: str
    created_at: str
    start_at: str
    expire_at: str

    @property
    def created_at_datetime(self) -> datetime:
        return datetime.fromisoformat(self.created_at)

    @property
    def start_at_datetime(self) -> datetime:
        return datetime.fromisoformat(self.start_at)

    def expire_at_datetime(self) -> datetime:
        return datetime.fromisoformat(self.expire_at)

    @classmethod
    def create(
            cls, user_id: str, subscription_id: str, start_at: datetime | None, expire_at: datetime | None = None
    ) -> 'UserSubscription':
        data_params: dict[str, any] = {"user_id": user_id, "subscription_id": subscription_id}
        if start_at:
            data_params["start_at"] = start_at.isoformat()
        if expire_at:
            data_params["expire_at"] = expire_at.isoformat()

        def create_user_subscription() -> 'UserSubscription':
            api_response: Response = signed_requests.request(
                method="POST",
                url=f"{constants.SUBSCRIPTIONS_BASE_URL}{constants.SUBSCRIPTIONS_CREATE_USER_SUBSCRIPTION}",
                json=data_params
            )
            if api_response.status_code == 201:
                return cls(**api_response.json())
            raise Exception(f"Error creating user subscription: {api_response.text}")
        return create_user_subscription()

    @classmethod
    def retrieve(cls, id: str) -> 'UserSubscription':
        def get_user_subscription() -> 'UserSubscription':
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.SUBSCRIPTIONS_BASE_URL}{constants.SUBSCRIPTIONS_RETRIEVE_USER_SUBSCRIPTION}"
                .replace('<str:user_subscription_id>', id)
            )
            if api_response.status_code == 200:
                return cls(**api_response.json())
            raise Exception(f"Error retrieving user subscription: {api_response.text}")

        return USER_SUBSCRIPTION_CACHE.get(
            cache_key_name=f'user_subscription-{id}', specialized_fetch_function=get_user_subscription
        )

    @classmethod
    def retrieve_ids(cls, **filters: dict[str, any]) -> list[str]:
        ALLOWED_FILTERS: dict[str, type] = {"user_id": str, "subscription_id": str, "is_active": bool}
        new_params: dict[str, str] = {}
        for param_key, param_value in filters.items():
            if param_key not in ALLOWED_FILTERS:
                raise ValueError(
                    f"Invalid filter parameter: {param_key}. Must be one of {list(ALLOWED_FILTERS.keys())}"
                )
            if not isinstance(param_value, ALLOWED_FILTERS[param_key]):
                raise TypeError(f"Invalid type for filter parameter: {param_key}. Must be {ALLOWED_FILTERS[param_key]}")
            new_params[param_key] = str(param_value)

        def get_user_subscriptions() -> list[str]:
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.SUBSCRIPTIONS_BASE_URL}{constants.SUBSCRIPTIONS_RETRIEVE_USER_SUBSCRIPTIONS}",
                params=new_params
            )
            if api_response.status_code == 200:
                return api_response.json()
            raise Exception(f"Error retrieving subscription: {api_response.text}")

        return USER_SUBSCRIPTION_CACHE.get(
            cache_key_name=f'user_subscriptions-{json.dumps(new_params)}',
            specialized_fetch_function=get_user_subscriptions
        )
