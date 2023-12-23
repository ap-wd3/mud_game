import sys
from map import Map, paths

m = Map(3, 6, 0, 1, paths)

while True:
    m.print_map()
    direction = input("What direction do you want to move? [n/e/s/w] ")
    m.move(direction)