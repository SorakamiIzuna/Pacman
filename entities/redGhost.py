import heapq
import random
import pygame
from maze import MAZE_LAYOUT

class RedGhost:
    def __init__(self):
        self.image = pygame.image.load("assets/red.png")
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.x, self.y = self.get_random_position()
        self.path = []

    def get_random_position(self):
        empty_cells = []
        for row_index, row in enumerate(MAZE_LAYOUT):
            for col_index, cell in enumerate(row):
                if cell == '0':
                    empty_cells.append((col_index, row_index))
        return random.choice(empty_cells)

    def reset_position(self):
        self.x, self.y = self.get_random_position()
        self.path = []

    def find_path_to_pacman(self, target_x, target_y):
        frontier = []
        start = (self.x, self.y)
        heapq.heappush(frontier, (0, 0, start, []))
        visited = set()

        while frontier:
            priority, cost, (x, y), path = heapq.heappop(frontier)

            if (x, y) in visited:
                continue
            visited.add((x, y))
            new_path = path + [(x, y)]

            if (x, y) == (target_x, target_y):
                self.path = new_path
                return

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self.is_valid(nx, ny) and (nx, ny) not in visited:
                    new_cost = cost + 1
                    heuristic = abs(target_x - nx) + abs(target_y - ny)
                    heapq.heappush(frontier, (new_cost + heuristic, new_cost, (nx, ny), new_path))

        self.path = []

    def is_valid(self, x, y):
        return 0 <= y < len(MAZE_LAYOUT) and 0 <= x < len(MAZE_LAYOUT[0]) and MAZE_LAYOUT[y][x] == '0'

    def move_step(self):
        if self.path and len(self.path) > 1:
            self.path.pop(0)
            self.x, self.y = self.path[0]

    def draw(self, screen, tile_size, show_path=False):
        screen.blit(self.image, (self.x * tile_size, self.y * tile_size))
        if show_path:
            for px, py in self.path[1:]:
                pygame.draw.rect(screen, (255, 100, 100), (px * tile_size, py * tile_size, tile_size, tile_size), 1)
