import pygame
import sys
import random

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CELL_SIZE = 50
NUM_CELLS_X = 12
NUM_CELLS_Y = 12
MAX_ANTHILLS = 4
MIN_ANTHILLS = 1
PLAYER_ICON = "P"
ANTHILL_ICON = "A"

class Anthill:
    def __init__(self, existing_positions):
        self.positions = self.generate_random_positions(existing_positions)

    def generate_random_positions(self, existing_positions):
        positions = set()
        num_anthills = random.randint(MIN_ANTHILLS, MAX_ANTHILLS)
        while len(positions) < num_anthills:
            x = random.randint(1, NUM_CELLS_X - 2)
            y = random.randint(1, NUM_CELLS_Y - 2)
            position = (x, y)
            if position not in existing_positions and position not in positions:
                positions.add(position)
        return positions

class Field:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.anthill = Anthill({(self.player.x, self.player.y)})

    def render(self, offset_x, offset_y):
        for x in range(NUM_CELLS_X):
            for y in range(NUM_CELLS_Y):
                cell_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
                cell_surface.fill((255, 255, 255))
                pygame.draw.rect(cell_surface, (0, 0, 0), cell_surface.get_rect(), 2)

                if x == 0 or x == NUM_CELLS_X - 1 or y == 0 or y == NUM_CELLS_Y - 1:
                    cell_surface.fill((255, 0, 0))

                cell_rect = cell_surface.get_rect(
                    topleft=(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE)
                )

                self.screen.blit(cell_surface, cell_rect.topleft)

        player_text = pygame.font.Font(None, CELL_SIZE).render(PLAYER_ICON, True, (0, 0, 255))
        player_rect = player_text.get_rect(
            center=(offset_x + (self.player.x + 0.5) * CELL_SIZE,
                    offset_y + (self.player.y + 0.5) * CELL_SIZE)
        )
        self.screen.blit(player_text, player_rect.topleft)

        for position in self.anthill.positions:
            anthill_text = pygame.font.Font(None, CELL_SIZE).render(ANTHILL_ICON, True, (255, 0, 0))
            anthill_rect = anthill_text.get_rect(
                center=(offset_x + (position[0] + 0.5) * CELL_SIZE,
                        offset_y + (position[1] + 0.5) * CELL_SIZE)
            )
            self.screen.blit(anthill_text, anthill_rect.topleft)

class Player:
    def __init__(self):
        self.spawn_not_on_border()

    def spawn_not_on_border(self):
        self.x = random.randint(1, NUM_CELLS_X - 2)
        self.y = random.randint(1, NUM_CELLS_Y - 2)

    def move(self, dx, dy, anthill_positions):
        new_x = (self.x + dx) % NUM_CELLS_X
        new_y = (self.y + dy) % NUM_CELLS_Y

        if new_x == 0 or new_x == NUM_CELLS_X - 1 or new_y == 0 or new_y == NUM_CELLS_Y - 1:
            return
        if (new_x, new_y) not in anthill_positions:
            self.x = new_x
            self.y = new_y

class Window:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.field = Field(self.screen)

    def run(self):
        while self.is_running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        anthill_positions = self.field.anthill.positions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                elif event.key == pygame.K_UP:
                    self.field.player.move(0, -1, anthill_positions)
                elif event.key == pygame.K_DOWN:
                    self.field.player.move(0, 1, anthill_positions)
                elif event.key == pygame.K_LEFT:
                    self.field.player.move(-1, 0, anthill_positions)
                elif event.key == pygame.K_RIGHT:
                    self.field.player.move(1, 0, anthill_positions)

    def update(self):
        pass

    def render(self):
        self.screen.fill((255, 255, 255))
        offset_x = (self.screen.get_width() - NUM_CELLS_X * CELL_SIZE) // 2
        offset_y = (self.screen.get_height() - NUM_CELLS_Y * CELL_SIZE) // 2

        self.field.render(offset_x, offset_y)

        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Window()
    game.run()
    game.quit_game()