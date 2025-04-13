import heapq
import pygame
from maze import MAZE_LAYOUT, TILE_SIZE

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

    def a_star(self, start_x, start_y, target_x, target_y, forbidden_cells=None):
        if forbidden_cells is None:
            forbidden_cells = set()

        open_list = []
        closed_list = set()
        came_from = {}
        g_score = { (start_x, start_y): 0 }
        f_score = { (start_x, start_y): self.heuristic(start_x, start_y, target_x, target_y) }

        heapq.heappush(open_list, (f_score[(start_x, start_y)], (start_x, start_y)))

        while open_list:
            _, current = heapq.heappop(open_list)
            current_x, current_y = current

            if current == (target_x, target_y):
                self.reconstruct_path(came_from, current)
                return True

            closed_list.add(current)

            for neighbor in self.get_neighbors(current_x, current_y):
                if neighbor in closed_list or neighbor in forbidden_cells:
                    continue

                tentative_g_score = g_score.get(current, float('inf')) + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor[0], neighbor[1], target_x, target_y)

                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return False

    def heuristic(self, x, y, target_x, target_y):
        return abs(x - target_x) + abs(y - target_y)  # Manhattan distance

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        self.path = path

    def get_neighbors(self, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for dx, dy in directions:
            next_x, next_y = x + dx, y + dy
            if 0 <= next_x < len(MAZE_LAYOUT[0]) and 0 <= next_y < len(MAZE_LAYOUT):
                if MAZE_LAYOUT[next_y][next_x] == '0':  # Check if it's an open space
                    neighbors.append((next_x, next_y))

        return neighbors

    def move_step(self):
        if self.path and len(self.path) > 1:
            self.path.pop(0)
            next_x, next_y = self.path[0]
            self.x, self.y = next_x, next_y

    def draw(self, screen, tile_size):
        screen.blit(self.image, (self.x * tile_size, self.y * tile_size))
        for px, py in self.path[1:]:
            pygame.draw.rect(screen, (255, 0, 0), (px * tile_size, py * tile_size, tile_size, tile_size), 1)
