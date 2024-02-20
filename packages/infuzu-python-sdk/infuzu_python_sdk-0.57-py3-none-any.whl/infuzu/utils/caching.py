import time
from typing import Callable


class CacheSystem:
    def __init__(self, default_fetch_function: Callable = None, default_expiry_time: int = 300) -> None:
        self.cache: dict[str, dict[str, any]] = {}
        self.default_fetch_function: Callable = default_fetch_function
        self.default_expiry_time: int = default_expiry_time

    def get(
            self,
            *args,
            cache_key_name: str,
            specialized_fetch_function: Callable = None,
            specialized_expiry_time: int = None,
            **kwargs
    ) -> any:
        self.cleanup()
        current_time: int = int(time.time())
        if cache_key_name in self.cache and self.cache[cache_key_name]['expiry_time'] > current_time:
            return self.cache[cache_key_name]['data']
        func: Callable = specialized_fetch_function or self.default_fetch_function
        data: any = func(*args, **kwargs)
        self.cache[cache_key_name] = {
            'data': data, 'expiry_time': current_time + (specialized_expiry_time or self.default_expiry_time)
        }
        return data

    def cleanup(self) -> None:
        current_time: int = int(time.time())
        keys_to_delete: list[str] = [key for key, value in self.cache.items() if value['expiry_time'] <= current_time]
        if keys_to_delete:
            for key in keys_to_delete:
                del self.cache[key]
