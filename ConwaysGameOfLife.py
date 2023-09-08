import pygame
import random


class ConwaysGameOfLife:
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.rows = 100
        self.cols = 100
        self.tick = 10
        self.grid = [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]

    def draw_grid(self, screen):
        cell_width = self.window_width // self.cols
        cell_height = self.window_height // self.rows

        for i in range(self.rows):
            for j in range(self.cols):
                x = j * cell_width
                y = i * cell_height

                if self.grid[i][j] == 1:
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_width, cell_height))
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (x, y, cell_width, cell_height))

    def update_grid(self, grid):
        new_grid = [[0 for _ in range(self.rows)] for _ in range(self.cols)]

        for i in range(self.rows):
            for j in range(self.cols):
                current_state = grid[i][j]

                neighbors = [
                    (i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
                    (i, j - 1), (i, j + 1),
                    (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)
                ]

                live_neighbors = sum(1 for x, y in neighbors
                                     if 0 <= x < self.rows and
                                     0 <= y < self.cols and grid[x][y] == 1)

                if current_state == 1 and (live_neighbors < 2 or live_neighbors > 3):
                    # Cell dies due to underpopulation or overpopulation
                    new_grid[i][j] = 0
                elif current_state == 0 and live_neighbors == 3:
                    # Dead cell becomes alive due to reproduction
                    new_grid[i][j] = 1
                else:
                    # Cell remains in its current state
                    new_grid[i][j] = current_state

        return new_grid

    @staticmethod
    def handle_input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

    def gameoflife(self):
        pygame.init()

        screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Conway's Game of Life")

        clock = pygame.time.Clock()
        running = True

        while running:
            self.handle_input()
            new_grid = self.update_grid(self.grid)
            self.grid = new_grid

            screen.fill((0, 0, 0))
            self.draw_grid(screen)
            pygame.display.flip()

            clock.tick(self.tick)

        pygame.quit()


if __name__ == '__main__':
    game = ConwaysGameOfLife()
    game.gameoflife()
