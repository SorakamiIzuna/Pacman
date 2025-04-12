import random
from collections import deque
from maze import MAZE_LAYOUT

class BlueGhost:
    def __init__(self):
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
        parent_map = {}

        queue = deque([(self.x, self.y)])
        visited.add((self.x, self.y))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            current_x, current_y = queue.popleft()

            if (current_x, current_y) == (target_x, target_y):
                # Truy ngược đường đi từ Pacman đến ma quái
                self.path = []
                while (current_x, current_y) != (self.x, self.y):
                    self.path.append((current_x, current_y))
                    current_x, current_y = parent_map[(current_x, current_y)]
                self.path.append((self.x, self.y))
                self.path.reverse()  # Đảo ngược để có đường đi từ ma quái đến Pacman
                return

            for dx, dy in directions:
                next_x, next_y = current_x + dx, current_y + dy
                if self.is_valid(next_x, next_y) and (next_x, next_y) not in visited:
                    visited.add((next_x, next_y))
                    parent_map[(next_x, next_y)] = (current_x, current_y)
                    queue.append((next_x, next_y))

    def is_valid(self, x, y):
        return 0 <= y < len(MAZE_LAYOUT) and 0 <= x < len(MAZE_LAYOUT[0]) and MAZE_LAYOUT[y][x] == '0'

    def move_step(self):
        if self.path and len(self.path) > 1:
            self.path.pop(0)  # Xóa bước hiện tại
            self.x, self.y = self.path[0]  # Di chuyển đến bước tiếp theo

    def draw(self, screen, tile_size):
        import pygame
        pygame.draw.circle(screen, (102, 171, 255), ((self.x + 0.5) * tile_size, (self.y + 0.5) * tile_size), tile_size // 2)

        for px, py in self.path[1:]:
            pygame.draw.rect(screen, (255, 182, 193), (px * tile_size, py * tile_size, tile_size, tile_size), 1)
