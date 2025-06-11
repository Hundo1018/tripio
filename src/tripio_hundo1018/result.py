from typing import Generic, TypeVar, Union
from typing_extensions import TypeGuard, TypeAlias

T = TypeVar("T")


class Ok(Generic[T]):
    def __init__(self, value: T):
        self._value = value

    def unwrap(self) -> T:
        return self._value


class Err:
    def __init__(self, error: Exception):
        self._err = error

    def unwrap(self) -> Exception:
        return self._err

Result:TypeAlias = Union[Ok[T], Err]


def is_ok(result: Result[T]) -> TypeGuard[Ok[T]]:
    return isinstance(result, Ok)


def is_err(result: Result[T]) -> TypeGuard[Err]:
    return isinstance(result, Err)


def get_result(b: bool) -> 'Result[int]':
    if b:
        return Ok(3)
    else:
        return Err(Exception('err'))
