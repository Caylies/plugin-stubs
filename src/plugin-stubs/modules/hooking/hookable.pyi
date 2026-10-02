from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any, Concatenate, Protocol, overload

__all__ = ("hookable", "Cancel", "Replace", "Hookable", "HookableCoroutine")

class Replace:
    """
    Return `Replace` from an `after` hook to replace the method's result.

    Parameters
    ----------
    value: Any
        The value to replace the method's result with.
    """

    value: Any

    def __init__(self, value: Any): ...

class Cancel(Exception):
    """
    Raise `Cancel` from a `before` hook to skip the method and return `value` instead.

    Parameters
    ----------
    value: Any
        The value to return instead.
    """

    value: Any

    def __init__(self, value: Any = None): ...

class Hookable[**P, R](Protocol):
    """
    The type `hookable` returns for a sync function: callable like the original, plus the
    `hook_key` attribute.
    """

    hook_key: str

    def __call__(self, inst: Any, *args: P.args, **kwargs: P.kwargs) -> R: ...
    @overload
    def __get__(self, obj: None, objtype: type | None = None) -> Hookable[P, R]: ...
    @overload
    def __get__(self, obj: object, objtype: type | None = None) -> Callable[P, R]: ...

class HookableCoroutine[**P, R](Protocol):
    """
    The type `hookable` returns for an async function. Same as `Hookable`, but callable as a
    coroutine function.
    """

    hook_key: str

    def __call__(self, inst: Any, *args: P.args, **kwargs: P.kwargs) -> Coroutine[Any, Any, R]: ...
    @overload
    def __get__(self, obj: None, objtype: type | None = None) -> HookableCoroutine[P, R]: ...
    @overload
    def __get__(self, obj: object, objtype: type | None = None) -> Callable[P, Coroutine[Any, Any, R]]: ...

@overload
def hookable[**P, R](fn: Callable[Concatenate[Any, P], Coroutine[Any, Any, R]]) -> HookableCoroutine[P, R]: ...
@overload
def hookable[**P, R](fn: Callable[Concatenate[Any, P], R]) -> Hookable[P, R]: ...
def hookable[**P, R](
    fn: Callable[Concatenate[Any, P], Coroutine[Any, Any, R]] | Callable[Concatenate[Any, P], R],
) -> HookableCoroutine[P, R] | Hookable[P, R]:
    """
    Allows a function to be hooked onto.

    Parameters
    ----------
    fn: Callable[Concatenate[Any, P], R] | Callable[Concatenate[Any, P], Coroutine[Any, Any, R]]
        The function to mark as hookable.

    Returns
    -------
    Hookable[P, R] | HookableCoroutine[P, R]
        A wrapper around `fn` that takes the same parameters and returns the
        same type, and runs registered `before` and `after` hooks around every call.
    """
    ...
