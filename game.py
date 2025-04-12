import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PACMAN_SPEED = 5

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pac-Man Game')

# Clock
clock = pygame.time.Clock()

# Load Pac-Man image
pacman_img = pygame.image.load('./assets/pacman.png').convert_alpha()
pacman_rect = pacman_img.get_rect()
pacman_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

def main():
    running = True

    while running:
        clock.tick(FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pacman_rect.x -= PACMAN_SPEED
        if keys[pygame.K_RIGHT]:
            pacman_rect.x += PACMAN_SPEED
        if keys[pygame.K_UP]:
            pacman_rect.y -= PACMAN_SPEED
        if keys[pygame.K_DOWN]:
            pacman_rect.y += PACMAN_SPEED

        # Fill background
        screen.fill((0, 0, 0))

        # Draw Pac-Man image
        screen.blit(pacman_img, pacman_rect)

        # Update screen
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
