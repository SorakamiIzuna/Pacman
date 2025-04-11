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
    "110110111010111011011",
    "110010100000001010011",  
    "111010101101101010111", 
    "111010101000101010111", 
    "000000000010000000000", 
    "110110101000101011011",
    "110110101101101011011",  
    "110010100000001010011", 
    "111010101111101010111", 
    "100000000010000000001",
    "101110111010111011101",
    "100010000000000010001",
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
        # if len(row) != len(MAZE_LAYOUT[0]):
        #    print(f"Warning: Row {row_index} has inconsistent length.")
        #    continue
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if tile == '1':
                pygame.draw.rect(screen, WALL_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
            # else: tile == '0', không vẽ gì (để lộ màu nền)

