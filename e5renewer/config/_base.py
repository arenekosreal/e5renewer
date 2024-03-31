from e5renewer.defines import DeserializableObject


class BaseConfig(DeserializableObject):
    """Basic config class.

    **DO NOT** use __init__() to create instance, use from_json() instead.
    """

    def __init__(self) -> None:
        raise RuntimeError("Use BaseConfig.from_json() instead.")
