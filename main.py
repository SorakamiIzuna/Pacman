import pygame
import sys
from maze import draw_maze, TILE_SIZE, MAZE_LAYOUT
from entities.pacman import Pacman
from entities.pinkGhost import PinkGhost
from entities.blueGhost import BlueGhost
from entities.orangeGhost import OrangeGhost

# Khởi tạo Pygame
pygame.init()

# Tính kích thước màn hình dựa trên kích thước mê cung
ROWS = len(MAZE_LAYOUT)
COLS = len(MAZE_LAYOUT[0])
SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE + 40  # Thêm vùng nút điều khiển

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man with Pink, Blue, Orange Ghost")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 24)

# Khởi tạo đối tượng
pacman = Pacman()
pink_ghost = PinkGhost()
blue_ghost = BlueGhost()
orange_ghost = OrangeGhost()

FPS = 10
start_pressed = False

def draw_buttons():
    reset_button = pygame.Rect(10, SCREEN_HEIGHT - 35, 80, 30)
    start_button = pygame.Rect(100, SCREEN_HEIGHT - 35, 80, 30)
    pygame.draw.rect(screen, (200, 200, 200), reset_button)
    pygame.draw.rect(screen, (0, 255, 0), start_button)
    screen.blit(FONT.render("Reset", True, (0, 0, 0)), (20, SCREEN_HEIGHT - 30))
    screen.blit(FONT.render("Start", True, (0, 0, 0)), (115, SCREEN_HEIGHT - 30))
    return reset_button, start_button

def game_loop():
    global start_pressed
    running = True
    while running:
        screen.fill((0, 0, 0))

        # Vẽ mê cung
        draw_maze(screen)

        # Xử lý sự kiện bàn phím để di chuyển Pacman
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman.move("UP")
        if keys[pygame.K_DOWN]:
            pacman.move("DOWN")
        if keys[pygame.K_LEFT]:
            pacman.move("LEFT")
        if keys[pygame.K_RIGHT]:
            pacman.move("RIGHT")

        # Vẽ Pacman và Ghost
        pacman.draw(screen, TILE_SIZE)
        pink_ghost.draw(screen, TILE_SIZE)
        orange_ghost.draw(screen, TILE_SIZE)
        blue_ghost.draw(screen, TILE_SIZE)

        # Vẽ nút bấm
        reset_btn, start_btn = draw_buttons()

        # Xử lý sự kiện chuột
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reset_btn.collidepoint(event.pos):
                    pacman.reset_position()
                    pink_ghost.reset_position()
                    blue_ghost.reset_position()
                    orange_ghost.reset_position()
                    start_pressed = False
                elif start_btn.collidepoint(event.pos):
                    pink_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    blue_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    orange_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    start_pressed = True

        # Di chuyển ma (nếu đã bắt đầu)
        if start_pressed:
            if pink_ghost.path:
                pink_ghost.move_step()
            if blue_ghost.path:
                blue_ghost.move_step()
            if orange_ghost.path:
                orange_ghost.move_step()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
