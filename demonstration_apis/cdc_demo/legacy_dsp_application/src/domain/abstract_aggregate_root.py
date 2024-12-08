from typing import Generic, TypeVar, List
from .event import DomainEvent

T = TypeVar("T")


class AbstactAggregateRoot(Generic[T]):
    events: List[DomainEvent] = []

    def register_event(self, model: DomainEvent):
        self.events.append(model)

    def clear_events(self):
        self.events = []

    def domain_events(self):
        return self.events
