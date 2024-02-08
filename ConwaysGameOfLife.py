import pygame
import pygame.freetype
import random


class ConwaysGameOfLife:
    def __init__(self, rows=None, cols=None, tick=None):
        self.window_width = 1000
        self.window_height = 800
        self.rows = rows
        self.cols = cols
        self.tick = tick
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
        screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Conway's Game of Life")
        pygame.display.set_mode((self.window_width, self.window_height))

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            new_grid = self.update_grid(self.grid)
            self.grid = new_grid

            screen.fill((0, 0, 0))
            self.draw_grid(screen)
            pygame.display.flip()

            clock.tick(self.tick)


class MenuScreen:
    def __init__(self):
        self.active_box = None
        self.menu_screen_width = 700
        self.menu_screen_height = 400
        self.input_box_width = 140
        self.input_box_height = 32
        self.button_width = 140
        self.button_height = 40
        self.font_size = 24
        self.font_color = pygame.Color('white')
        self.bg_color = pygame.Color('black')
        self.cursor_color = pygame.Color('white')
        self.cursor_width = 2
        self.max_rows = 500
        self.max_cols = 500

    def setup_screen(self):
        screen = pygame.display.set_mode((self.menu_screen_width, self.menu_screen_height))
        pygame.display.set_caption("Setup Conway's Game of Life")

        font = pygame.freetype.SysFont("Arial", self.font_size)

        base_y = (self.menu_screen_height - (3 * self.input_box_height + self.button_height + 20)) // 2
        input_boxes = {
            "rows": {"rect": pygame.Rect((self.menu_screen_width - self.input_box_width) // 2 + 40, base_y,
                                         self.input_box_width, self.input_box_height),
                     "text": '', "active": False, "label": "Rows"},
            "cols": {
                "rect": pygame.Rect((self.menu_screen_width - self.input_box_width) // 2 + 40, base_y + 40,
                                    self.input_box_width, self.input_box_height),
                "text": '', "active": False, "label": "Cols"},
            "tick": {
                "rect": pygame.Rect((self.menu_screen_width - self.input_box_width) // 2 + 40, base_y + 80,
                                    self.input_box_width, self.input_box_height),
                "text": '', "active": False, "label": "Tick"},
        }
        start_button = pygame.Rect((self.menu_screen_width - self.button_width) // 2 + 30, base_y + 130,
                                   self.button_width, self.button_height)

        active_box = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active_box = None
                    for key, value in input_boxes.items():
                        if value["rect"].collidepoint(event.pos):
                            active_box = key
                            value["active"] = True
                        else:
                            value["active"] = False
                    if start_button.collidepoint(event.pos):
                        rows = min(self.max_rows, int(input_boxes["rows"]["text"] or 100))
                        cols = min(self.max_cols, int(input_boxes["cols"]["text"] or 100))
                        tick = int(input_boxes["tick"]["text"] or 10)
                        game = ConwaysGameOfLife(rows, cols, tick)
                        game.gameoflife()
                        return
                if event.type == pygame.KEYDOWN:
                    if active_box is not None:
                        if event.key == pygame.K_BACKSPACE:
                            input_boxes[active_box]["text"] = input_boxes[active_box]["text"][:-1]
                        else:
                            input_boxes[active_box]["text"] += event.unicode
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        if active_box is not None:
                            input_boxes[active_box]["active"] = False
                        if input_boxes[active_box]["text"] != '':
                            input_boxes[active_box]["text"] = input_boxes[active_box]["text"][:-1]
                        active_box = (list(input_boxes.keys()) + [None])[list(input_boxes.keys()).index(active_box) + 1]
                        if active_box is not None:
                            input_boxes[active_box]["active"] = True
                        else:
                            active_box = list(input_boxes.keys())[0]
                            input_boxes[active_box]["active"] = True
                    elif event.key == pygame.K_LSHIFT:
                        if active_box is not None:
                            input_boxes[active_box]["active"] = False
                        input_boxes[active_box]["text"] = input_boxes[active_box]["text"][:-1]
                        active_box = (list(input_boxes.keys()) + [None])[list(input_boxes.keys()).index(active_box) - 1]
                        if active_box is not None:
                            input_boxes[active_box]["active"] = True
                        else:
                            active_box = list(input_boxes.keys())[-1]
                            input_boxes[active_box]["active"] = True
            screen.fill(self.bg_color)

            for key, value in input_boxes.items():
                txt_surface, rect = font.render(value["label"], self.font_color)
                screen.blit(txt_surface, (value["rect"].x - rect.width - 10,
                                          value["rect"].y - 1 + (value["rect"].h - rect.height) // 2))

                pygame.draw.rect(screen, self.font_color, value["rect"], 2)
                txt_surface, rect = font.render(value["text"], self.font_color)
                screen.blit(txt_surface, (value["rect"].x + 5, value["rect"].y + 6))
                pygame.draw.line(screen, self.font_color, (value["rect"].x + 20,
                                                           value["rect"].y - 2 + value["rect"].h),
                                 (value["rect"].x + value["rect"].w,
                                  value["rect"].y - 2 + value["rect"].h), 2)

                if value["active"]:
                    pygame.draw.rect(screen, self.cursor_color, (
                        value["rect"].x + rect.width + 5,
                        value["rect"].y + 3, self.cursor_width, value["rect"].h - 6))

            # Render and position the "Start" text in the button
            txt_surface, rect = font.render('Start', self.font_color)
            screen.blit(txt_surface, (start_button.x + (self.button_width - rect.width) // 2,
                                      start_button.y + (self.button_height - rect.height) // 2))
            pygame.draw.rect(screen, self.font_color, start_button, 2)

            # Render and position of default values
            txt_surface, rect = font.render('Default Values - Rows: 100, Columns: 100, Tick Rate: 10',
                                            self.font_color)
            screen.blit(txt_surface, (self.menu_screen_width - rect.width - 10,
                                      self.menu_screen_height - rect.height - 10))

            pygame.display.flip()


pygame.init()
