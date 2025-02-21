from abc import ABCMeta, abstractmethod


class TrafficLight2(metaclass=ABCMeta):

    @abstractmethod
    def is_red(self) -> bool: ...

    @abstractmethod
    def is_yellow(self) -> bool: ...

    @abstractmethod
    def is_green(self) -> bool: ...


class Red(TrafficLight2):
    def is_red(self) -> bool:
        return True

    def is_yellow(self) -> bool:
        return False

    def is_green(self) -> bool:
        return False


class Yellow(TrafficLight2):
    def is_red(self) -> bool:
        return False

    def is_yellow(self) -> bool:
        return True

    def is_green(self) -> bool:
        return False


class Green(TrafficLight2):
    def is_red(self) -> bool:
        return False

    def is_yellow(self) -> bool:
        return False

    def is_green(self) -> bool:
        return True


CYCLE = [Red(), Green(), Yellow()]


def update_car_for_light2(current: TrafficLight2, car):
    if current.is_red():
        car.stop()
    else:
        car.drive()
