import heapq
import random
import pygame
from maze import MAZE_LAYOUT,TILE_SIZE

class OrangeGhost:
    def __init__(self, pacman_pos):
        self.image = pygame.image.load("assets/orange.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.x, self.y = self.get_random_position(pacman_pos)
        self.start_position = (self.x, self.y)
        self.path = []

    def get_random_position(self, pacman_pos):
        empty_cells = []
        restricted_rows = {10, 11, 12, 16, 17, 18}
        restricted_cols_start = set(range(5))
        restricted_cols_end = set(range(22, 28))

        for row_index, row in enumerate(MAZE_LAYOUT):
            for col_index, cell in enumerate(row):
                if cell == '0':
                    if row_index in restricted_rows:
                        if col_index in restricted_cols_start or col_index in restricted_cols_end:
                            continue
                    if (col_index, row_index) != pacman_pos:
                        empty_cells.append((col_index, row_index))
        return random.choice(empty_cells) if empty_cells else (0, 0)

    def reset_position(self, pacman_pos):
        self.x, self.y = self.get_random_position(pacman_pos)
        self.start_position = (self.x, self.y)
        self.path = []

    def restore_start_position(self):
        self.x, self.y = self.start_position
        self.path = []

    def find_path_to_pacman(self, target_x, target_y):
        frontier = []
        heapq.heappush(frontier, (0, (self.x, self.y), []))
        visited = set()

        while frontier:
            cost, (x, y), path = heapq.heappop(frontier)

            if (x, y) in visited:
                continue
            visited.add((x, y))
            new_path = path + [(x, y)]

            if (x, y) == (target_x, target_y):
                self.path = new_path
                return

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if y == 14:
                if x == 0:
                    directions.append((-1, 0))
                if x == 27:
                    directions.append((1, 0))

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if y == 14:
                    if x == 0 and dx == -1:
                        nx = 27
                    elif x == 27 and dx == 1:
                        nx = 0
                if self.is_valid(nx, ny) and (nx, ny) not in visited:
                    heapq.heappush(frontier, (cost + 1, (nx, ny), new_path))

        self.path = []

    def is_valid(self, x, y):
        if y == 14 and (x == -1 or x == 28):
            return True
        return 0 <= y < len(MAZE_LAYOUT) and 0 <= x < len(MAZE_LAYOUT[0]) and MAZE_LAYOUT[y][x] == '0'

    def move_step(self):
        if self.path and len(self.path) > 1:
            self.path.pop(0)
            next_x, next_y = self.path[0]
            if next_y == 14:
                if next_x == -1:
                    next_x = 27
                elif next_x == 28:
                    next_x = 0
            self.x, self.y = next_x, next_y

    def draw(self, screen, tile_size):
        screen.blit(self.image, (self.x * tile_size, self.y * tile_size))
        for px, py in self.path[1:]:
            pygame.draw.rect(screen, (255, 215, 0), (px * tile_size, py * tile_size, tile_size, tile_size), 1)