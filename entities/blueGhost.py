import random
from collections import deque
import pygame
from maze import MAZE_LAYOUT, TILE_SIZE
import os
from config import ASSET_DIR
class BlueGhost:
    def __init__(self, pacman_pos):
        self.image = pygame.image.load(os.path.join(ASSET_DIR, "blue.png"))
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.x, self.y = self.get_random_position(pacman_pos)
        self.start_position = (self.x, self.y)
        self.path = []
        self.nodes=0

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

    def find_path_to_pacman(self, target_x, target_y, forbidden_cells=None):
        if forbidden_cells is None:
            forbidden_cells = set()
        visited = set()
        parent_map = {}
        queue = deque([(self.x, self.y)])
        visited.add((self.x, self.y))

        while queue:
            current_x, current_y = queue.popleft()

            if (current_x, current_y) == (target_x, target_y):
                self.path = []
                while (current_x, current_y) != (self.x, self.y):
                    self.path.append((current_x, current_y))
                    current_x, current_y = parent_map[(current_x, current_y)]
                self.path.append((self.x, self.y))
                self.path.reverse()
                return

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if current_y == 14:
                if current_x == 0:
                    directions.append((-1, 0))
                if current_x == 27:
                    directions.append((1, 0))

            for dx, dy in directions:
                next_x, next_y = current_x + dx, current_y + dy
                if current_y == 14:
                    if current_x == 0 and dx == -1:
                        next_x = 27
                    elif current_x == 27 and dx == 1:
                        next_x = 0
                if (self.is_valid(next_x, next_y) and 
                    (next_x, next_y) not in visited and 
                    ((next_x, next_y) not in forbidden_cells or (next_x, next_y) == (target_x, target_y))):
                    visited.add((next_x, next_y))
                    parent_map[(next_x, next_y)] = (current_x, current_y)
                    queue.append((next_x, next_y))
            self.nodes += 1 
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
            pygame.draw.rect(screen, (173, 216, 230), (px * tile_size, py * tile_size, tile_size, tile_size), 1)
    def getNodes(self):
        return self.nodes
    def getLocation(self):
        return self.x, self.y
