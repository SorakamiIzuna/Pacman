import random
import pygame
from maze import MAZE_LAYOUT,TILE_SIZE
import os
from config import ASSET_DIR
class Pacman:
    def __init__(self):
        self.image = pygame.image.load(os.path.join(ASSET_DIR, "pacman.png"))
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.initial_position = self.find_fixed_position()
        self.x, self.y = self.initial_position
        self.speed = 1

    def find_fixed_position(self):
        for row_index, row in enumerate(MAZE_LAYOUT):
            for col_index, cell in enumerate(row):
                if cell == '0':
                    return col_index, row_index
        return 0, 0

    def reset_position(self):
        self.x, self.y = self.initial_position

    def draw(self, screen, tile_size):
        screen.blit(self.image, (self.x * tile_size, self.y * tile_size))

    def move(self, direction):
        self.direction = direction
        next_x, next_y = self.x, self.y

        if self.direction == "UP":
            next_y -= self.speed
        elif self.direction == "DOWN":
            next_y += self.speed
        elif self.direction == "LEFT":
            next_x -= self.speed
        elif self.direction == "RIGHT":
            next_x += self.speed

        if next_y == 14:
            if next_x == -1:
                next_x = 27
            elif next_x == 28:
                next_x = 0

        if self.is_valid_move(next_x, next_y):
            self.x, self.y = next_x, next_y

    def is_valid_move(self, x, y):
        if y == 14 and (x == -1 or x == 28):
            return True
        return 0 <= y < len(MAZE_LAYOUT) and 0 <= x < len(MAZE_LAYOUT[0]) and MAZE_LAYOUT[y][x] == '0'