from typing import NoReturn
from abc import ABCMeta, abstractmethod


class Car:
    def stop(self): ...

    def drive(self): ...


car = Car()


class TrafficLight2(metaclass=ABCMeta):

    @abstractmethod
    def is_red(self) -> bool: ...

    @abstractmethod
    def is_yellow(self) -> bool: ...

    @abstractmethod
    def is_green(self) -> bool: ...

    @abstractmethod
    def update_car(self) -> NoReturn: ...


class Red(TrafficLight2):
    def is_red(self) -> bool:
        return True

    def is_yellow(self) -> bool:
        return False

    def is_green(self) -> bool:
        return False

    def update_car(self):
        car.stop()


class Yellow(TrafficLight2):
    def is_red(self) -> bool:
        return False

    def is_yellow(self) -> bool:
        return True

    def is_green(self) -> bool:
        return False

    def update_car(self):
        car.drive()


class Green(TrafficLight2):
    def is_red(self) -> bool:
        return False

    def is_yellow(self) -> bool:
        return False

    def is_green(self) -> bool:
        return True

    def update_car(self):
        car.drive()


CYCLE = [Red(), Green(), Yellow()]


def update_car_for_light2(current: TrafficLight2):
    current.update_car()
