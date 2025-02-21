from enum import Enum


class TrafficLight(Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


CYCLE = [TrafficLight.RED, TrafficLight.GREEN, TrafficLight.YELLOW]


def update_car_for_light(current: TrafficLight, car):
    if current == TrafficLight.RED:
        car.stop()
    else:
        car.drive()
