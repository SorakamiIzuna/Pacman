import pygame
import sys

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 60  # Frames per second

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Game state
game_running = True

# Main game loop
def game_loop():
    global game_running
    while game_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        # Game logic goes here
        # (Add your Pac-Man, Ghosts, and Maze logic in the next steps)

        # Fill the screen with a color (background)
        screen.fill(WHITE)

        # Here you would draw all your game entities (Pac-Man, ghosts, etc.)

        # Update the display
        pygame.display.update()

        # Control the game speed
        clock.tick(FPS)

# End game
def end_game():
    pygame.quit()
    sys.exit()

# Run the game loop
if __name__ == "__main__":
    game_loop()
    end_game()
