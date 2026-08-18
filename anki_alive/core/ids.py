from __future__ import annotations

from typing import Protocol
from uuid import UUID, uuid4


class IdFactory(Protocol):
    def new(self) -> UUID:
        ...


class Uuid4Factory:
    def new(self) -> UUID:
        return uuid4()
