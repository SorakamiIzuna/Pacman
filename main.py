import pygame
import sys
from maze import draw_maze, TILE_SIZE, MAZE_LAYOUT
from entities.pacman import Pacman
from entities.pinkGhost import PinkGhost
from entities.blueGhost import BlueGhost
from entities.orangeGhost import OrangeGhost
from entities.redGhost import RedGhost

pygame.init()

ROWS = len(MAZE_LAYOUT)
COLS = len(MAZE_LAYOUT[0])
SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE + 40

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 24)
wall = pygame.image.load("assets/pixel-wall.png").convert_alpha()
wall_image = pygame.transform.scale(wall, (TILE_SIZE, TILE_SIZE))

pacman = Pacman()
pink_ghost = PinkGhost(pacman_pos=(pacman.x, pacman.y))
blue_ghost = BlueGhost(pacman_pos=(pacman.x, pacman.y))
orange_ghost = OrangeGhost(pacman_pos=(pacman.x, pacman.y))
red_ghost = RedGhost(pacman_pos=(pacman.x, pacman.y))

FPS = 10
start_pressed = False

def draw_buttons():
    new_random_button = pygame.Rect(10, SCREEN_HEIGHT - 35, 195, 30)
    reset_button = pygame.Rect(245, SCREEN_HEIGHT - 35, 80, 30)       
    start_button = pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 35, 80, 30)
    pygame.draw.rect(screen, (200, 200, 200), new_random_button)
    pygame.draw.rect(screen, (200, 200, 200), reset_button)
    pygame.draw.rect(screen, (0, 255, 0), start_button)
    screen.blit(FONT.render("New Random Position", True, (0, 0, 0)), (20, SCREEN_HEIGHT - 30))
    screen.blit(FONT.render("Reset", True, (0, 0, 0)), (263, SCREEN_HEIGHT - 30))
    screen.blit(FONT.render("Start", True, (0, 0, 0)), (SCREEN_WIDTH - 81, SCREEN_HEIGHT - 30))
    return new_random_button, reset_button, start_button

def game_loop():
    global start_pressed
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_maze(screen, wall_image)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman.move("UP")
        if keys[pygame.K_DOWN]:
            pacman.move("DOWN")
        if keys[pygame.K_LEFT]:
            pacman.move("LEFT")
        if keys[pygame.K_RIGHT]:
            pacman.move("RIGHT")

        pacman.draw(screen, TILE_SIZE)
        pink_ghost.draw(screen, TILE_SIZE)
        orange_ghost.draw(screen, TILE_SIZE)
        blue_ghost.draw(screen, TILE_SIZE)
        red_ghost.draw(screen, TILE_SIZE)

        new_random_btn, reset_btn, start_btn = draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_random_btn.collidepoint(event.pos):
                    pacman.reset_position()
                    pink_ghost.reset_position(pacman_pos=(pacman.x, pacman.y))
                    blue_ghost.reset_position(pacman_pos=(pacman.x, pacman.y))
                    orange_ghost.reset_position(pacman_pos=(pacman.x, pacman.y))
                    red_ghost.reset_position(pacman_pos=(pacman.x, pacman.y))
                    start_pressed = False
                elif reset_btn.collidepoint(event.pos):
                    pink_ghost.restore_start_position()
                    blue_ghost.restore_start_position()
                    orange_ghost.restore_start_position()
                    red_ghost.restore_start_position()
                    start_pressed = False
                elif start_btn.collidepoint(event.pos):
                    pink_ghost.start_position = (pink_ghost.x, pink_ghost.y)
                    blue_ghost.start_position = (blue_ghost.x, blue_ghost.y)
                    orange_ghost.start_position = (orange_ghost.x, orange_ghost.y)
                    red_ghost.start_position = (red_ghost.x, red_ghost.y)
                    pink_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    blue_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    orange_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    red_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    start_pressed = True

        if start_pressed:
            old_pink_x, old_pink_y = pink_ghost.x, pink_ghost.y
            if red_ghost.path:
                red_ghost.move_step()
            if blue_ghost.path:
                blue_ghost.move_step()
            if orange_ghost.path:
                orange_ghost.move_step()
            if pink_ghost.path:
                pink_ghost.move_step()
                next_pink_pos = (pink_ghost.x, pink_ghost.y)
                red_pos = (red_ghost.x, red_ghost.y)
                blue_pos = (blue_ghost.x, blue_ghost.y)
                orange_pos = (orange_ghost.x, orange_ghost.y)
                forbidden_cells = {red_pos, blue_pos, orange_pos}
                if (pacman.x, pacman.y) in forbidden_cells:
                    forbidden_cells.remove((pacman.x, pacman.y))
                if next_pink_pos in forbidden_cells:
                    pink_ghost.x, pink_ghost.y = old_pink_x, old_pink_y
                    pink_ghost.find_path_to_pacman(pacman.x, pacman.y, forbidden_cells)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()