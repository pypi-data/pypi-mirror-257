from typing import Optional, TypeVar

T = TypeVar("T")


def unwrap(val: Optional[T]) -> T:
    """
    Unwrap a value from an Optional
    """
    if val is None:
        raise ValueError("Value is None")
    return val
