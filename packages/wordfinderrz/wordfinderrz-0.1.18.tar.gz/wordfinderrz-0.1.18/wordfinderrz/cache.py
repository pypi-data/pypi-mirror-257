from __future__ import annotations

from collections import OrderedDict, deque
from collections.abc import Callable, Hashable, Iterable
from functools import update_wrapper
from typing import Generic, ParamSpec, SupportsIndex, TypeVar, cast, overload

P = ParamSpec("P")
T = TypeVar("T")


class _SENTINEL: ...


class CachedFunction(Generic[P, T]):
    """LRU cache for functions with hashable parameters."""

    def __init__(
        self,
        func: Callable[P, T],
        /,
        maxsize: int | None = 128,
        typed: bool = False,
    ) -> None:
        self.func: Callable[P, T] = func
        self.cache: OrderedDict[Hashable, T] = OrderedDict()
        self.hits = self.misses = 0
        self.maxsize = maxsize
        self.typed = typed
        update_wrapper(self, func)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        key = CachedFunction._make_key(args, kwargs, self.typed)
        cached_result = self._cache_get(key)
        if cached_result is _SENTINEL:
            self.misses += 1
            result = self.func(*args, **kwargs)
            self.cache[key] = result
            if self.maxsize is not None and len(self.cache) > self.maxsize:
                self.cache.popitem(last=False)
            return result
        else:
            self.hits += 1
            return cast(T, cached_result)

    def _cache_get(self, key: Hashable) -> T | type[_SENTINEL]:
        return self.cache.get(key, _SENTINEL)

    @staticmethod
    def _make_key(
        args: tuple[Hashable, ...], kwargs: dict[str, Hashable], typed: bool
    ) -> Hashable:
        result = *args, _SENTINEL, *kwargs.items()
        if typed:
            result += (
                _SENTINEL,
                *(type(arg) for arg in args),
                _SENTINEL,
                *((k, type(v)) for k, v in kwargs.items()),
            )
        return result


@overload
def lru_cache(
    func: Callable[P, T],
    /,
    maxsize: int | None = 128,
    typed: bool = False,
) -> CachedFunction[P, T]: ...


@overload
def lru_cache(
    func: None = None,
    /,
    maxsize: int | None = 128,
    typed: bool = False,
) -> Callable[[Callable[P, T]], CachedFunction[P, T]]: ...


def lru_cache(
    func: Callable[P, T] | None = None,
    /,
    maxsize: int | None = 128,
    typed: bool = False,
) -> CachedFunction[P, T] | Callable[[Callable[P, T]], CachedFunction[P, T]]:
    """LRU cache for functions with hashable parameters."""
    if func is None:
        return lambda fn: CachedFunction(fn, maxsize=maxsize, typed=typed)
    return CachedFunction(func, maxsize, typed)


def cache(func: Callable[P, T]) -> CachedFunction[P, T]:
    """Cache for functions with hashable parameters."""
    return CachedFunction(func, maxsize=None, typed=False)


class LruQueue(Generic[T]):
    """Appends items left, truncates at max_size."""

    def __init__(self, max_size: int) -> None:
        self.max_size = max_size
        self.data: deque[T] = deque()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{str(self.data).replace('deque', '')}"

    def __getitem__(self, idx: SupportsIndex) -> T:
        return self.data[idx]

    def append(self, item: T) -> None:
        self.data.appendleft(item)
        if len(self.data) > self.max_size:
            self.data.pop()

    def extend(self, items: Iterable[T]) -> None:
        for item in items:
            self.append(item)
