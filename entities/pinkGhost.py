import random
import pygame
from maze import MAZE_LAYOUT,TILE_SIZE
import os
from config import ASSET_DIR
class PinkGhost:
    def __init__(self, pacman_pos):
        self.image = pygame.image.load(os.path.join(ASSET_DIR, "pink.png"))
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

    def find_path_to_pacman(self, target_x, target_y, forbidden_cells=None):
        if forbidden_cells is None:
            forbidden_cells = set()
        visited = set()
        path = []

        def dfs(x, y):
            if (x, y) == (target_x, target_y):
                path.append((x, y))
                return True
            if (x, y) in visited or not self.is_valid(x, y) or ((x, y) in forbidden_cells and (x, y) != (target_x, target_y)):
                return False
            visited.add((x, y))
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if y == 14:
                if x == 0:
                    directions.append((-1, 0))
                if x == 27:
                    directions.append((1, 0))
            for dx, dy in directions:
                next_x, next_y = x + dx, y + dy
                if y == 14:
                    if x == 0 and dx == -1:
                        next_x = 27
                    elif x == 27 and dx == 1:
                        next_x = 0
                if dfs(next_x, next_y):
                    path.append((x, y))
                    return True
            return False

        if dfs(self.x, self.y):
            self.path = path[::-1]
        else:
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
            pygame.draw.rect(screen, (255, 182, 193), (px * tile_size, py * tile_size, tile_size, tile_size), 1)