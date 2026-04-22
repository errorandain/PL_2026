import math
import random
import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """Конструктор класса ball"""
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = True          # активна ли пуля для попаданий
        self.stopped = False      # остановилась ли пуля на полу
        self.stop_timer = 0       # таймер для удаления
        self.bounce_count = 0     # счётчик отскоков от пола
        self.max_bounces = 2      # максимум отскоков

    def move(self):
        """Переместить мяч с учётом физики."""
        if self.stopped:
            self.stop_timer += 1
            return

        # Гравитация
        self.vy -= 0.5
        self.x += self.vx
        self.y -= self.vy

        # Отскок от левой и правой стен
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx * 0.8
        elif self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            self.vx = -self.vx * 0.8

        # Отскок от потолка
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = -self.vy * 0.8

        # Отскок от пола
        elif self.y + self.r >= HEIGHT:
            self.y = HEIGHT - self.r
            self.bounce_count += 1

            if self.bounce_count >= self.max_bounces:
                # Останавливаем пулю после N отскоков
                self.vy = 0
                self.vx = 0
                self.stopped = True
                self.live = False
            else:
                # Отскок с потерей энергии
                self.vy = -self.vy * 0.6
                self.vx *= 0.9

            # Если скорость очень мала — тоже останавливаем
            if abs(self.vx) < 0.3:
                self.vx = 0

        # Если пуля почти остановилась в воздухе
        if not self.stopped and abs(self.vx) < 0.1 and abs(self.vy) < 0.1:
            self.stopped = True
            self.live = False

    def draw(self):
        """Рисование пули."""
        pygame.draw.circle(
            self.screen,
            self.color,
            (int(self.x), int(self.y)),
            self.r
        )
        # Обводка для остановившихся пуль
        if self.stopped:
            pygame.draw.circle(
                self.screen,
                BLACK,
                (int(self.x), int(self.y)),
                self.r,
                2
            )

    def hittest(self, obj):
        """Проверка столкновения с целью."""
        if not self.live or self.stopped:
            return False
        dx = self.x - obj.x
        dy = self.y - obj.y
        distance = math.hypot(dx, dy)
        return distance <= self.r + obj.r

    def should_remove(self):
        """Нужно ли удалить пулю."""
        # Удаляем через 3 секунды после остановки
        if self.stopped and self.stop_timer > 90:
            return True
        # Удаляем если улетела далеко за экран
        if self.x < -100 or self.x > WIDTH + 100 or self.y > HEIGHT + 100:
            return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 40
        self.y = 450

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом."""
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание."""
        if event:
            if event.pos[0] - self.x != 0:
                self.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Рисование пушки."""
        end_x = self.x + 50 * math.cos(self.an)
        end_y = self.y + 50 * math.sin(self.an)
        pygame.draw.line(self.screen, self.color, (self.x, self.y), (end_x, end_y), 7)

    def power_up(self):
        """Увеличение мощности при удержании."""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1
        # Скорости для движения
        self.vx = random.randint(-3, 3)
        self.vy = random.randint(-3, 3)
        self.new_target()

    def new_target(self):
        """Создание новой цели."""
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 500)
        self.r = random.randint(10, 50)
        self.color = RED
        self.live = 1

    def move(self):
        """Движение цели с отскоком от стен."""
        if self.live:
            self.x += self.vx
            self.y += self.vy

            if self.x - self.r <= 0 or self.x + self.r >= WIDTH:
                self.vx = -self.vx
            if self.y - self.r <= 0 or self.y + self.r >= HEIGHT:
                self.vy = -self.vy

    def hit(self, points=1):
        """Попадание в цель."""
        self.points += points
        self.live = 0

    def draw(self):
        """Рисование цели."""
        if self.live:
            pygame.draw.circle(
                self.screen,
                self.color,
                (int(self.x), int(self.y)),
                self.r
            )
            pygame.draw.circle(
                self.screen,
                BLACK,
                (int(self.x), int(self.y)),
                self.r // 2
            )


def draw_text(screen, text, x, y, size=30, color=BLACK):
    """Вывод текста на экран."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пушка")
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)

# Две движущиеся цели
targets = [Target(screen) for _ in range(2)]

total_score = 0
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()

    for t in targets:
        t.draw()

    for b in balls:
        b.draw()

    # Интерфейс
    draw_text(screen, f"Счёт: {total_score}", 10, 10)
    draw_text(screen, f"Выстрелов: {bullet}", 10, 40)
    draw_text(screen, f"Пули на поле: {len(balls)}", 10, 70)

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    # Движение пуль и проверка попаданий
    for b in balls[:]:
        b.move()

        if b.should_remove():
            balls.remove(b)
            continue

        if b.live:
            for t in targets:
                if t.live and b.hittest(t):
                    t.live = 0
                    t.hit()
                    total_score += 1
                    t.new_target()
                    b.live = False  # пуля больше не попадает
                    break

    # Движение целей
    for t in targets:
        t.move()

    gun.power_up()

pygame.quit()
