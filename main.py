import pygame
import sys
from maze import draw_maze, TILE_SIZE
from entities.pacman import Pacman
from entities.pinkGhost import PinkGhost

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man with Pink Ghost")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 24)

pacman = Pacman()
pink_ghost = PinkGhost()

FPS = 10
start_pressed = False

def draw_buttons():
    reset_button = pygame.Rect(10, 560, 80, 30)
    start_button = pygame.Rect(100, 560, 80, 30)
    pygame.draw.rect(screen, (200, 200, 200), reset_button)
    pygame.draw.rect(screen, (0, 255, 0), start_button)
    screen.blit(FONT.render("Reset", True, (0, 0, 0)), (20, 565))
    screen.blit(FONT.render("Start", True, (0, 0, 0)), (115, 565))
    return reset_button, start_button

def game_loop():
    global start_pressed
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_maze(screen)
        pacman.draw(screen, TILE_SIZE)
        pink_ghost.draw(screen, TILE_SIZE)

        reset_btn, start_btn = draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reset_btn.collidepoint(event.pos):
                    pacman.reset_position()
                    pink_ghost.reset_position()
                    start_pressed = False
                elif start_btn.collidepoint(event.pos):
                    pink_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    start_pressed = True

        if start_pressed and pink_ghost.path:
            pink_ghost.move_step()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
