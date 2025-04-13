import random
import heapq
import pygame
from maze import MAZE_LAYOUT, TILE_SIZE

def a_star(start, goal, is_valid_func, heuristic_func, forbidden_cells=set()):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        x, y = current
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if y == 14:
            if x == 0:
                directions.append((-1, 0))
            elif x == 27:
                directions.append((1, 0))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if ny == 14:
                if nx == -1:
                    nx = 27
                elif nx == 28:
                    nx = 0
            next_pos = (nx, ny)

            if not is_valid_func(nx, ny) or (next_pos in forbidden_cells and next_pos != goal):
                continue

            new_cost = cost_so_far[current] + 1
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic_func(goal, next_pos)
                heapq.heappush(frontier, (priority, next_pos))
                came_from[next_pos] = current

    if goal not in came_from:
        return []  # No path found

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


class RedGhost:
    def __init__(self, pacman_pos):
        self.image = pygame.image.load("assets/red.png")
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

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    def is_valid(self, x, y):
        if y == 14 and (x == -1 or x == 28):  # tunnel logic
            return True
        return 0 <= y < len(MAZE_LAYOUT) and 0 <= x < len(MAZE_LAYOUT[0]) and MAZE_LAYOUT[y][x] == '0'

    def find_path_to_pacman(self, target_x, target_y, forbidden_cells=None):
        if forbidden_cells is None:
            forbidden_cells = set()
        start = (self.x, self.y)
        goal = (target_x, target_y)
        self.path = a_star(start, goal, self.is_valid, self.heuristic, forbidden_cells)

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
            pygame.draw.rect(screen, (255, 0, 0), (px * tile_size, py * tile_size, tile_size, tile_size), 1)