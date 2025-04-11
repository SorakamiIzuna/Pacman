import random
import pygame 
from maze import MAZE_LAYOUT, TILE_SIZE

class Pacman:
    def __init__(self):
        self.x, self.y = self.get_random_position()

    def get_random_position(self):
        valid_positions = []
        for row_idx, row in enumerate(MAZE_LAYOUT):
            for col_idx, tile in enumerate(row):
                if tile == '0':
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    valid_positions.append((x, y))
        return random.choice(valid_positions)

    def draw(self, screen):
        PACMAN_COLOR = (255, 255, 0)
        radius = TILE_SIZE // 2
        center = (self.x + radius, self.y + radius)
        pygame.draw.circle(screen, PACMAN_COLOR, center, radius)
