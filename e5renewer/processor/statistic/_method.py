from typing import Any
from typing import TypeVar
from typing import Callable
from typing import Coroutine
from e5renewer.logger import debug


_known_methods: set[Callable[..., Coroutine[Any, Any, Any]]] = set()
_Func = TypeVar("_Func", bound="Callable[..., Coroutine[Any, Any, Any]]")


def register(function: _Func) -> _Func:
    if function not in _known_methods:
        _known_methods.add(function)
    return function


async def invoke(method: str, *args: Any, **kwargs: Any) -> Any:
    debug("Invoking method %s with args %s and kwargs %s", method, args, kwargs)
    for function in _known_methods:
        if function.__name__ == method:
            try:
                return await function(*args, **kwargs)
            except Exception:
                return None
    return None
