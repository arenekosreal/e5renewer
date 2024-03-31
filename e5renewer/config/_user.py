import json
from typing import Any
from typing import Self
from datetime import time
from datetime import datetime
from typing_extensions import override
from e5renewer.config._base import BaseConfig


class User(BaseConfig):
    name = ""
    tenant_id = ""
    client_id = ""
    secret = ""
    from_time = time()
    to_time = time()

    @classmethod
    @override
    def from_json(cls, json: dict[str, str]) -> Self:
        """Deserialize config from json dict.

        Args:
            json(dict[str, str | list[int]]): the input json
        Returns:
            User: The instance deserialized from json
        """
        instance = cls.__new__(cls)
        for key in dir(instance):
            if key in json:
                match key:
                    case "name" | "tenant_id" | "client_id" | "secret":
                        json_val = json[key]
                        if isinstance(json_val, type(getattr(instance, key))):
                            setattr(instance, key, json_val)
                    case "from_time" | "to_time":
                        json_val = json[key]
                        try:
                            json_val = time.fromisoformat(json_val)
                        except ValueError:
                            pass
                        else:
                            setattr(instance, key, json_val)

                    case _:
                        pass
        return instance

    @property
    @override
    def is_valid(self) -> bool:
        return all([self.name, self.tenant_id, self.client_id, self.secret])

    @property
    def is_enabled(self) -> bool:
        now = datetime.now().time()
        return self.from_time <= now <= self.to_time

    @override
    def __eq__(self, __value: object) -> bool:
        if hasattr(__value, "__dict__"):
            for key in ["name", "tenant_id", "client_id", "secret"]:
                if getattr(__value, key) != getattr(self, key):
                    return False
            return True

        return super().__eq__(__value)

    @override
    def __hash__(self) -> int:
        return super().__hash__()

    @override
    def __str__(self) -> str:
        dict_to_return: dict[str, Any] = {}
        for key, item in self.__dict__.items():
            if key.startswith("_") or callable(item) or isinstance(item, time):
                continue
            dict_to_return[key] = item
        return json.dumps(dict_to_return, indent=self._indent, sort_keys=True)
