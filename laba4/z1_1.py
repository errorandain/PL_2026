import pygame
from pygame.draw import *
from random import randint, choice
import math
import sys

# --- Инициализация Pygame ---
pygame.init()

# --- Константы экрана и времени ---
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
FPS = 60

# --- Цвета ---
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# --- Настройки экрана ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Поймай шарик - Настройки")
clock = pygame.time.Clock()

# --- Класс Button (кнопка) ---
class Button:
    """Класс для создания интерактивных кнопок."""
    
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=LIGHT_GRAY, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
    
    def draw(self, surface):
        """Рисует кнопку."""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        """Обрабатывает события мыши."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False


class Slider:
    """Класс для создания ползунка настроек."""
    
    def __init__(self, x, y, width, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        self.knob_radius = 10
        
    def draw(self, surface):
        """Рисует ползунок."""
        font = pygame.font.Font(None, 28)
        label_text = font.render(f"{self.label}: {self.value:.1f}", True, WHITE)
        surface.blit(label_text, (self.rect.x, self.rect.y - 25))
        
        # Рисуем линию
        pygame.draw.line(surface, WHITE, (self.rect.x, self.rect.y + 10), 
                        (self.rect.x + self.rect.width, self.rect.y + 10), 3)
        
        # Вычисляем позицию ручки
        knob_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        knob_pos = (knob_x, self.rect.y + 10)
        
        # Рисуем ручку
        pygame.draw.circle(surface, ORANGE, (int(knob_pos[0]), int(knob_pos[1])), self.knob_radius)
        pygame.draw.circle(surface, WHITE, (int(knob_pos[0]), int(knob_pos[1])), self.knob_radius, 2)
    
    def handle_event(self, event):
        """Обрабатывает события мыши для ползунка."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                knob_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
                if abs(mouse_x - knob_x) <= self.knob_radius and abs(mouse_y - (self.rect.y + 10)) <= self.knob_radius:
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
                self.value = self.min_val + (mouse_x - self.rect.x) / self.rect.width * (self.max_val - self.min_val)
                return True
        return False


class Checkbox:
    """Класс для создания чекбокса."""
    
    def __init__(self, x, y, label, initial_state=False):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.label = label
        self.checked = initial_state
        self.is_hovered = False
    
    def draw(self, surface):
        """Рисует чекбокс."""
        font = pygame.font.Font(None, 28)
        label_text = font.render(self.label, True, WHITE)
        surface.blit(label_text, (self.rect.x + 30, self.rect.y))
        
        # Рисуем квадрат
        color = LIGHT_GRAY if self.is_hovered else WHITE
        pygame.draw.rect(surface, color, self.rect, 2)
        
        if self.checked:
            pygame.draw.line(surface, GREEN, (self.rect.x + 3, self.rect.y + 10), 
                           (self.rect.x + 8, self.rect.y + 17), 3)
            pygame.draw.line(surface, GREEN, (self.rect.x + 8, self.rect.y + 17), 
                           (self.rect.x + 17, self.rect.y + 3), 3)
    
    def handle_event(self, event):
        """Обрабатывает события мыши для чекбокса."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                self.checked = not self.checked
                return True
        return False


class SettingsMenu:
    """Класс меню настроек."""
    
    def __init__(self):
        self.visible = False
        
        # Настройки по умолчанию
        self.timeout = 5.0  # секунд
        self.speed_multiplier = 1.0
        self.collisions_enabled = False
        self.ball_count = 2
        self.combo_enabled = True
        
        # Создаем элементы управления
        self.create_ui_elements()
        
        # Кнопки навигации
        self.back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, 
                                  "Back to Game", GREEN, LIGHT_GRAY)
        self.apply_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 170, 200, 50,
                                  "Apply Settings", ORANGE, LIGHT_GRAY)
        self.reset_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 240, 200, 50,
                                  "Reset to Default", RED, LIGHT_GRAY)
    
    def create_ui_elements(self):
        """Создает элементы управления."""
        start_y = 150
        spacing = 80
        
        # Ползунок таймера перезапуска (1-15 секунд)
        self.timeout_slider = Slider(SCREEN_WIDTH // 2 - 200, start_y, 400, 1, 15, 
                                     self.timeout, "Timeout (seconds)")
        
        # Ползунок скорости (0.5-3.0)
        self.speed_slider = Slider(SCREEN_WIDTH // 2 - 200, start_y + spacing, 400, 0.5, 3.0,
                                   self.speed_multiplier, "Speed Multiplier")
        
        # Чекбокс коллизий
        self.collisions_checkbox = Checkbox(SCREEN_WIDTH // 2 - 100, start_y + spacing * 2,
                                           "Enable Ball Collisions", self.collisions_enabled)
        
        # Ползунок количества шаров (2-15)
        self.ball_count_slider = Slider(SCREEN_WIDTH // 2 - 200, start_y + spacing * 3, 400, 2, 15,
                                        self.ball_count, "Initial Ball Count")
        
        # Чекбокс комбо
        self.combo_checkbox = Checkbox(SCREEN_WIDTH // 2 - 100, start_y + spacing * 4,
                                      "Enable Combo System", self.combo_enabled)
    
    def update_from_ui(self):
        """Обновляет настройки из элементов UI."""
        self.timeout = self.timeout_slider.value
        self.speed_multiplier = self.speed_slider.value
        self.collisions_enabled = self.collisions_checkbox.checked
        self.ball_count = int(self.ball_count_slider.value)
        self.combo_enabled = self.combo_checkbox.checked
    
    def reset_to_default(self):
        """Сбрасывает настройки к значениям по умолчанию."""
        self.timeout = 5.0
        self.speed_multiplier = 1.0
        self.collisions_enabled = False
        self.ball_count = 2
        self.combo_enabled = True
        
        # Обновляем элементы UI
        self.timeout_slider.value = self.timeout
        self.speed_slider.value = self.speed_multiplier
        self.collisions_checkbox.checked = self.collisions_enabled
        self.ball_count_slider.value = self.ball_count
        self.combo_checkbox.checked = self.combo_enabled
    
    def draw(self, surface):
        """Рисует меню настроек."""
        if not self.visible:
            return
        
        # Полупрозрачный фон
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # Заголовок
        font = pygame.font.Font(None, 48)
        title = font.render("GAME SETTINGS", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        surface.blit(title, title_rect)
        
        # Рисуем элементы управления
        self.timeout_slider.draw(surface)
        self.speed_slider.draw(surface)
        self.collisions_checkbox.draw(surface)
        self.ball_count_slider.draw(surface)
        self.combo_checkbox.draw(surface)
        
        # Рисуем кнопки
        self.back_button.draw(surface)
        self.apply_button.draw(surface)
        self.reset_button.draw(surface)
        
        # Информация о текущих настройках
        info_font = pygame.font.Font(None, 24)
        info_text = info_font.render("Adjust settings and click 'Apply Settings' to see changes in game", 
                                     True, LIGHT_GRAY)
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        surface.blit(info_text, info_rect)
    
    def handle_event(self, event):
        """Обрабатывает события в меню."""
        if not self.visible:
            return None
        
        # Обрабатываем слайдеры
        self.timeout_slider.handle_event(event)
        self.speed_slider.handle_event(event)
        self.ball_count_slider.handle_event(event)
        
        # Обрабатываем чекбоксы
        self.collisions_checkbox.handle_event(event)
        self.combo_checkbox.handle_event(event)
        
        # Обрабатываем кнопки
        if self.apply_button.handle_event(event):
            self.update_from_ui()
            return "apply"
        
        if self.reset_button.handle_event(event):
            self.reset_to_default()
            return "reset"
        
        if self.back_button.handle_event(event):
            self.visible = False
            return "close"
        
        return None


class Ball:
    """Класс шарика."""
    
    def __init__(self, x=None, y=None, r=None, vx=None, vy=None, color=None):
        self.x = x if x is not None else randint(50, SCREEN_WIDTH - 50)
        self.y = y if y is not None else randint(50, SCREEN_HEIGHT - 50)
        self.r = r if r is not None else randint(15, 40)
        self.vx = vx if vx is not None else randint(-5, 5)
        self.vy = vy if vy is not None else randint(-5, 5)
        
        while self.vx == 0 and self.vy == 0:
            self.vx = randint(-5, 5)
            self.vy = randint(-5, 5)
        
        self.color = color if color is not None else choice(COLORS)
        self.explosion_particles = []

    def move(self):
        """Движение шарика с отражением."""
        self.x += self.vx
        self.y += self.vy

        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx
        elif self.x + self.r >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.r
            self.vx = -self.vx

        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = -self.vy
        elif self.y + self.r >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.r
            self.vy = -self.vy

    def draw(self, surface):
        """Рисует шарик с бликом."""
        circle(surface, self.color, (self.x, self.y), self.r)
        circle(surface, WHITE, (self.x - self.r//3, self.y - self.r//3), self.r//5)

    def contains_point(self, px, py):
        """Проверяет попадание."""
        distance = math.hypot(px - self.x, py - self.y)
        return distance <= self.r

    def collide_with_ball(self, other):
        """Столкновение шаров."""
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        min_dist = self.r + other.r

        if distance < min_dist:
            if distance == 0:
                distance = 1
            overlap = min_dist - distance
            angle = math.atan2(dy, dx)
            self.x += math.cos(angle) * (overlap / 2)
            self.y += math.sin(angle) * (overlap / 2)
            other.x -= math.cos(angle) * (overlap / 2)
            other.y -= math.sin(angle) * (overlap / 2)

            # Обмен скоростями
            self.vx, other.vx = other.vx, self.vx
            self.vy, other.vy = other.vy, self.vy


class Particle:
    """Класс частицы для эффектов."""
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        self.color = color
        self.lifetime = 20
        self.size = randint(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
    
    def draw(self, surface):
        if self.lifetime > 0:
            circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class Game:
    """Основной класс игры."""
    
    def __init__(self):
        self.settings = SettingsMenu()
        self.reset_game()
        self.running = True
        self.paused = False
        self.show_menu = False
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def reset_game(self):
        """Сбрасывает игру с текущими настройками."""
        self.balls = []
        self.score = 0
        self.level = 1
        self.combo_counter = 0
        self.idle_timer = 0
        self.total_clicks = 0
        self.perfect_hits = 0
        self.create_initial_balls()
    
    def create_initial_balls(self):
        """Создает шары с учетом настроек."""
        self.balls.clear()
        ball_count = self.settings.ball_count
        
        for _ in range(ball_count):
            vx = int(randint(-5, 5) * self.settings.speed_multiplier)
            vy = int(randint(-5, 5) * self.settings.speed_multiplier)
            while vx == 0 and vy == 0:
                vx = int(randint(-5, 5) * self.settings.speed_multiplier)
                vy = int(randint(-5, 5) * self.settings.speed_multiplier)
            
            ball = Ball(vx=vx, vy=vy)
            self.balls.append(ball)
    
    def handle_click(self, pos):
        """Обрабатывает клик."""
        self.total_clicks += 1
        self.idle_timer = 0
        
        hit_ball = None
        for ball in self.balls:
            if ball.contains_point(pos[0], pos[1]):
                hit_ball = ball
                break
        
        if hit_ball:
            # Попадание
            combo_multipliers = [1, 2, 3, 5, 10]
            combo_index = min(self.combo_counter, 4)
            points = 10 * combo_multipliers[combo_index]
            
            if self.settings.combo_enabled:
                self.score += points
                self.combo_counter += 1
            else:
                self.score += 10
                self.combo_counter = 0
            
            self.perfect_hits += 1
            
            # Удаляем шарик
            self.balls.remove(hit_ball)
            
            # Создаем 2 новых шарика
            max_balls = min(30, self.settings.ball_count * 3)
            if len(self.balls) < max_balls:
                for _ in range(2):
                    vx = int(randint(-7, 7) * self.settings.speed_multiplier)
                    vy = int(randint(-7, 7) * self.settings.speed_multiplier)
                    new_ball = Ball(vx=vx, vy=vy)
                    self.balls.append(new_ball)
            
            # Проверка уровня
            level_thresholds = [0, 100, 300, 600, 1000]
            if self.level < 5 and self.score >= level_thresholds[self.level]:
                self.level += 1
                self.combo_counter = 0
        else:
            # Промах
            self.combo_counter = 0
    
    def update(self, dt):
        """Обновляет состояние игры."""
        if self.show_menu or self.paused:
            return
        
        # Таймер бездействия
        if self.balls:
            timeout_ms = self.settings.timeout * 1000
            self.idle_timer += dt
            if self.idle_timer >= timeout_ms:
                self.balls.clear()
                self.combo_counter = 0
                self.create_initial_balls()
                self.idle_timer = 0
                self.score = max(0, self.score - 20)
        
        # Движение шаров
        for ball in self.balls:
            ball.move()
        
        # Коллизии
        if self.settings.collisions_enabled:
            for i in range(len(self.balls)):
                for j in range(i + 1, len(self.balls)):
                    self.balls[i].collide_with_ball(self.balls[j])
        
        # Проверка на пустоту
        if not self.balls:
            self.create_initial_balls()
    
    def draw(self):
        """Рисует игру."""
        screen.fill(BLACK)
        
        # Рисуем шары
        for ball in self.balls:
            ball.draw(screen)
        
        # Интерфейс
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        
        if self.settings.combo_enabled:
            combo_multipliers = [1, 2, 3, 5, 10]
            combo_index = min(self.combo_counter, 4)
            combo_color = WHITE if combo_index < 2 else ORANGE if combo_index < 4 else YELLOW
            combo_text = self.font.render(f"Combo: x{combo_multipliers[combo_index]}", True, combo_color)
            combo_count_text = self.small_font.render(f"({self.combo_counter} hits)", True, WHITE)
            screen.blit(combo_count_text, (150, 96))
        
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        if self.settings.combo_enabled:
            screen.blit(combo_text, (10, 90))
        
        # Информация о настройках
        info_text = self.small_font.render("Press ESC for settings", True, GRAY)
        screen.blit(info_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30))
        
        # Таймер
        if self.balls:
            remaining = max(0, (self.settings.timeout * 1000 - self.idle_timer) / 1000)
            timer_text = self.small_font.render(f"Timeout: {remaining:.1f}s", True, WHITE)
            screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))
    
    def handle_event(self, event):
        """Обрабатывает события."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.show_menu = not self.show_menu
                if self.show_menu:
                    self.settings.visible = True
                else:
                    self.settings.visible = False
            elif event.key == pygame.K_SPACE and not self.show_menu:
                self.reset_game()
        
        if self.show_menu:
            result = self.settings.handle_event(event)
            if result == "apply":
                self.reset_game()
            elif result == "close":
                self.show_menu = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)
    
    def run(self):
        """Главный цикл игры."""
        while self.running:
            dt = clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)
            
            if not self.show_menu:
                self.update(dt)
                self.draw()
            else:
                self.settings.draw(screen)
            
            pygame.display.update()
        
        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()