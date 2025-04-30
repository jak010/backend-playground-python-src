"""
    Q. elif (else if) 가 길게 늘어진 코드는 어떻게 리팩터링 할 수 있을까 ?
"""
TILE_SIZE = 32
map_data = [
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 3, 0, 1, 1, 2, 0, 2],
    [2, 4, 2, 6, 1, 2, 0, 2],
    [2, 8, 4, 1, 1, 2, 0, 2],
    [2, 4, 1, 1, 1, 9, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2],
]


class Tile:
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


def draw_map(ax):
    for y in range(len(map_data)):
        for x in range(len(map_data[y])):
            # JavaScript의 map[y][x]와 동일하게 접근
            if map_data[y][x] == Tile.FLUX:
                color = "#ccffcc"
            elif map_data[y][x] == Tile.UNBREAKABLE:
                color = "#999999"
            elif map_data[y][x] == Tile.STONE or map_data[y][x] == Tile.FALLING_STONE:
                color = "#0000cc"
            elif map_data[y][x] == Tile.FALLING_BOX:
                color = "#8b4513"
            elif map_data[y][x] == Tile.LOCK1:
                color = "#ffcc00"
            elif map_data[y][x] == Tile.KEY2:
                color = "#00ccff"
            else:
                # AIR 또는 다른 값은 그리지 않음
                continue

            if map_data[y][x] != Tile.AIR or map_data[y][x] != Tile.PLAYER:
                print((x * TILE_SIZE, y * TILE_SIZE), TILE_SIZE, TILE_SIZE, )
