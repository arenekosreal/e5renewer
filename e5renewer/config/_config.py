import os
import socket
from typing import Self
from typing import Literal
from typing import ClassVar
from pathlib import Path
from typing_extensions import override
from e5renewer.config._base import BaseConfig
from e5renewer.config._user import User


_KeyType = Literal["listen_port", "listen_socket_permission"]
PORT_MIN = 0
PORT_MAX = 65535
PERMISSION_MIN = 0
PERMISSION_MAX = 777


class Config(BaseConfig):
    debug = False
    auth_token = ""
    users: ClassVar[list[User]] = []
    listen_addr = ""
    listen_port = 0
    listen_socket = Path("/run/e5renewer/e5renewer.socket")
    listen_socket_permission = 666

    @classmethod
    @override
    def from_json(cls, json: dict[str, str | int | list[dict[str, str]]]) -> Self:
        """Deserialize config from json dict.

        Args:
            json(dict[str,str | int | list[dict[str, str]]]]): the input json

        Returns:
            Config: The instance deserialized from json
        """
        instance = cls.__new__(cls)
        for key in dir(instance):
            if key in json:
                json_val = json[key]
                match key:
                    case "users":
                        if isinstance(json_val, list):
                            users: list[User] = []
                            for item in json_val:  # User in json
                                user = User.from_json(item)
                                if user not in users and user.is_valid:
                                    users.append(user)
                            setattr(instance, key, users)
                    case "listen_socket":
                        if isinstance(json_val, str):
                            path = Path(json_val)
                            if path.is_file():
                                setattr(instance, key, path)
                    case "listen_port" | "listen_socket_permission":

                        def extra_check(key: _KeyType, value: int) -> bool:
                            if key == "listen_port":
                                return PORT_MIN < value < PORT_MAX
                            return PERMISSION_MIN < value < PERMISSION_MAX

                        if isinstance(json_val, int) and extra_check(key, json_val):
                            setattr(instance, key, json_val)
                    case "auth_token" | "listen_addr" | "debug":
                        if isinstance(json_val, type(getattr(instance, key))):
                            setattr(instance, key, json_val)
                    case _:
                        pass
        return instance

    @property
    def _is_listen_valid(self) -> bool:
        if self.listen_addr:
            return self.listen_port != 0
        if hasattr(socket, "AF_UNIX"):
            return os.access(self.listen_socket.parent, os.W_OK)
        return False

    @property
    @override
    def is_valid(self) -> bool:
        return bool(self.auth_token) and self._is_listen_valid
