from typing import List

from dependency_injector.wiring import Provide

from config import container
from config.broker import MessageQueuePublisher
from src.domain.event import DomainEvent

from src.application.events.message import DomainMessage


class LegacyDomainEventListener:
    events: List[DomainEvent] = Provide[container.EventContainer.event_store]

    # BINDING_NAME = "legacy-rabbit-out"
    # OUTPUT_BINDING , 어디로(RabbitMq, Redis, Kafaka) Event를 보낼것인가

    message_publisher = MessageQueuePublisher()

    @classmethod
    def handle_event(cls):
        for event in cls.events:
            cls.message_publisher.send(
                message=DomainMessage.of(
                    aggregate_id=event.aggregate_id(),
                    aggregate_type=event.aggregate_type().value,
                    occred_on=event.occured_on().isoformat(),
                    owner_id=event.ower_id()
                )
            )
            cls.events.remove(event)
