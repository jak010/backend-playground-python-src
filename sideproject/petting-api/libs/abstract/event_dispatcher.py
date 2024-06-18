import queue
from abc import ABCMeta, abstractmethod


class AbstractEvent(metaclass=ABCMeta):
    REASEON: str = ""

    @abstractmethod
    def publish(self, *args, **kwargs): ...


class EventHandler:

    def __init__(self):
        self.events: queue.Queue = queue.Queue()

    def add_event(self, event: AbstractEvent):
        self.events.put(event)

    def emit(self):
        while not self.events.empty():
            event = self.events.get()
            event.publish()
