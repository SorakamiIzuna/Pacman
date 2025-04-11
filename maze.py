import pygame

# Màu sắc
WALL_COLOR = (0, 0, 255)
TILE_SIZE = 20 # Giữ nguyên kích thước ô hoặc điều chỉnh nếu cần để vừa màn hình

# Ma trận mô tả mê cung: 1 là tường, 0 là đường (bao gồm cả vị trí pellets và không gian nhà ma)
# Layout này được tạo dựa trên hình ảnh image_4b71cd.jpg (19 cột x 23 hàng)
MAZE_LAYOUT = [
    "111111111111111111111",
    "100000000010000000001",
    "101110111010111011101",
    "101110111010111011101",
    "100000000000000000001",
    "101110101111101011101",
    "100000100010001000001",
    "111110111010111011111",
    "111110100000001011111", # Khu vực trên nhà ma # Tường trên nhà ma
    "111110101111101011111", # Tường hai bên nhà ma
    "000000001111100000000", # Coi cổng nhà ma là đường đi '0'
    "111110101111101011111", # Tường hai bên nhà ma
    "111110100000001011111", # Khu vực dưới nhà ma
    "111110101111101011111", # Tường dưới nhà ma
    "100000000010000000001",
    "101110111010111011101",
    "100010000000000010001", # Lưu ý các tường đơn gần vị trí power pellets
    "111010101111101010111",
    "100000100010001000001",
    "101111111010111111101",
    "100000000000000000001",
    "111111111111111111111",
]


# Giữ nguyên hàm draw_maze
def draw_maze(screen):
    """Vẽ mê cung lên màn hình dựa trên MAZE_LAYOUT."""
    for row_index, row in enumerate(MAZE_LAYOUT):
        # Kiểm tra độ dài hàng để tránh lỗi nếu layout không đồng nhất (tùy chọn)
        # if len(row) != len(MAZE_LAYOUT[0]):
        #    print(f"Warning: Row {row_index} has inconsistent length.")
        #    continue
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if tile == '1':
                pygame.draw.rect(screen, WALL_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
            # else: tile == '0', không vẽ gì (để lộ màu nền)

# --- Phần code Pygame để chạy và hiển thị (ví dụ) ---
if __name__ == '__main__':
    pygame.init()

    # Tính toán kích thước màn hình dựa trên layout và TILE_SIZE
    maze_cols = len(MAZE_LAYOUT[0])
    maze_rows = len(MAZE_LAYOUT)
    SCREEN_WIDTH = maze_cols * TILE_SIZE
    SCREEN_HEIGHT = maze_rows * TILE_SIZE
    BG_COLOR = (0, 0, 0) # Màu nền đen

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Display")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR) # Xóa màn hình với màu nền
        draw_maze(screen)     # Vẽ mê cung
        pygame.display.flip() # Cập nhật màn hình

    pygame.quit()