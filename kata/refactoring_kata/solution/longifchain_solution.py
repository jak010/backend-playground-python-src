"""
    1. elif는 extract-method Action을 이용해 Method로 뽑아낸다.
    2. Tile(Enum)을 Interface 로 변경한다.

"""

from abc import ABCMeta, abstractmethod
from typing import List

TILE_SIZE = 32


class RawTile:
    FLUX = 1
    UNBREAKABLE = 2
    STONE = 3
    FALLING_STONE = 4
    BOX = 5
    FALLING_BOX = 6
    KEY1 = 7
    LOCK1 = 8
    KEY2 = 9
    LOCK2 = 10
    AIR = 11
    PLAYER = 12


class Tile2(metaclass=ABCMeta):

    @abstractmethod
    def is_flux(self) -> bool: ...

    @abstractmethod
    def is_unbreakable(self) -> bool: ...

    @abstractmethod
    def is_stone(self) -> bool: ...

    @abstractmethod
    def is_falling_stone(self) -> bool: ...

    @abstractmethod
    def is_box(self) -> bool: ...

    @abstractmethod
    def is_falling_box(self) -> bool: ...

    @abstractmethod
    def is_key1(self) -> bool: ...

    @abstractmethod
    def is_lock1(self) -> bool: ...

    def is_air(self):
        pass

    def is_player(self):
        pass


map_data: List[List[Tile2]] = [
    []
]


def draw_map(ax):
    for y in range(len(map_data)):
        for x in range(len(map_data[y])):
            # JavaScript의 map[y][x]와 동일하게 접근
            color_of_tile(x, y)

            if map_data[y][x].is_air() or map_data[y][x].is_player():
                print((x * TILE_SIZE, y * TILE_SIZE), TILE_SIZE, TILE_SIZE, )


def color_of_tile(x, y):
    if map_data[y][x].is_flux():
        color = "#ccffcc"
    elif map_data[y][x].is_unbreakable():
        color = "#999999"
    elif map_data[y][x].is_stone():
        color = "#0000cc"
    elif map_data[y][x].is_falling_stone():
        color = "#8b4513"
    elif map_data[y][x].is_lock1() or map_data[y][x].is_key1():
        color = "#ffcc00"
    elif map_data[y][x].is_lock2() or map_data[y][x].is_key2():
        color = "#00ccff"
