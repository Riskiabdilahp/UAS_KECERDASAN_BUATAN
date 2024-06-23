import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Konfigurasi layar dan grid
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Blok tetris (tetrominoes) dan warnanya
tetrominoes = [
    [[1, 1, 1, 1]],                      # I
    [[1, 1, 1],
     [0, 1, 0]],                        # T
    [[1, 1, 1],
     [1, 0, 0]],                        # L
    [[1, 1, 1],
     [0, 0, 1]],                        # J
    [[1, 1],
     [1, 1]],                           # O
    [[0, 1, 1],
     [1, 1, 0]],                        # S
    [[1, 1, 0],
     [0, 1, 1]]                         # Z
]

tetromino_colors = [CYAN, PURPLE, ORANGE, BLUE, YELLOW, GREEN, RED]

# Membuat layar game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Fungsi untuk menggambar kotak di grid
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

# Kelas untuk blok Tetris
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.rotation = 0
        self.x = 3
        self.y = 0

    def draw(self):
        for row in range(len(self.shape[self.rotation])):
            for col in range(len(self.shape[self.rotation][row])):
                if self.shape[self.rotation][row][col] == 1:
                    draw_block(self.x + col, self.y + row, self.color)

    def move(self, dx, dy):
        if self.can_move(dx, dy):
            self.x += dx
            self.y += dy
            return True
        return False

    def can_move(self, dx, dy):
        for row in range(len(self.shape[self.rotation])):
            for col in range(len(self.shape[self.rotation][row])):
                if self.shape[self.rotation][row][col] == 1:
                    new_x = self.x + col + dx
                    new_y = self.y + row + dy
                    if not (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT):
                        return False
        return True

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def get_blocks(self):
        blocks = []
        for row in range(len(self.shape[self.rotation])):
            for col in range(len(self.shape[self.rotation][row])):
                if self.shape[self.rotation][row][col] == 1:
                    blocks.append((self.x + col, self.y + row))
        return blocks

# Fungsi untuk membuat grid kosong
def create_empty_grid():
    return [[WHITE for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Fungsi untuk menggambar grid
def draw_grid(grid):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            draw_block(col, row, grid[row][col])

# Fungsi untuk menggambar judul
def draw_title():
    font = pygame.font.SysFont(None, 30)
    text = font.render("TETRIS", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 10))

# Fungsi untuk menghapus baris yang penuh
def remove_full_rows(grid):
    full_rows = [row for row in range(GRID_HEIGHT) if all(block != WHITE for block in grid[row])]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [WHITE for _ in range(GRID_WIDTH)])
    return len(full_rows)

# Fungsi utama untuk menjalankan game
def main():
    grid = create_empty_grid()
    current_piece = Tetromino(random.choice(tetrominoes), random.choice(tetromino_colors))
    next_piece = Tetromino(random.choice(tetrominoes), random.choice(tetromino_colors))
    score = 0
    game_over = False

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    current_piece.move(0, 1)
                elif event.key == pygame.K_UP:
                    current_piece.rotate()

        # Memeriksa apakah blok dapat terus jatuh atau tidak
        if not current_piece.move(0, 1):
            for block in current_piece.get_blocks():
                grid[block[1]][block[0]] = current_piece.color
            score += remove_full_rows(grid)
            current_piece = next_piece
            next_piece = Tetromino(random.choice(tetrominoes), random.choice(tetromino_colors))
            if not current_piece.move(0, 0):
                game_over = True

        # Menggambar semua elemen di layar
        screen.fill(WHITE)
        draw_title()
        draw_grid(grid)
        current_piece.draw()

        pygame.display.update()

        # Mengatur kecepatan jatuh blok
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            if not current_piece.move(0, 1):
                for block in current_piece.get_blocks():
                    grid[block[1]][block[0]] = current_piece.color
                score += remove_full_rows(grid)
                current_piece = next_piece
                next_piece = Tetromino(random.choice(tetrominoes), random.choice(tetromino_colors))
                if not current_piece.move(0, 0):
                    game_over = True

    pygame.quit()

if __name__ == '__main__':
    main()
