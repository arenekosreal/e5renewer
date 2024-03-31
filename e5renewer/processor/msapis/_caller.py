from abc import abstractmethod
from typing import Any
from typing import TypeVar
from typing import Callable
from typing import Coroutine
from typing import NamedTuple
from msgraph import GraphServiceClient
from e5renewer.sdk import Module
from e5renewer.sdk import module

# TODO: Use async version when AttributeError is fixed
# ClientSecretCredential.get_token failed: 'NoneType' object has no attribute '__aenter__'
from azure.identity import ClientSecretCredential
from e5renewer.config import User
from e5renewer.logger import debug
from typing_extensions import override
from e5renewer.processor.statistic._method import register
from msgraph.generated.models.o_data_errors.o_data_error import ODataError


class APIResult(NamedTuple):
    _CONNETOR = " - "
    code: int
    msg: str
    raw_result: Any

    @override
    def __str__(self) -> str:
        return self._CONNETOR.join([str(self.code), self.msg])


class APICaller(Module):
    def __init__(self, user: User) -> None:
        credential = ClientSecretCredential(user.tenant_id, user.client_id, user.secret)
        self._client = GraphServiceClient(credentials=credential)
        self.apis = _known_apis
        self.user_name = user.name

    @abstractmethod
    async def call_next_api(self, update: bool = True): ...

    @override
    def __eq__(self, __value: object) -> bool:
        if hasattr(__value, "user_name"):
            return self.user_name == getattr(__value, "user_name")
        return super().__eq__(__value)

    @override
    def __hash__(self) -> int:
        return hash(self.user_name)


_T = TypeVar("_T", bound="APICaller")
_InputAPIFunction = Callable[[GraphServiceClient], Coroutine[Any, Any, Any]]
APIFunction = Callable[[GraphServiceClient], Coroutine[Any, Any, APIResult]]


_known_callers: set[type[APICaller]] = set()
_known_apis: dict[str, APIFunction] = {}


def caller(caller: type[_T]) -> type[_T]:
    if caller not in _known_callers:
        caller = module()(caller)
        _known_callers.add(caller)
    return caller


def api(name: str) -> Callable[[_InputAPIFunction], APIFunction]:
    def api_wrapper(function: _InputAPIFunction) -> APIFunction:
        async def invoke(client: GraphServiceClient) -> APIResult:
            debug("Calling API %s....", name)
            try:
                result = await function(client)
            except ODataError as err:
                api_result = APIResult(
                    err.response_status_code if err.response_status_code else -1,
                    err.error.code if err.error and err.error.code else "ERROR",
                    None,
                )
            except Exception as err:
                debug("Failed to send http request because %s", str(err))
                api_result = APIResult(-1, "ERROR", None)
            else:
                debug("result is %s", str(result))
                api_result = APIResult(200, "OK", result)
            return api_result

        if name not in _known_apis:
            _known_apis[name] = invoke
        return _known_apis[name]

    return api_wrapper


@register
async def get_list_apis() -> list[str]:
    return list(_known_apis.keys())
