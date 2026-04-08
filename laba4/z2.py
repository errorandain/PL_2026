import pygame
from pygame.draw import *
from random import randint, choice
import math
import sys

# --- Инициализация Pygame ---
pygame.init()

# --- Константы экрана и времени ---
SCREEN_WIDTH = 1000
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
GOLD = (255, 215, 0)

COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# --- Настройки экрана ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Поймай шарик - Режимы игры")
clock = pygame.time.Clock()

# --- Параметры уровней для режима "По уровням" ---
LEVEL_CONFIG = {
    1: {"balls": 2, "score_needed": 100, "speed": 1.0, "timeout": 5.0, "collisions": False},
    2: {"balls": 4, "score_needed": 300, "speed": 1.2, "timeout": 4.0, "collisions": False},
    3: {"balls": 6, "score_needed": 600, "speed": 1.5, "timeout": 3.5, "collisions": True},
    4: {"balls": 8, "score_needed": 1000, "speed": 2.0, "timeout": 3.0, "collisions": True},
    5: {"balls": 10, "score_needed": 1500, "speed": 2.5, "timeout": 2.5, "collisions": True}
}


class Button:
    """Класс кнопки."""
    
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=LIGHT_GRAY, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        font = pygame.font.Font(None, 28)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False


class Slider:
    """Класс ползунка."""
    
    def __init__(self, x, y, width, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        self.knob_radius = 8
        
    def draw(self, surface):
        font = pygame.font.Font(None, 24)
        label_text = font.render(f"{self.label}: {self.value:.1f}", True, WHITE)
        surface.blit(label_text, (self.rect.x, self.rect.y - 22))
        
        pygame.draw.line(surface, WHITE, (self.rect.x, self.rect.y + 10), 
                        (self.rect.x + self.rect.width, self.rect.y + 10), 2)
        
        knob_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        knob_pos = (knob_x, self.rect.y + 10)
        
        pygame.draw.circle(surface, ORANGE, (int(knob_pos[0]), int(knob_pos[1])), self.knob_radius)
        pygame.draw.circle(surface, WHITE, (int(knob_pos[0]), int(knob_pos[1])), self.knob_radius, 2)
    
    def handle_event(self, event):
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
    """Класс чекбокса."""
    
    def __init__(self, x, y, label, initial_state=False):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.label = label
        self.checked = initial_state
        self.is_hovered = False
    
    def draw(self, surface):
        font = pygame.font.Font(None, 24)
        label_text = font.render(self.label, True, WHITE)
        surface.blit(label_text, (self.rect.x + 25, self.rect.y - 2))
        
        color = LIGHT_GRAY if self.is_hovered else WHITE
        pygame.draw.rect(surface, color, self.rect, 2)
        
        if self.checked:
            pygame.draw.line(surface, GREEN, (self.rect.x + 3, self.rect.y + 9), 
                           (self.rect.x + 7, self.rect.y + 14), 2)
            pygame.draw.line(surface, GREEN, (self.rect.x + 7, self.rect.y + 14), 
                           (self.rect.x + 15, self.rect.y + 3), 2)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                self.checked = not self.checked
                return True
        return False


class ModeSelectionMenu:
    """Меню выбора режима игры."""
    
    def __init__(self):
        self.visible = True
        self.selected_mode = None
        
        self.levels_mode_btn = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 80, 300, 60,
                                      "🏆 LEVELS MODE 🏆", GOLD, YELLOW, BLACK)
        self.custom_mode_btn = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20, 300, 60,
                                      "⚙️ CUSTOM MODE ⚙️", ORANGE, YELLOW, BLACK)
        self.quit_btn = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50,
                              "QUIT", RED, LIGHT_GRAY, WHITE)
    
    def draw(self, surface):
        surface.fill(BLACK)
        
        font_big = pygame.font.Font(None, 64)
        title = font_big.render("CATCH THE BALL", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(title, title_rect)
        
        font_small = pygame.font.Font(None, 28)
        subtitle = font_small.render("Choose your game mode", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 220))
        surface.blit(subtitle, subtitle_rect)
        
        levels_desc = font_small.render("• Progressive difficulty • Auto level up • 5 levels • Infinite play on max level", True, GRAY)
        levels_desc_rect = levels_desc.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        surface.blit(levels_desc, levels_desc_rect)
        
        custom_desc = font_small.render("• Fully customizable • Your rules • No level limits", True, GRAY)
        custom_desc_rect = custom_desc.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        surface.blit(custom_desc, custom_desc_rect)
        
        self.levels_mode_btn.draw(surface)
        self.custom_mode_btn.draw(surface)
        self.quit_btn.draw(surface)
    
    def handle_event(self, event):
        if self.levels_mode_btn.handle_event(event):
            self.selected_mode = "levels"
            self.visible = False
            return "levels"
        elif self.custom_mode_btn.handle_event(event):
            self.selected_mode = "custom"
            self.visible = False
            return "custom"
        elif self.quit_btn.handle_event(event):
            return "quit"
        return None


class SettingsMenu:
    """Меню настроек для пользовательского режима."""
    
    def __init__(self):
        self.visible = False
        
        self.timeout = 5.0
        self.speed_multiplier = 1.0
        self.collisions_enabled = False
        self.ball_count = 2
        self.combo_enabled = True
        
        self.create_ui_elements()
        
        self.back_button = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 70, 160, 40, 
                                  "Back to Game", GREEN, LIGHT_GRAY)
        self.apply_button = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 120, 160, 40,
                                  "Apply Settings", ORANGE, LIGHT_GRAY)
        self.reset_button = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 170, 160, 40,
                                  "Reset to Default", RED, LIGHT_GRAY)
        self.quit_button = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 220, 160, 40,
                                 "Quit Game", GRAY, LIGHT_GRAY)
    
    def create_ui_elements(self):
        start_y = 100
        spacing = 65
        
        self.timeout_slider = Slider(SCREEN_WIDTH // 2 - 150, start_y, 300, 1, 15, 
                                     self.timeout, "Timeout (seconds)")
        self.speed_slider = Slider(SCREEN_WIDTH // 2 - 150, start_y + spacing, 300, 0.5, 3.0,
                                   self.speed_multiplier, "Speed Multiplier")
        self.collisions_checkbox = Checkbox(SCREEN_WIDTH // 2 - 80, start_y + spacing * 2,
                                           "Enable Ball Collisions", self.collisions_enabled)
        self.ball_count_slider = Slider(SCREEN_WIDTH // 2 - 150, start_y + spacing * 3, 300, 2, 15,
                                        self.ball_count, "Initial Ball Count")
        self.combo_checkbox = Checkbox(SCREEN_WIDTH // 2 - 80, start_y + spacing * 4,
                                      "Enable Combo System", self.combo_enabled)
    
    def update_from_ui(self):
        self.timeout = self.timeout_slider.value
        self.speed_multiplier = self.speed_slider.value
        self.collisions_enabled = self.collisions_checkbox.checked
        self.ball_count = int(self.ball_count_slider.value)
        self.combo_enabled = self.combo_checkbox.checked
    
    def reset_to_default(self):
        self.timeout = 5.0
        self.speed_multiplier = 1.0
        self.collisions_enabled = False
        self.ball_count = 2
        self.combo_enabled = True
        
        self.timeout_slider.value = self.timeout
        self.speed_slider.value = self.speed_multiplier
        self.collisions_checkbox.checked = self.collisions_enabled
        self.ball_count_slider.value = self.ball_count
        self.combo_checkbox.checked = self.combo_enabled
    
    def draw(self, surface):
        if not self.visible:
            return
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 48)
        title = font.render("CUSTOM MODE SETTINGS", True, ORANGE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
        surface.blit(title, title_rect)
        
        self.timeout_slider.draw(surface)
        self.speed_slider.draw(surface)
        self.collisions_checkbox.draw(surface)
        self.ball_count_slider.draw(surface)
        self.combo_checkbox.draw(surface)
        
        self.back_button.draw(surface)
        self.apply_button.draw(surface)
        self.reset_button.draw(surface)
        self.quit_button.draw(surface)
        
        info_font = pygame.font.Font(None, 20)
        info_text = info_font.render("Adjust any settings to create your perfect game experience", 
                                     True, LIGHT_GRAY)
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25))
        surface.blit(info_text, info_rect)
    
    def handle_event(self, event):
        if not self.visible:
            return None
        
        self.timeout_slider.handle_event(event)
        self.speed_slider.handle_event(event)
        self.ball_count_slider.handle_event(event)
        self.collisions_checkbox.handle_event(event)
        self.combo_checkbox.handle_event(event)
        
        if self.apply_button.handle_event(event):
            self.update_from_ui()
            return "apply"
        if self.reset_button.handle_event(event):
            self.reset_to_default()
            return "reset"
        if self.back_button.handle_event(event):
            self.visible = False
            return "close"
        if self.quit_button.handle_event(event):
            return "quit"
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

    def move(self):
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
        circle(surface, self.color, (self.x, self.y), self.r)
        circle(surface, WHITE, (self.x - self.r//3, self.y - self.r//3), self.r//5)

    def contains_point(self, px, py):
        distance = math.hypot(px - self.x, py - self.y)
        return distance <= self.r

    def collide_with_ball(self, other):
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

            self.vx, other.vx = other.vx, self.vx
            self.vy, other.vy = other.vy, self.vy


class Game:
    """Основной класс игры с поддержкой двух режимов."""
    
    def __init__(self, mode):
        self.mode = mode
        self.settings = SettingsMenu() if mode == "custom" else None
        self.reset_game()
        self.running = True
        self.show_menu = False
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)
        self.current_level = 1
        self.max_level_reached = False  # Флаг достижения максимального уровня
    
    def reset_game(self):
        """Сбрасывает игру."""
        self.balls = []
        self.score = 0
        self.combo_counter = 0
        self.idle_timer = 0
        self.total_clicks = 0
        self.perfect_hits = 0
        
        if self.mode == "levels":
            self.current_level = 1
            self.max_level_reached = False
            self.create_level_balls()
        else:
            self.create_custom_balls()
    
    def create_level_balls(self):
        """Создает шары для режима уровней."""
        self.balls.clear()
        
        # Если достигнут 5 уровень, используем конфигурацию 5 уровня
        if self.current_level > 5:
            config = LEVEL_CONFIG[5]
        else:
            config = LEVEL_CONFIG[self.current_level]
        
        ball_count = config["balls"]
        
        for _ in range(ball_count):
            vx = int(randint(-5, 5) * config["speed"])
            vy = int(randint(-5, 5) * config["speed"])
            while vx == 0 and vy == 0:
                vx = int(randint(-5, 5) * config["speed"])
                vy = int(randint(-5, 5) * config["speed"])
            
            ball = Ball(vx=vx, vy=vy)
            self.balls.append(ball)
    
    def create_custom_balls(self):
        """Создает шары для пользовательского режима."""
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
    
    def get_current_config(self):
        """Получает текущую конфигурацию для режима уровней."""
        if self.current_level > 5:
            return LEVEL_CONFIG[5]
        return LEVEL_CONFIG[self.current_level]
    
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
            
            if self.mode == "custom" and not self.settings.combo_enabled:
                points = 10
            
            self.score += points
            self.combo_counter += 1
            self.perfect_hits += 1
            
            self.balls.remove(hit_ball)
            
            # Создаем новые шары
            if self.mode == "levels":
                config = self.get_current_config()
                max_balls = min(30, config["balls"] * 3)
                if len(self.balls) < max_balls:
                    for _ in range(2):
                        vx = int(randint(-7, 7) * config["speed"])
                        vy = int(randint(-7, 7) * config["speed"])
                        new_ball = Ball(vx=vx, vy=vy)
                        self.balls.append(new_ball)
            else:
                max_balls = min(30, self.settings.ball_count * 3)
                if len(self.balls) < max_balls:
                    for _ in range(2):
                        vx = int(randint(-7, 7) * self.settings.speed_multiplier)
                        vy = int(randint(-7, 7) * self.settings.speed_multiplier)
                        new_ball = Ball(vx=vx, vy=vy)
                        self.balls.append(new_ball)
            
            # Проверка перехода уровня (только для режима уровней)
            if self.mode == "levels":
                # Если уже на 5 уровне или выше, не проверяем переход
                if self.current_level <= 5:
                    needed_score = LEVEL_CONFIG[self.current_level]["score_needed"]
                    if self.score >= needed_score:
                        self.current_level += 1
                        self.combo_counter = 0
                        
                        # Если перешли на 5 уровень, показываем сообщение
                        if self.current_level == 5:
                            print("🏆 MAXIMUM LEVEL REACHED! Now playing on hardest difficulty! 🏆")
                        elif self.current_level > 5:
                            print("🌟 MASTER MODE! Continuing on maximum difficulty! 🌟")
                        
                        self.create_level_balls()
        else:
            # Промах
            self.combo_counter = 0
    
    def update(self, dt):
        """Обновляет состояние игры."""
        if self.show_menu:
            return
        
        # Таймер бездействия
        if self.balls:
            if self.mode == "levels":
                config = self.get_current_config()
                timeout = config["timeout"] * 1000
            else:
                timeout = self.settings.timeout * 1000
            
            self.idle_timer += dt
            if self.idle_timer >= timeout:
                self.balls.clear()
                self.combo_counter = 0
                if self.mode == "levels":
                    self.create_level_balls()
                else:
                    self.create_custom_balls()
                self.idle_timer = 0
                self.score = max(0, self.score - 20)
        
        # Движение шаров
        for ball in self.balls:
            ball.move()
        
        # Коллизии
        if self.mode == "levels":
            config = self.get_current_config()
            collisions_enabled = config["collisions"]
        else:
            collisions_enabled = self.settings.collisions_enabled
        
        if collisions_enabled:
            for i in range(len(self.balls)):
                for j in range(i + 1, len(self.balls)):
                    self.balls[i].collide_with_ball(self.balls[j])
        
        if not self.balls:
            if self.mode == "levels":
                self.create_level_balls()
            else:
                self.create_custom_balls()
    
    def draw(self):
        """Рисует игру."""
        screen.fill(BLACK)
        
        for ball in self.balls:
            ball.draw(screen)
        
        # Интерфейс
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if self.mode == "levels":
            # Отображение уровня
            if self.current_level > 5:
                level_text = self.font.render(f"Level: MASTER (∞)", True, GOLD)
                screen.blit(level_text, (10, 45))
                
                # Информация о максимальной сложности
                master_text = self.small_font.render("MAXIMUM DIFFICULTY - INFINITE MODE", True, ORANGE)
                screen.blit(master_text, (10, 80))
            else:
                level_text = self.font.render(f"Level: {self.current_level}/5", True, GOLD)
                screen.blit(level_text, (10, 45))
                
                # Информация о следующем уровне
                if self.current_level < 5:
                    next_score = LEVEL_CONFIG[self.current_level]["score_needed"]
                    need = next_score - self.score
                    next_text = self.small_font.render(f"Next level: {need} points", True, GRAY)
                    screen.blit(next_text, (10, 80))
        else:
            mode_text = self.font.render("CUSTOM MODE", True, ORANGE)
            screen.blit(mode_text, (10, 45))
        
        # Комбо
        if self.mode == "custom" and not self.settings.combo_enabled:
            combo_text = self.small_font.render("Combo: OFF", True, GRAY)
            combo_y = 80 if self.mode == "levels" else 110
            screen.blit(combo_text, (10, combo_y))
        else:
            combo_multipliers = [1, 2, 3, 5, 10]
            combo_index = min(self.combo_counter, 4)
            combo_color = WHITE if combo_index < 2 else ORANGE if combo_index < 4 else GOLD
            combo_text = self.font.render(f"Combo: x{combo_multipliers[combo_index]}", True, combo_color)
            combo_count_text = self.small_font.render(f"({self.combo_counter} hits)", True, WHITE)
            
            if self.mode == "levels":
                base_y = 80 if self.current_level <= 5 else 115
                screen.blit(combo_text, (10, base_y))
                screen.blit(combo_count_text, (150, base_y + 4))
            else:
                screen.blit(combo_text, (10, 110))
                screen.blit(combo_count_text, (150, 114))
        
        # Информация
        info_text = self.small_font.render("ESC - Settings | SPACE - Restart | X - Quit", True, GRAY)
        screen.blit(info_text, (SCREEN_WIDTH - 280, SCREEN_HEIGHT - 25))
        
        # Таймер
        if self.balls:
            if self.mode == "levels":
                config = self.get_current_config()
                remaining = max(0, config["timeout"] - self.idle_timer / 1000)
                timer_text = self.small_font.render(f"Timeout: {remaining:.1f}s", True, WHITE)
            else:
                remaining = max(0, self.settings.timeout - self.idle_timer / 1000)
                timer_text = self.small_font.render(f"Timeout: {remaining:.1f}s", True, WHITE)
            screen.blit(timer_text, (SCREEN_WIDTH - 120, 10))
    
    def handle_event(self, event):
        """Обрабатывает события."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.mode == "custom":
                    self.show_menu = not self.show_menu
                    if self.show_menu:
                        self.settings.visible = True
                    else:
                        self.settings.visible = False
            elif event.key == pygame.K_SPACE:
                self.reset_game()
        
        if self.mode == "custom" and self.show_menu:
            result = self.settings.handle_event(event)
            if result == "apply":
                self.reset_game()
            elif result == "close":
                self.show_menu = False
            elif result == "quit":
                self.running = False
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
            
            if self.mode == "custom" and self.show_menu:
                self.settings.draw(screen)
            else:
                self.update(dt)
                self.draw()
            
            pygame.display.update()
        
        pygame.quit()
        sys.exit()


def main():
    """Главная функция."""
    mode_menu = ModeSelectionMenu()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            result = mode_menu.handle_event(event)
            if result == "levels":
                game = Game("levels")
                game.run()
                mode_menu.visible = True
                mode_menu.selected_mode = None
            elif result == "custom":
                game = Game("custom")
                game.run()
                mode_menu.visible = True
                mode_menu.selected_mode = None
            elif result == "quit":
                pygame.quit()
                sys.exit()
        
        mode_menu.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()