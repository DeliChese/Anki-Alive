from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, DefaultDict, TypeVar

EventT = TypeVar("EventT")
Handler = Callable[[Any], None]


@dataclass(frozen=True)
class Subscription:
    event_type: type[Any]
    handler: Handler


class EventBus:
    """Small synchronous in-process event bus for Phase 0.

    The bus is intentionally boring: explicit subscriptions, deterministic
    delivery order, and no hidden threading or retries.
    """

    def __init__(self) -> None:
        self._handlers: DefaultDict[type[Any], list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: type[EventT], handler: Callable[[EventT], None]) -> Subscription:
        handlers = self._handlers[event_type]
        if handler not in handlers:
            handlers.append(handler)
        return Subscription(event_type=event_type, handler=handler)

    def unsubscribe(self, subscription: Subscription) -> None:
        handlers = self._handlers.get(subscription.event_type)
        if not handlers:
            return
        try:
            handlers.remove(subscription.handler)
        except ValueError:
            return
        if not handlers:
            self._handlers.pop(subscription.event_type, None)

    def publish(self, event: EventT) -> None:
        for handler in tuple(self._handlers.get(type(event), ())):
            handler(event)
