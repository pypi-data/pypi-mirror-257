"""Define applications with a dataclass-like interface."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Optional, Type

from typing_extensions import dataclass_transform

from numerous.utils import MISSING, ToolT


class HTML:
    def __init__(self, default: str) -> None:
        self.default = default


def html(  # type: ignore[no-untyped-def] # noqa: ANN201, PLR0913
    *,
    default: str = MISSING,  # type: ignore[assignment]
    default_factory: Callable[[], str] = MISSING,  # type: ignore[assignment] # noqa: ARG001
    init: bool = True,  # noqa: ARG001
    repr: bool = True,  # noqa: ARG001, A002
    hash: Optional[bool] = None,  # noqa: ARG001, A002
    compare: bool = True,  # noqa: ARG001
    metadata: Optional[MappingProxyType[str, Any]] = None,  # noqa: ARG001
    kw_only: bool = MISSING,  # type: ignore[assignment] # noqa: ARG001
):
    return HTML(default)


DEFAULT_FLOAT_MIN = 0.0
DEFAULT_FLOAT_MAX = 100.0


class Slider:
    def __init__(self, default: float, min_value: float, max_value: float) -> None:
        self.default = default
        self.min_value = min_value
        self.max_value = max_value


def slider(  # type: ignore[no-untyped-def] # noqa: ANN201, PLR0913
    *,
    default: float = MISSING,  # type: ignore[assignment]
    default_factory: Callable[[], float] = MISSING,  # type: ignore[assignment] # noqa: ARG001
    init: bool = True,  # noqa: ARG001
    repr: bool = True,  # noqa: ARG001, A002
    hash: Optional[bool] = None,  # noqa: ARG001, A002
    compare: bool = True,  # noqa: ARG001
    metadata: Optional[MappingProxyType[str, Any]] = None,  # noqa: ARG001
    kw_only: bool = MISSING,  # type: ignore[assignment] # noqa: ARG001
    min_value: float = DEFAULT_FLOAT_MIN,
    max_value: float = DEFAULT_FLOAT_MAX,
):
    return Slider(default=default, min_value=min_value, max_value=max_value)


@dataclass_transform(field_specifiers=(html,))
def app(cls: Type[ToolT]) -> Type[ToolT]:
    """Define an application."""
    cls.__numerous_app__ = True  # type: ignore[attr-defined]
    return dataclass(cls)


@dataclass_transform()
def container(cls: Type[ToolT]) -> Type[ToolT]:
    """Define a container."""
    cls.__container__ = True  # type: ignore[attr-defined]
    return dataclass(cls)


def action(action: Callable[[ToolT], Any]) -> Callable[[ToolT], Any]:
    """Define an action."""
    action.__action__ = True  # type: ignore[attr-defined]
    return action
