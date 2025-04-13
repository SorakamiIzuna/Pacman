import random
import pygame
from maze import MAZE_LAYOUT

class PinkGhost:
    def __init__(self):
        self.image = pygame.image.load("assets/pink.png")
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
        visited = set()
        path = []

        def dfs(x, y):
            if (x, y) == (target_x, target_y):
                path.append((x, y))
                return True
            if (x, y) in visited or not self.is_valid(x, y):
                return False
            visited.add((x, y))
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                if dfs(x + dx, y + dy):
                    path.append((x, y))
                    return True
            return False

        if dfs(self.x, self.y):
            self.path = path[::-1]  # reverse to get from ghost to pacman

    def is_valid(self, x, y):
        return 0 <= y < len(MAZE_LAYOUT) and 0 <= x < len(MAZE_LAYOUT[0]) and MAZE_LAYOUT[y][x] == '0'

    def move_step(self):
        if self.path and len(self.path) > 1:
            self.path.pop(0)
            self.x, self.y = self.path[0]

    def draw(self, screen, tile_size):
        screen.blit(self.image, (self.x * tile_size, self.y * tile_size))
        for px, py in self.path[1:]:
            pygame.draw.rect(screen, (255, 182, 193), (px * tile_size, py * tile_size, tile_size, tile_size), 1)
