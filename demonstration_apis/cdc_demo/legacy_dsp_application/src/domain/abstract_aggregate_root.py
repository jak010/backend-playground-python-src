from typing import Generic, TypeVar, List
from .event import DomainEvent

from dependency_injector.wiring import Provide
from config import container

T = TypeVar("T")


class AbstactAggregateRoot(Generic[T]):
    events: List[DomainEvent] = Provide[container.EventContainer.event_store]

    @classmethod
    def register_event(cls, model: DomainEvent):
        cls.events.append(model)

    @classmethod
    def clear_events(cls):
        cls.events = []

    @classmethod
    def domain_events(cls):
        return cls.events
