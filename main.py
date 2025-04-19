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
SCREEN_HEIGHT = ROWS * TILE_SIZE

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
old_pacman_pos = (pacman.x, pacman.y)
last_path_update_time = 0
UPDATE_INTERVAL = 500

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


def check_endgame(pacman, ghosts_list):
    for ghost_tuple in ghosts_list:
        if ghost_tuple is not None:
            ghost, _, _ = ghost_tuple
            if (ghost.x, ghost.y) == (pacman.x, pacman.y):
                return True
    return False


def level_selection_screen():
    running = True
    while running:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 48)
        title_surface = font.render("Select a Level", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)

        level_buttons = []
        for i in range(1, 6):
            button = pygame.Rect(SCREEN_WIDTH // 2 - 50, 100 + (i - 1) * 60, 100, 40)
            pygame.draw.rect(screen, (0, 0, 255), button)
            screen.blit(FONT.render(f"Level {i}", True, (255, 255, 255)), (SCREEN_WIDTH // 2 - 30, 110 + (i - 1) * 60))
            level_buttons.append((button, i))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button, lvl in level_buttons:
                    if button.collidepoint(event.pos):
                        return lvl  

        pygame.display.update()
        clock.tick(FPS)


def display_level_screen(level):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 72)
    text_surface = font.render(f"Level {level}", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  


def set_level(level):
    global blue_ghost, pink_ghost, orange_ghost, red_ghost
    if level == 1:
        blue_ghost = BlueGhost(pacman_pos=(pacman.x, pacman.y))
        pink_ghost = None
        orange_ghost = None
        red_ghost = None
    elif level == 2:
        blue_ghost = None
        pink_ghost = PinkGhost(pacman_pos=(pacman.x, pacman.y))
        orange_ghost = None
        red_ghost = None
    elif level == 3:
        blue_ghost = None
        pink_ghost = None
        orange_ghost = OrangeGhost(pacman_pos=(pacman.x, pacman.y))
        red_ghost = None
    elif level == 4:
        blue_ghost = None
        pink_ghost = None
        orange_ghost = None
        red_ghost = RedGhost(pacman_pos=(pacman.x, pacman.y))
    elif level == 5:
        blue_ghost = BlueGhost(pacman_pos=(pacman.x, pacman.y))
        pink_ghost = PinkGhost(pacman_pos=(pacman.x, pacman.y))
        orange_ghost = OrangeGhost(pacman_pos=(pacman.x, pacman.y))
        red_ghost = RedGhost(pacman_pos=(pacman.x, pacman.y))

def game_loop():
    global start_pressed, old_pacman_pos, last_path_update_time
    ghost_move_counter = 0
    GHOST_MOVE_DELAY = 3
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
        
        
        if blue_ghost:
            blue_ghost.draw(screen, TILE_SIZE)
        if pink_ghost:
            pink_ghost.draw(screen, TILE_SIZE)
        if orange_ghost:
            orange_ghost.draw(screen, TILE_SIZE)
        if red_ghost:
            red_ghost.draw(screen, TILE_SIZE)

        new_random_btn, reset_btn, start_btn = draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_random_btn.collidepoint(event.pos):
                    pacman.reset_position()
                    if pink_ghost:
                        pink_ghost.reset_position(pacman_pos=(pacman.x, pacman.y))
                    if blue_ghost:
                        blue_ghost.reset_position(pacman_pos=(pacman.x, pacman.y))
                    if orange_ghost:
                        orange_ghost.reset_position(pacman_pos=(pacman.x, pacman.y))
                    if red_ghost:
                        red_ghost.reset_position(pacman_pos=(pacman.x, pacman.y))
                    start_pressed = False
                    old_pacman_pos = (pacman.x, pacman.y)
                elif reset_btn.collidepoint(event.pos):
                    if pink_ghost:
                        pink_ghost.restore_start_position()
                    if blue_ghost:
                        blue_ghost.restore_start_position()
                    if orange_ghost:
                        orange_ghost.restore_start_position()
                    if red_ghost:
                        red_ghost.restore_start_position()
                    start_pressed = False
                    old_pacman_pos = (pacman.x, pacman.y)
                elif start_btn.collidepoint(event.pos):
                    if pink_ghost:
                        pink_ghost.start_position = (pink_ghost.x, pink_ghost.y)
                        pink_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    if blue_ghost:
                        blue_ghost.start_position = (blue_ghost.x, blue_ghost.y)
                        blue_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    if orange_ghost:
                        orange_ghost.start_position = (orange_ghost.x, orange_ghost.y)
                        orange_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    if red_ghost:
                        red_ghost.start_position = (red_ghost.x, red_ghost.y)
                        red_ghost.find_path_to_pacman(pacman.x, pacman.y)
                    start_pressed = True
                    old_pacman_pos = (pacman.x, pacman.y)

        if start_pressed:
            current_time = pygame.time.get_ticks()
            pacman_moved = (pacman.x, pacman.y) != old_pacman_pos
           
            if pacman_moved:
                if pink_ghost:
                    pink_ghost.find_path_to_pacman(pacman.x, pacman.y)
                if blue_ghost:
                    blue_ghost.find_path_to_pacman(pacman.x, pacman.y)
                if orange_ghost:
                    orange_ghost.find_path_to_pacman(pacman.x, pacman.y)
                if red_ghost:
                    red_ghost.find_path_to_pacman(pacman.x, pacman.y)
                last_path_update_time = current_time
            old_pacman_pos = (pacman.x, pacman.y)

            old_red_pos = (red_ghost.x, red_ghost.y) if red_ghost else None
            old_blue_pos = (blue_ghost.x, blue_ghost.y) if blue_ghost else None
            old_orange_pos = (orange_ghost.x, orange_ghost.y) if orange_ghost else None
            old_pink_pos = (pink_ghost.x, pink_ghost.y) if pink_ghost else None

            next_positions = {}
           
            ghosts = [
                (red_ghost, 'red', 0) if red_ghost else None,
                (blue_ghost, 'blue', 1) if blue_ghost else None,
                (orange_ghost, 'orange', 2) if orange_ghost else None,
                (pink_ghost, 'pink', 3) if pink_ghost else None
            ]
            ghosts = [ghost for ghost in ghosts if ghost is not None]  

            ghost_move_counter += 1
            if ghost_move_counter >= GHOST_MOVE_DELAY:
                ghost_move_counter = 0  

                for ghost, name, _ in ghosts:
                    if ghost and ghost.path and len(ghost.path) > 1:
                        ghost.move_step()
                        next_pos = (ghost.x, ghost.y)
                        next_positions[name] = next_pos
                    else:
                        next_positions[name] = (ghost.x, ghost.y) if ghost else None
            else:
                for ghost, name, _ in ghosts:
                    next_positions[name] = (ghost.x, ghost.y) if ghost else None
            pos_count = {}
            for name, pos in next_positions.items():
                if pos:
                    pos_count[pos] = pos_count.get(pos, []) + [(name, ghosts[[g[1] for g in ghosts].index(name)][0])]

            for pos, ghost_list in pos_count.items():
                if len(ghost_list) > 1 and pos != (pacman.x, pacman.y):
                    ghost_list.sort(key=lambda x: [g[2] for g in ghosts if g[1] == x[0]][0])
                    winner_name, winner_ghost = ghost_list[0]
                    for loser_name, loser_ghost in ghost_list[1:]:
                        if loser_name == 'red' and red_ghost:
                            red_ghost.x, red_ghost.y = old_red_pos
                        elif loser_name == 'blue' and blue_ghost:
                            blue_ghost.x, blue_ghost.y = old_blue_pos
                        elif loser_name == 'orange' and orange_ghost:
                            orange_ghost.x, orange_ghost.y = old_orange_pos
                        elif loser_name == 'pink' and pink_ghost:
                            pink_ghost.x, pink_ghost.y = old_pink_pos
                        forbidden_cells = {next_positions[winner_name]}
                        loser_ghost.find_path_to_pacman(pacman.x, pacman.y, forbidden_cells)
                elif pos == (pacman.x, pacman.y):
                    pass
                else:
                    pass

            if check_endgame(pacman, ghosts):
                game_over_font = pygame.font.SysFont(None, 72)
                text_surface = game_over_font.render("GAME OVER!", True, (255, 0, 0))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text_surface, text_rect)
                pygame.display.update()

                print("Game Over! Returning to level selection!")
                pygame.time.delay(2000)
                return 

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def main():
    while True:
        selected_level = level_selection_screen()  
        display_level_screen(selected_level) 
        set_level(selected_level) 
        game_loop()  

if __name__ == "__main__":
    main()