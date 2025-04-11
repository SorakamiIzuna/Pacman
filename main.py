import pygame
import sys
from maze import draw_maze


pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Game")

clock = pygame.time.Clock()
game_running = True

def game_loop():
    global game_running
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        screen.fill((0, 0, 0))  # Nền đen
        draw_maze(screen)      # Vẽ mê cung


        pygame.display.update()
        clock.tick(FPS)

def end_game():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
    end_game()
