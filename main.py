import pygame
import sys


class Window:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.is_running = True

        # Размер клетки и количество клеток в строке и столбце
        self.cell_size = 50
        self.num_cells_x = 10
        self.num_cells_y = 10

    def run(self):
        while self.is_running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

    def update(self):
        pass

    def render(self):
        self.screen.fill((255, 255, 255))

        # Вычисляем координаты, чтобы разместить поле по центру экрана
        offset_x = (self.screen.get_width() - self.num_cells_x * self.cell_size) // 2
        offset_y = (self.screen.get_height() - self.num_cells_y * self.cell_size) // 2

        for x in range(self.num_cells_x):
            for y in range(self.num_cells_y):
                # Создаем поверхность для клетки
                cell_surface = pygame.Surface((self.cell_size, self.cell_size))
                cell_surface.fill((255, 255, 255))  # Заполняем клетку цветом

                # Добавляем обводку
                pygame.draw.rect(cell_surface, (0, 0, 0), cell_surface.get_rect(), 2)

                # Получаем прямоугольник для клетки и располагаем его на поле
                cell_rect = cell_surface.get_rect(
                    topleft=(offset_x + x * self.cell_size, offset_y + y * self.cell_size)
                )

                # Отображаем клетку на экране
                self.screen.blit(cell_surface, cell_rect.topleft)

        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Window()
    game.run()
    game.quit_game()