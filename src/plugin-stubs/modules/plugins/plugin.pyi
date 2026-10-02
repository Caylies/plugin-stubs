from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol

__all__ = ("Plugin", "get")

class _HookTarget(Protocol):
    hook_key: str

class Plugin:
    """
    A core component for accessing plugin hooks.

    Parameters
    ----------
    id: str
        A unique ID for the plugin.
    """

    id: str

    def __init__(self, id: str) -> None: ...
    def state(self, instance: object) -> dict:
        """
        Returns a per-plugin storage dictionary stored on `instance`, isolated from
        other plugins.

        Parameters
        ----------
        instance: object
            The object to store the state on.

        Returns
        -------
        dict
            A dictionary unique to this plugin's ID for the given `instance`.
            It is also returned on every call for the same `instance`.
        """
        ...

    def unload(self):
        """
        Unloads a plugin by removing every hook the plugin registered.
        """
        ...

    def before[F: Callable[..., Any]](self, target: _HookTarget) -> Callable[[F], F]:
        """
        Runs a function before the target method runs. Raise `Cancel(value)` to skip the method and return `value`.

        Parameters
        ----------
        target: _HookTarget
            The method to run the function before.

        Returns
        -------
        Callable[[F], F]
            A decorator that registers the function as a before-hook for the target and returns it.
        """
        ...

    def after[F: Callable[..., Any]](self, target: _HookTarget) -> Callable[[F], F]:
        """
        Runs a function after the target method runs. Return `Replace(value)` to change the result.

        Parameters
        ----------
        target: _HookTarget
            The method to run the function after.

        Returns
        -------
        Callable[[F], F]
            A decorator that registers the function as an after-hook for the target and returns it.
        """
        ...

def get(id: str) -> Plugin | None:
    """
    Looks up a registered plugin by ID. Useful for checking if a plugin is enabled.

    Parameters
    ----------
    id: str
        The ID of the plugin to look up.

    Returns
    -------
    Plugin | None
        The plugin registered under `id`, or `None` if no plugin with that ID is
        currently registered.
    """
    ...
