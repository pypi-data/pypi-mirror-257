import asyncio as _asyncio
import inspect as _inspect
import time as _time
from math import floor as _floor
from functools import wraps as _wraps


SLEEP_TIME = 0.05
_sliding_window_target = lambda window, limit, n_tests: (window / limit) * n_tests
_token_bucket_target = lambda capacity, fill_rate, n_tests: (capacity / fill_rate * (n_tests - capacity))
_leaky_bucket_target = lambda capacity, fill_rate, n_tests: (n_tests - capacity) / fill_rate
_gcra_target = lambda period, limit, n_tests: (n_tests - (capacity := _floor(limit / period))) * period + (limit if n_tests <= capacity else 0)



class _Ratelimit:
    __slots__ = ("_cache")

    def __init__(self):
        self._cache = {}


    def increment(self):
        while not self.ok():
            _time.sleep(SLEEP_TIME)


    async def increment_async(self):
        while not self.ok():
            await _asyncio.sleep(SLEEP_TIME)


class _RatelimitDecorator:
    def __call__(self, func):
        if _inspect.iscoroutinefunction(func):
            @_wraps(func)
            async def wrapper(*args, **kwargs):
                await self.increment_async()
                return await func(*args, **kwargs)
        else:
            @_wraps(func)
            def wrapper(*args, **kwargs):
                self.increment()
                return func(*args, **kwargs)
        return wrapper


class TokenBucketRatelimiter(_Ratelimit):
    __slots__ = ("capacity", "tokens", "fill_rate", "last_check")

    def __init__(self, capacity=10, fill_rate=1, *args, **kwargs):
        super().__init__()
        self.capacity = capacity
        self.fill_rate = fill_rate
        self.tokens = capacity
        self.last_check = _time.time()


    def get_tokens(self):
        # Calculate the _time elapsed since the last fill
        current = _time.time()
        elapsed = current - self.last_check

        # Calculate the number of tokens to add based on the fill rate
        to_add = elapsed * (self.fill_rate / self.capacity)

        # Set the new number of tokens (up to capacity)
        self.tokens = min(self.capacity, self.tokens + to_add)
        self.last_check = current


    def ok(self):
        self.get_tokens()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


# The `LeakyBucketRateLimiter` class is a decorator that implements a rate limit for a given function
# using the leaky bucket algorithm.
class LeakyBucketRatelimiter(_Ratelimit):
    __slots__ = ("capacity", "leak_rate", "content", "last_checked")

    def __init__(self, capacity=10, leak_rate=5, *args, **kwargs):
        super().__init__()
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.content = 0
        self.last_checked = _time.time()


    def _leak(self):
        # Calculate the amount of time that has passed
        current_time = _time.time()
        elapsed = current_time - self.last_checked
        self.last_checked = current_time

        # Leak the appropriate amount of requests
        self.content -= elapsed * self.leak_rate
        self.content = max(self.content, 0)


    def ok(self):
        self._leak()
        if self.content < self.capacity:
            self.content += 1
            return True
        return False


class SlidingWindowRatelimiter(_Ratelimit):
    __slots__ = ("limit", "window", "cur_time", "pre_count", "cur_count")

    def __init__(self, limit=10, window=1, *args, **kwargs):
        super().__init__()
        self.limit = limit
        self.window = window
        self.cur_time = _time.time()
        self.pre_count = limit
        self.cur_count = 0


    def ok(self):
        if ((time := _time.time()) - self.cur_time) > self.window:
            self.cur_time = time
            self.pre_count = self.cur_count
            self.cur_count = 0
        ec = (self.pre_count * (self.window - (_time.time() - self.cur_time)) / self.window) + self.cur_count
        if ec < self.limit:
            self.cur_count += 1
            return True
        return False


class FixedWindowRatelimiter(_Ratelimit):
    __slots__ = ("limit", "window", "requests", "current_time", "window_start")

    def __init__(self, limit=10, window=10, *args, **kwargs):
        super().__init__()
        self.window = window
        self.limit = limit
        self.requests = 0
        self.window_start = _time.time()


    def ok(self):
        current_time = _time.time()
        if current_time - self.window_start > self.window:
            self.requests = 0
            self.window_start = current_time

        if self.requests < self.limit:
            self.requests += 1
            return True
        return False


# The `GCRARatelimiter` class is a decorator that limits the rate at which a function can be called
# based on a specified rate and burst size.
class GCRARatelimiter(_Ratelimit):
    __slots__ = ("period", "limit", "last_time")

    def __init__(self, period, limit):
        super().__init__()
        self.period = period  # Time period for each cell/token (in seconds)
        self.limit = limit  # Limit on the burst size (in seconds)
        self.last_time = None  # Time of the last conforming cell/token


    def ok(self):
        current_time = _time.time()
        expected_time = self.last_time + self.period if self.last_time else current_time

        if current_time < expected_time - self.limit:
            # The cell/token arrives too early and does not conform.
            return False
        else:
            # The cell/token conforms; update the last_time.
            self.last_time = max(expected_time, current_time)
            return True


class leakybucket(LeakyBucketRatelimiter, _RatelimitDecorator):
    pass

class tokenbucket(TokenBucketRatelimiter, _RatelimitDecorator):
    pass

class slidingwindow(SlidingWindowRatelimiter, _RatelimitDecorator):
    pass

class fixedwindow(FixedWindowRatelimiter, _RatelimitDecorator):
    pass

class gcra(GCRARatelimiter, _RatelimitDecorator):
    pass


_TYPES = {
    "leakybucket": leakybucket,
    "tokenbucket": tokenbucket,
    "slidingwindow": slidingwindow,
    "fixedwindow": fixedwindow,
    "gcra": gcra,
}


class ratelimit:
    def __new__(cls, type="slidingwindow", *args, **kwargs):
        '''The function creates a new instance of a class based on the specified type and initializes it with
        the given arguments.

        Parameters
        ----------
        cls
            The `cls` parameter is a reference to the class itself. It is automatically passed as the first
        parameter to the `__new__` method when creating a new instance of the class.
        type, optional
            The `type` parameter is a string that specifies the type of object to create. It is used to
        determine the class to instantiate based on the value of the `type` parameter. The value of the
        `type` parameter is converted to lowercase before determining the class to instantiate.

        Returns
        -------
            The instance of the class that is created.

        '''
        type = _TYPES[type.lower()]
        instance = type.__new__(type)
        instance.__init__(*args, **kwargs)
        return instance