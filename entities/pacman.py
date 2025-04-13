import random
import pygame
from maze import MAZE_LAYOUT, TILE_SIZE

class Pacman:
    def __init__(self):
        self.image = pygame.image.load("assets/pacman.png")
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

        if self.direction == "UP":
            if self.is_valid_move(self.x, self.y - self.speed):
                self.y -= self.speed
        elif self.direction == "DOWN":
            if self.is_valid_move(self.x, self.y + self.speed):
                self.y += self.speed
        elif self.direction == "LEFT":
            if self.is_valid_move(self.x - self.speed, self.y):
                self.x -= self.speed
        elif self.direction == "RIGHT":
            if self.is_valid_move(self.x + self.speed, self.y):
                self.x += self.speed

    def is_valid_move(self, x, y):
        if 0 <= x < len(MAZE_LAYOUT[0]) and 0 <= y < len(MAZE_LAYOUT):
            return MAZE_LAYOUT[y][x] == '0'
        return False
