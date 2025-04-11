import random
from maze import MAZE_LAYOUT

class Pacman:
    def __init__(self):
        self.initial_position = self.find_fixed_position()
        self.x, self.y = self.initial_position

    def find_fixed_position(self):
        for row_index, row in enumerate(MAZE_LAYOUT):
            for col_index, cell in enumerate(row):
                if cell == '0':
                    return col_index, row_index  # Cột là x, hàng là y

    def reset_position(self):
        self.x, self.y = self.initial_position

    def draw(self, screen, tile_size):
        import pygame
        pygame.draw.circle(screen, (255, 255, 0), ((self.x + 0.5) * tile_size, (self.y + 0.5) * tile_size), tile_size // 2)
