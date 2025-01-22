from random import random, randint
from typing import List, Tuple
from core.node import Node

class Coordinates():
    start: Node
    walls: List[Tuple[int, int]]
    maze: List[List[int]]
    open_list: List[Node]
    closed_list: List[Node]
    current_node: Node | None
    start_point: Tuple[int, int] | None


    def __init__(self):
        self.clear_all_field()


    def clear_all_field(self):
        self.start = None
        self.walls = []
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.current_node = None
        self.start_point = None


    def clear_cut(self):
        self.maze = []
        self.open_list = []
        self.closed_list = []


    def largest_distance(self):
        largest = 0

        for wall in self.walls:
            if wall[0] > largest:
                largest = wall[0]

            if wall[1] > largest:
                largest = wall[1]

        if self.start_point[0] > largest:
            largest = self.start_point[0]
        if self.start_point[1] > largest:
                largest = self.start_point[1]

        return largest + 1


    def create_maze(self, gui):
        largest = self.largest_distance()

        if gui.grid_size > largest:
            largest = gui.grid_size

        self.maze = [[0 for x in range(largest)] for y in range(largest)]
        for wall in self.walls:
            try:
                wall_x, wall_y = wall
                self.maze[wall_x][wall_y] = 1
            except:
                pass


    def generate_random_obstacles(self, gui):
        self.walls = []
        for _ in range(gui.grid_size*gui.grid_size):
            if random() > 0.6:
                wall = (randint(0, gui.grid_size-1),
                        randint(0, gui.grid_size-1))
                if wall not in self.walls:
                    self.walls.append(wall)
