"""Singleton metaclass."""
from typing import Any, cast

class Singleton(type):
    """Singleton metaclass."""

    _instances = {}
    def __call__(cls: Any, *args: list[Any], **kwargs: dict[str, Any]):
        """Call method for the Singleton class.

        Returns:
            Any: Instance of the class
        """
        if cls not in cls._instances:
            cls._instances[cls] = cast(Any, super(Singleton, cls)).__call__(*args, **kwargs)
        return cls._instances[cls]