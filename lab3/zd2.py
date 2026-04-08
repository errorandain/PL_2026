import pygame
from pygame.draw import *
from random import randint, uniform
import math

# Инициализация Pygame
pygame.init()

# Константы экрана
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FPS = 60

# Цвета
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# Параметры уровней (0-4, всего 5 уровней)
LEVEL_BALL_COUNTS = [2, 4, 6, 8, 10]          # начальное количество шаров на уровне
LEVEL_SCORE_THRESHOLDS = [0, 100, 300, 600, 1000]  # очки для перехода на следующий уровень
LEVEL_SPEED_MULTIPLIER = [1.0, 1.2, 1.5, 2.0, 2.5] # множитель скорости
LEVEL_TIMEOUT = [10, 8, 6, 5, 4]             # время (сек) без попадания до взрыва всех шаров

# Параметры комбо
COMBO_THRESHOLDS = [5, 10, 20, 50]           # количество попаданий подряд
COMBO_MULTIPLIERS = [2, 3, 5, 10]            # соответствующие множители очков

# Базовое количество очков за попадание
BASE_SCORE = 10

# Диапазон случайных скоростей (пикселей в секунду)
MIN_SPEED = 100
MAX_SPEED = 300

class Ball:
    """Класс шарика."""
    def __init__(self, x, y, r, color, vx, vy):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vx = vx
        self.vy = vy

    def move(self, dt):
        """Переместить шарик с учётом времени кадра dt (сек)."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Отражение от стенок
        if self.x - self.r < 0:
            self.x = self.r
            self.vx = -self.vx
        if self.x + self.r > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.r
            self.vx = -self.vx
        if self.y - self.r < 0:
            self.y = self.r
            self.vy = -self.vy
        if self.y + self.r > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.r
            self.vy = -self.vy

    def draw(self, screen):
        """Нарисовать шарик на экране."""
        circle(screen, self.color, (int(self.x), int(self.y)), self.r)

    def contains_point(self, pos):
        """Проверить, находится ли точка pos внутри шарика."""
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        return dx*dx + dy*dy <= self.r*self.r

    def reflect_with(self, other):
        """Упругое столкновение двух шаров."""
        # Вектор между центрами
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        # Нормаль
        nx = dx / dist
        ny = dy / dist
        # Относительная скорость
        dvx = other.vx - self.vx
        dvy = other.vy - self.vy
        # Проекция относительной скорости на нормаль
        vrel = dvx * nx + dvy * ny
        if vrel > 0:
            return
        # Коэффициент упругости (1 - абсолютно упругое)
        e = 1.0
        # Импульс
        m1 = self.r ** 2   # масса пропорциональна площади (или квадрату радиуса)
        m2 = other.r ** 2
        imp = (1 + e) * vrel / (1/m1 + 1/m2)
        # Изменение скоростей
        self.vx += imp / m1 * nx
        self.vy += imp / m1 * ny
        other.vx -= imp / m2 * nx
        other.vy -= imp / m2 * ny

class Game:
    """Основной класс игры."""
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.balls = []
        self.score = 0
        self.level = 0                # 0..4
        self.combo_counter = 0
        self.combo_multiplier = 1
        self.last_hit_time = pygame.time.get_ticks() / 1000.0   # секунды
        self.running = True

        # Создаём шарики для начального уровня
        self._spawn_initial_balls()

    def _spawn_initial_balls(self):
        """Создать начальное количество шаров для текущего уровня."""
        self.balls.clear()
        count = LEVEL_BALL_COUNTS[self.level]
        speed_mult = LEVEL_SPEED_MULTIPLIER[self.level]
        for _ in range(count):
            ball = self._create_random_ball(speed_mult)
            self.balls.append(ball)

    def _create_random_ball(self, speed_mult=1.0):
        """Создать один случайный шарик с множителем скорости."""
        r = randint(20, 50)
        x = randint(r, SCREEN_WIDTH - r)
        y = randint(r, SCREEN_HEIGHT - r)
        color = COLORS[randint(0, len(COLORS)-1)]
        # Случайная скорость в диапазоне, затем умножаем на множитель уровня
        base_vx = uniform(-MAX_SPEED, MAX_SPEED)
        base_vy = uniform(-MAX_SPEED, MAX_SPEED)
        # Чтобы шарик не был слишком медленным
        while abs(base_vx) < MIN_SPEED and abs(base_vy) < MIN_SPEED:
            base_vx = uniform(-MAX_SPEED, MAX_SPEED)
            base_vy = uniform(-MAX_SPEED, MAX_SPEED)
        vx = base_vx * speed_mult
        vy = base_vy * speed_mult
        return Ball(x, y, r, color, vx, vy)

    def _max_balls_allowed(self):
        """Максимальное количество шаров на текущем уровне по формуле n+2*(n+n) = 5*n."""
        n = LEVEL_BALL_COUNTS[self.level]
        return 5 * n

    def _update_combo(self, hit):
        """Обновить комбо: hit = True при попадании, False при промахе."""
        if hit:
            self.combo_counter += 1
            # Определяем множитель
            mult = 1
            for i, thresh in enumerate(COMBO_THRESHOLDS):
                if self.combo_counter >= thresh:
                    mult = COMBO_MULTIPLIERS[i]
                else:
                    break
            self.combo_multiplier = mult
        else:
            self.combo_counter = 0
            self.combo_multiplier = 1

    def _add_score(self, base):
        """Добавить очки с учётом множителя комбо."""
        gained = base * self.combo_multiplier
        self.score += gained
        # После добавления очков проверим переход уровня
        self._check_level_up()

    def _check_level_up(self):
        """Проверить, не пора ли перейти на следующий уровень."""
        if self.level + 1 < len(LEVEL_SCORE_THRESHOLDS) and self.score >= LEVEL_SCORE_THRESHOLDS[self.level + 1]:
            self.level += 1
            # Сброс комбо при переходе
            self.combo_counter = 0
            self.combo_multiplier = 1
            # Удаляем все шары и создаём новые для нового уровня
            self._spawn_initial_balls()
            # Сбрасываем таймер последнего попадания
            self.last_hit_time = pygame.time.get_ticks() / 1000.0

    def _handle_timeout(self, current_time):
        """Проверить таймер бездействия и взорвать все шары при превышении."""
        time_since_last_hit = current_time - self.last_hit_time
        timeout_limit = LEVEL_TIMEOUT[self.level]
        if time_since_last_hit > timeout_limit:
            # Взрыв всех шаров: очищаем и создаём новые
            self.balls.clear()
            self._spawn_initial_balls()
            # Сбрасываем комбо
            self.combo_counter = 0
            self.combo_multiplier = 1
            # Обновляем время последнего попадания, чтобы таймер начал отсчёт заново
            self.last_hit_time = current_time

    def _handle_collisions(self):
        """Обработать столкновения шаров между собой (если уровень >= 3)."""
        if self.level >= 3:
            n = len(self.balls)
            for i in range(n):
                for j in range(i+1, n):
                    b1 = self.balls[i]
                    b2 = self.balls[j]
                    dx = b1.x - b2.x
                    dy = b1.y - b2.y
                    dist = math.hypot(dx, dy)
                    if dist < b1.r + b2.r:
                        # Шары пересеклись – отражаем
                        b1.reflect_with(b2)
                        # Раздвигаем, чтобы не залипали
                        overlap = b1.r + b2.r - dist
                        if dist == 0:
                            angle = uniform(0, 2*math.pi)
                        else:
                            angle = math.atan2(dy, dx)
                        shift_x = math.cos(angle) * overlap / 2
                        shift_y = math.sin(angle) * overlap / 2
                        b1.x += shift_x
                        b1.y += shift_y
                        b2.x -= shift_x
                        b2.y -= shift_y

    def handle_click(self, pos):
        """Обработать клик мыши. Возвращает True, если попали в шарик."""
        # Ищем первый шарик, в который попали
        hit_ball = None
        for ball in self.balls:
            if ball.contains_point(pos):
                hit_ball = ball
                break

        if hit_ball:
            # Попадание
            self._update_combo(True)
            self._add_score(BASE_SCORE)
            # Удаляем шарик
            self.balls.remove(hit_ball)
            # Обновляем время последнего попадания
            self.last_hit_time = pygame.time.get_ticks() / 1000.0

            # Создаём два новых шарика, но не превышая лимит уровня
            max_allowed = self._max_balls_allowed()
            speed_mult = LEVEL_SPEED_MULTIPLIER[self.level]
            for _ in range(2):
                if len(self.balls) < max_allowed:
                    self.balls.append(self._create_random_ball(speed_mult))
            return True
        else:
            # Промах
            self._update_combo(False)
            return False

    def update(self, dt):
        """Обновить состояние игры за время dt (сек)."""
        # Движение шаров
        for ball in self.balls:
            ball.move(dt)
        # Столкновения между шарами (если разрешено)
        self._handle_collisions()
        # Проверка таймера бездействия
        current_time = pygame.time.get_ticks() / 1000.0
        self._handle_timeout(current_time)

    def draw(self):
        """Отрисовать всё на экране."""
        self.screen.fill(BLACK)
        for ball in self.balls:
            ball.draw(self.screen)

        # Отображение счёта, уровня и комбо
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {self.level+1}", True, (255, 255, 255))
        combo_text = font.render(f"Combo: x{self.combo_multiplier} ({self.combo_counter})", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        self.screen.blit(combo_text, (10, 90))

        pygame.display.update()

    def run(self):
        """Главный игровой цикл."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0   # время в секундах между кадрами

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.update(dt)
            self.draw()

        pygame.quit()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Поймай шарик")
    game = Game(screen)
    game.run()

if __name__ == "__main__":
    main()