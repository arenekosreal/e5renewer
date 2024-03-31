import random
from e5renewer.defines import AUTHOR
from typing_extensions import override
from e5renewer.processor.statistic import set_api_call_result
from e5renewer.processor.msapis._caller import APICaller
from e5renewer.processor.msapis._caller import caller


@caller
class RandomAPICaller(APICaller):
    @property
    @override
    def name(self) -> str:
        return "Random API caller"

    @property
    @override
    def author(self) -> str:
        return AUTHOR

    @override
    async def call_next_api(self, update: bool = True):
        api = random.choice(list(self.apis.keys()))
        result = await self.apis[api](self._client)
        if update:
            set_api_call_result(self.user_name, api, str(result))
