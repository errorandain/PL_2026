import pygame
from pygame.draw import *
from random import randint, choice
import math

# --- Инициализация Pygame ---
pygame.init()

# --- Константы экрана и времени ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FPS = 60  # Частота обновления экрана для плавного движения

# --- Цвета (RGB) ---
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# --- Настройки экрана и времени ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Поймай шарик")
clock = pygame.time.Clock()

# --- Глобальные переменные игры ---
score = 0                # Общее количество очков
level = 1                # Текущий уровень (1-5)
combo_counter = 0        # Счетчик успешных попаданий подряд (для комбо)
balls = []               # Список всех шаров на экране (объекты Ball)
idle_timer = 0           # Таймер бездействия (в миллисекундах)

# --- Класс Ball (шарик) ---
class Ball:
    """Класс, представляющий движущийся шарик."""
    def __init__(self, x=None, y=None, r=None, vx=None, vy=None, color=None):
        """Инициализация шарика со случайными параметрами, если не заданы."""
        self.x = x if x is not None else randint(50, SCREEN_WIDTH - 50)
        self.y = y if y is not None else randint(50, SCREEN_HEIGHT - 50)
        self.r = r if r is not None else randint(15, 40)
        self.vx = vx if vx is not None else randint(-5, 5)
        self.vy = vy if vy is not None else randint(-5, 5)
        # Убедимся, что скорость не нулевая
        while self.vx == 0 and self.vy == 0:
            self.vx = randint(-5, 5)
            self.vy = randint(-5, 5)
        self.color = color if color is not None else choice(COLORS)

    def move(self):
        """Движение шарика с отражением от стен."""
        self.x += self.vx
        self.y += self.vy

        # Отражение по горизонтали
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx
        elif self.x + self.r >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.r
            self.vx = -self.vx

        # Отражение по вертикали
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = -self.vy
        elif self.y + self.r >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.r
            self.vy = -self.vy

    def draw(self, surface):
        """Отрисовка шарика."""
        circle(surface, self.color, (self.x, self.y), self.r)

    def contains_point(self, px, py):
        """Проверка, находится ли точка (px, py) внутри шарика."""
        distance = math.hypot(px - self.x, py - self.y)
        return distance <= self.r

    def collide_with_ball(self, other):
        """Проверка и обработка столкновения с другим шаром (упругое)."""
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        min_dist = self.r + other.r

        if distance < min_dist:
            # Корректировка позиций, чтобы шары не накладывались
            if distance == 0:
                distance = 1
            overlap = min_dist - distance
            angle = math.atan2(dy, dx)
            self.x += math.cos(angle) * (overlap / 2)
            self.y += math.sin(angle) * (overlap / 2)
            other.x -= math.cos(angle) * (overlap / 2)
            other.y -= math.sin(angle) * (overlap / 2)

            # Обмен скоростями (упругое столкновение)
            self.vx, other.vx = other.vx, self.vx
            self.vy, other.vy = other.vy, self.vy

# --- Функции игры ---
def create_initial_balls():
    """Создание начального набора шаров в зависимости от уровня."""
    global balls
    balls.clear()
    # Количество шаров: 2, 4, 6, 8, 10 для уровней 1-5
    num_balls = [2, 4, 6, 8, 10][level - 1]
    # Базовый множитель скорости в зависимости от уровня (чем выше, тем быстрее)
    speed_multiplier = 1 + (level - 1) * 0.3

    for _ in range(num_balls):
        # Генерируем шары с учетом уровня (увеличиваем скорость)
        base_vx = randint(-5, 5)
        base_vy = randint(-5, 5)
        while base_vx == 0 and base_vy == 0:
            base_vx = randint(-5, 5)
            base_vy = randint(-5, 5)
        vx = int(base_vx * speed_multiplier)
        vy = int(base_vy * speed_multiplier)

        ball = Ball(vx=vx, vy=vy)
        balls.append(ball)

def handle_click(pos):
    """Обработка клика мыши: проверка попадания по шарам и начисление очков."""
    global score, combo_counter, idle_timer, level, balls

    # Сброс таймера бездействия при любом клике
    idle_timer = 0

    # Проверяем все шары
    hit_ball = None
    for ball in balls:
        if ball.contains_point(pos[0], pos[1]):
            hit_ball = ball
            break

    if hit_ball:
        # Попадание!
        # Начисление очков с учетом комбо
        base_points = 10
        combo_multipliers = [1, 2, 3, 5, 10]  # для комбо 1,2,3,4,5+
        combo_index = min(combo_counter, 4)    # максимум 4 (x10)
        points = base_points * combo_multipliers[combo_index]

        score += points
        combo_counter += 1
        print(f"Попадание! +{points} очков. Комбо: {combo_counter}")

        # "Взрыв" шарика: удаляем его и создаем два новых
        balls.remove(hit_ball)
        
        # Ограничение количества шаров: не более 30
        if len(balls) < 30:
            # Создаем два новых шара со скоростями чуть выше
            speed_mult = 1 + (level - 1) * 0.3
            for _ in range(2):
                vx = randint(-5, 5) + randint(1, 3) * (1 if randint(0,1) else -1)
                vy = randint(-5, 5) + randint(1, 3) * (1 if randint(0,1) else -1)
                vx = int(vx * speed_mult)
                vy = int(vy * speed_mult)
                new_ball = Ball(vx=vx, vy=vy)
                balls.append(new_ball)

        # Проверка на переход уровня
        required_score = level * 50  # для перехода нужно 50, 100, 150, 200, 250 очков
        if score >= required_score and level < 5:
            level += 1
            combo_counter = 0  # Сброс комбо при переходе уровня
            print(f"УРОВЕНЬ {level}! Скорость увеличена.")
            create_initial_balls()  # пересоздаем шары для нового уровня
        elif score >= 250 and level == 5:
            # Если достигнут максимум уровня 5, продолжаем игру бесконечно,
            # но уровень остается 5, просто счет растет дальше
            print(f"Максимальный уровень! Счет: {score}")
    else:
        # Промах: сброс комбо
        combo_counter = 0
        print("Промах! Комбо сброшено.")

def update_idle_timer(dt):
    """Обновление таймера бездействия. Возвращает True, если таймер сработал."""
    global idle_timer, balls, level, combo_counter
    if balls:  # если есть шары на экране
        # Время до взрыва в зависимости от уровня (чем выше уровень, тем меньше времени)
        timeout = max(1000, 5000 - (level - 1) * 800)  # от 5000 до 1000 мс
        idle_timer += dt
        if idle_timer >= timeout:
            # Взрыв всех шаров
            print("Таймер бездействия: все шары взорваны!")
            balls.clear()
            # Создаем новые шары с наказанием (сбрасываем комбо)
            combo_counter = 0
            create_initial_balls()
            idle_timer = 0
            return True
    else:
        idle_timer = 0
    return False

def handle_ball_collisions():
    """Обработка столкновений шаров между собой (включается с 3 уровня)."""
    if level >= 3:
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                balls[i].collide_with_ball(balls[j])

def draw_ui():
    """Отрисовка интерфейса: очки, уровень, комбо."""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    combo_text = font.render(f"Combo: x{min(combo_counter, 10)}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))
    screen.blit(combo_text, (10, 90))

def reset_game():
    """Сброс всех глобальных переменных для новой игры."""
    global score, level, combo_counter, balls, idle_timer
    score = 0
    level = 1
    combo_counter = 0
    idle_timer = 0
    create_initial_balls()

# --- Основной игровой цикл ---
def main():
    reset_game()
    running = True

    while running:
        dt = clock.tick(FPS)  # Получаем время в миллисекундах

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    handle_click(event.pos)

        # Обновление таймера бездействия
        update_idle_timer(dt)

        # Движение и отрисовка всех шаров
        for ball in balls:
            ball.move()
            ball.draw(screen)

        # Обработка столкновений шаров (если уровень >= 3)
        handle_ball_collisions()

        # Отрисовка интерфейса
        draw_ui()

        # Если шаров нет, пересоздаем (аварийная ситуация)
        if not balls:
            create_initial_balls()
            idle_timer = 0

        pygame.display.update()
        screen.fill(BLACK)

    pygame.quit()

if __name__ == "__main__":
    main()