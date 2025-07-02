from typing import Any, Generic,  TypeVar, Union
from typing_extensions import TypeGuard

T = TypeVar("T",covariant=True)
E = TypeVar("E",bound=Exception, covariant=True)

class Ok(Generic[T]):
    def __init__(self, value: T):
        self._value = value

    def unwrap(self) -> T:
        return self._value
    
    def wrap(self) -> 'Result[T,Any]':
        return Result(self._value)


class Err(Generic[E]):
    def __init__(self, error: E):
        self._err = error

    def unwrap(self) -> E:
        return self._err
    
    def wrap(self) -> 'Result[Any,E]':
        return Result(self._err)

class Result(Generic[T,E]):
    def __init__(self, value: Union[T, E]):
        if isinstance(value, Exception):
            self._result = Err(value)
        else:
            self._result = Ok(value)

    def unwrap(self) -> Union[T, E]:
        if isinstance(self._result, Ok):
            return self._result.unwrap()
        else:
            raise self._result.unwrap()
    def get_result(self):
        return self._result
        
def is_ok(result: Result[T,E]) -> TypeGuard[Ok[T]]:
    r = result.get_result()
    p = isinstance(r, Ok)
    n = not isinstance(r, Err)
    return p and n

def is_err(result: Result[T,E]) -> TypeGuard[Err[E]]:
    r = result.get_result()
    p = isinstance(r, Err)
    n = not isinstance(r, Ok)
    return p and n