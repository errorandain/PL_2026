import math
import random
import pygame
from abc import ABC, abstractmethod

FPS = 30

# Расширенная палитра цветов
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
ORANGE = 0xFFA500
PURPLE = 0x800080
PINK = 0xFF69B4
BROWN = 0x8B4513
LIGHT_BLUE = 0x87CEEB
DARK_GREEN = 0x006400
GOLD = 0xFFD700
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
DARK_GREY = 0x404040
NAVY = 0x000080
MAROON = 0x800000

GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, ORANGE, PURPLE, PINK, GOLD]
TARGET_COLORS = [RED, ORANGE, PURPLE, (255, 100, 100), (255, 165, 0), DARK_GREEN]

WIDTH = 800
HEIGHT = 600

# =====================================================
# РЕФАКТОРИНГ: Создание базового класса для игровых объектов
# Устраняет дублирование кода (x, y, screen, параметры движения)
# =====================================================

class GameObject(ABC):
    """Базовый класс для всех игровых объектов.
    Рефакторинг: вынесены общие свойства (screen, x, y) в отдельный класс."""
    
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.live = True
    
    @abstractmethod
    def move(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass


class MovableObject(GameObject):
    """Базовый класс для движущихся объектов с физикой.
    Рефакторинг: общая логика движения вынесена в отдельный класс."""
    
    def __init__(self, screen, x, y, vx=0, vy=0):
        super().__init__(screen, x, y)
        self.vx = vx
        self.vy = vy
        self.gravity = 0.5
        self.friction = 0.98
    
    def apply_physics(self):
        """Применение физики движения."""
        self.vy -= self.gravity
        self.x += self.vx
        self.y -= self.vy
        self.vx *= self.friction
        self.vy *= self.friction
    
    def check_bounds(self, left=0, right=WIDTH, top=0, bottom=HEIGHT):
        """Проверка выхода за границы и отскок."""
        bounced = False
        if self.x < left:
            self.x = left
            self.vx = abs(self.vx) * 0.8
            bounced = True
        elif self.x > right:
            self.x = right
            self.vx = -abs(self.vx) * 0.8
            bounced = True
        
        if self.y < top:
            self.y = top
            self.vy = -abs(self.vy) * 0.8
            bounced = True
        elif self.y > bottom:
            self.y = bottom
            self.vy = abs(self.vy) * 0.5
            self.vx *= 0.85
            bounced = True
        
        return bounced


# =====================================================
# РЕФАКТОРИНГ: Различные типы снарядов
# Комментарий: Расширение класса Ball до иерархии снарядов
# =====================================================

class Projectile(MovableObject):
    """Базовый класс для всех типов снарядов.
    Рефакторинг: объединение общей логики снарядов."""
    
    def __init__(self, screen, x, y, vx, vy, color=None, radius=10):
        super().__init__(screen, x, y, vx, vy)
        self.r = radius
        self.color = color if color else random.choice(GAME_COLORS)
        self.stopped = False
        self.stop_timer = 0
        self.bounce_count = 0
        self.max_bounces = 3
        self.trail = []  # След от снаряда
        self.hit_target = False
        self.damage = 1
        self.explosion_radius = 0
        self.explosion_particles = 10
    
    def move(self):
        if self.stopped:
            self.stop_timer += 1
            return
        
        # Сохраняем след
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop(0)
        
        self.apply_physics()
        
        # Обработка границ
        if self.check_bounds(0, WIDTH, 0, HEIGHT):
            self.bounce_count += 1
            if self.bounce_count >= self.max_bounces:
                self.vy = 0
                self.vx = 0
                self.stopped = True
                self.live = False
        
        if not self.stopped and abs(self.vx) < 0.1 and abs(self.vy) < 0.1:
            self.stopped = True
            self.live = False
    
    def draw(self):
        # Отрисовка следа
        for i, pos in enumerate(self.trail):
            alpha = i / len(self.trail) * 0.7
            if isinstance(self.color, int):
                r = ((self.color >> 16) & 0xFF)
                g = ((self.color >> 8) & 0xFF)
                b = (self.color & 0xFF)
                trail_color = (int(r * alpha), int(g * alpha), int(b * alpha))
            else:
                trail_color = tuple(int(c * alpha) for c in self.color)
            pygame.draw.circle(self.screen, trail_color, 
                             (int(pos[0]), int(pos[1])), int(self.r * alpha))
        
        # Основной круг
        pygame.draw.circle(self.screen, self.color, 
                         (int(self.x), int(self.y)), self.r)
        # Блик
        pygame.draw.circle(self.screen, WHITE, 
                         (int(self.x - 3), int(self.y - 3)), 4)
        
        # Обводка для остановившихся
        if self.stopped:
            pygame.draw.circle(self.screen, BLACK, 
                             (int(self.x), int(self.y)), self.r, 2)
    
    def hittest(self, obj):
        """Проверка столкновения с объектом."""
        if not self.live or self.stopped:
            return False
        dx = self.x - obj.x
        dy = self.y - obj.y
        distance = math.hypot(dx, dy)
        return distance <= self.r + obj.r
    
    def should_remove(self):
        """Нужно ли удалить снаряд."""
        if self.stopped and self.stop_timer > 120:
            return True
        if self.x < -100 or self.x > WIDTH + 100 or self.y > HEIGHT + 100:
            return True
        return False


class NormalBullet(Projectile):
    """Обычный снаряд - базовый тип.
    Комментарий: добавлен новый тип снаряда."""
    
    def __init__(self, screen, x, y, vx, vy):
        color = random.choice(GAME_COLORS)
        super().__init__(screen, x, y, vx, vy, color, radius=10)
        self.damage = 1
        self.explosion_particles = 10


class HeavyBullet(Projectile):
    """Тяжелый снаряд - большой урон, взрывной радиус.
    Комментарий: добавлен новый тип снаряда."""
    
    def __init__(self, screen, x, y, vx, vy):
        super().__init__(screen, x, y, vx * 0.7, vy * 0.7, MAROON, radius=18)
        self.damage = 3
        self.gravity = 0.8
        self.max_bounces = 1
        self.explosion_particles = 25
        self.explosion_radius = 30
    
    def draw(self):
        super().draw()
        # Дополнительный эффект для тяжелого снаряда
        pygame.draw.circle(self.screen, YELLOW, 
                         (int(self.x), int(self.y)), self.r + 3, 2)


class FireBullet(Projectile):
    """Зажигательный снаряд - поджигает цели.
    Комментарий: добавлен новый тип снаряда."""
    
    def __init__(self, screen, x, y, vx, vy):
        super().__init__(screen, x, y, vx * 1.2, vy * 1.2, ORANGE, radius=12)
        self.damage = 1
        self.burn_damage = 1
        self.burn_duration = 60
        self.explosion_particles = 20
    
    def draw(self):
        super().draw()
        # Эффект пламени
        for i in range(3):
            flame_x = self.x + random.randint(-5, 5)
            flame_y = self.y + random.randint(-5, 5)
            pygame.draw.circle(self.screen, YELLOW, 
                             (int(flame_x), int(flame_y)), 
                             random.randint(3, self.r))


class SplitBullet(Projectile):
    """Разделяющийся снаряд - делится при попадании.
    Комментарий: добавлен новый тип снаряда."""
    
    def __init__(self, screen, x, y, vx, vy):
        super().__init__(screen, x, y, vx, vy, GREEN, radius=8)
        self.damage = 1
        self.explosion_particles = 5
        self.splits_into = 3


class ProjectileFactory:
    """Фабрика для создания снарядов.
    Рефакторинг: применение паттерна Фабрика."""
    
    @staticmethod
    def create_projectile(projectile_type, screen, x, y, power, angle, spread=0):
        """Создание снаряда указанного типа."""
        angle += spread
        vx = power * math.cos(angle)
        vy = -power * math.sin(angle)
        
        if projectile_type == "normal":
            return NormalBullet(screen, x, y, vx, vy)
        elif projectile_type == "heavy":
            return HeavyBullet(screen, x, y, vx, vy)
        elif projectile_type == "fire":
            return FireBullet(screen, x, y, vx, vy)
        elif projectile_type == "split":
            return SplitBullet(screen, x, y, vx, vy)
        else:
            return NormalBullet(screen, x, y, vx, vy)


# =====================================================
# РЕФАКТОРИНГ: Иерархия целей с разным поведением движения
# Комментарий: вместо одного класса Target - иерархия с разным движением
# =====================================================

class TargetBase(MovableObject):
    """Базовый класс для всех типов целей.
    Рефакторинг: общая логика целей вынесена в базовый класс."""
    
    def __init__(self, screen, x=None, y=None, radius=25):
        x = x if x is not None else random.randint(100, 700)
        y = y if y is not None else random.randint(100, 500)
        super().__init__(screen, x, y)
        self.r = radius
        self.points = 0
        self.hits_to_die = 1
        self.current_hits = 0
        self.color = RED
        self.rotation = 0
        self.burn_timer = 0
        self.burn_damage_timer = 0
        self.bomb_timer = random.randint(180, 300)  # Таймер для сброса бомб
    
    def hit(self, damage=1, burn=False):
        """Обработка попадания."""
        self.current_hits += damage
        if burn:
            self.burn_timer = 60
        
        if self.current_hits >= self.hits_to_die:
            self.points += self.calculate_points()
            self.live = False
            return True
        return False
    
    def calculate_points(self):
        """Расчет очков за уничтожение."""
        return 10
    
    def apply_burn_damage(self):
        """Применение урона от горения."""
        if self.burn_timer > 0:
            self.burn_damage_timer -= 1
            if self.burn_damage_timer <= 0:
                self.current_hits += 1
                self.burn_damage_timer = 20
                if self.current_hits >= self.hits_to_die:
                    self.live = False
            self.burn_timer -= 1
    
    def move(self):
        """Движение цели."""
        if self.live:
            self.apply_physics()
            self.check_bounds(0, WIDTH, 0, HEIGHT)
            self.rotation += 5
            self.apply_burn_damage()
            self.bomb_timer -= 1
    
    def draw(self):
        """Отрисовка цели."""
        if self.live:
            pygame.draw.circle(self.screen, self.color, 
                             (int(self.x), int(self.y)), self.r)
            self.draw_special_effects()
            
            # Эффект горения
            if self.burn_timer > 0:
                for _ in range(3):
                    fx = self.x + random.randint(-self.r, self.r)
                    fy = self.y + random.randint(-self.r, self.r)
                    pygame.draw.circle(self.screen, ORANGE, 
                                     (int(fx), int(fy)), 3)
    
    @abstractmethod
    def draw_special_effects(self):
        """Специальные визуальные эффекты."""
        pass
    
    def new_target(self):
        """Сброс цели в новую позицию."""
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 500)
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])
        self.live = True
        self.current_hits = 0
        self.burn_timer = 0
        self.bomb_timer = random.randint(180, 300)
    
    def should_drop_bomb(self):
        """Проверка, должна ли цель сбросить бомбу."""
        if self.bomb_timer <= 0:
            self.bomb_timer = random.randint(180, 300)
            return True
        return False


class NormalTarget(TargetBase):
    """Обычная цель - прямолинейное движение.
    Комментарий: добавлен новый тип цели."""
    
    def __init__(self, screen):
        super().__init__(screen, radius=random.randint(15, 40))
        self.color = random.choice(TARGET_COLORS)
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])
    
    def draw_special_effects(self):
        angle = math.radians(self.rotation)
        inner_x = self.x + self.r * 0.3 * math.cos(angle)
        inner_y = self.y + self.r * 0.3 * math.sin(angle)
        pygame.draw.circle(self.screen, BLACK, (int(inner_x), int(inner_y)), self.r // 3)
        pygame.draw.circle(self.screen, WHITE, (int(self.x - 5), int(self.y - 5)), 5)
    
    def calculate_points(self):
        return 10


class FastTarget(TargetBase):
    """Быстрая цель - хаотичное движение.
    Комментарий: добавлен новый тип цели."""
    
    def __init__(self, screen):
        super().__init__(screen, radius=18)
        self.color = GREEN
        self.vx = random.choice([-4, -3, 3, 4])
        self.vy = random.choice([-4, -3, 3, 4])
        self.hits_to_die = 2
        self.direction_change_timer = random.randint(30, 90)
    
    def move(self):
        super().move()
        self.direction_change_timer -= 1
        if self.direction_change_timer <= 0:
            self.vx = random.choice([-5, -4, -3, 3, 4, 5])
            self.vy = random.choice([-5, -4, -3, 3, 4, 5])
            self.direction_change_timer = random.randint(30, 90)
    
    def draw_special_effects(self):
        # Эффект скорости
        for i in range(3):
            offset_x = -self.vx * i * 2
            offset_y = -self.vy * i * 2
            pygame.draw.circle(self.screen, (0, int(200 - i*50), 0), 
                             (int(self.x + offset_x), int(self.y + offset_y)), 
                             self.r - i*2)
    
    def calculate_points(self):
        return 25


class ZigzagTarget(TargetBase):
    """Зигзагообразная цель - синусоидальное движение.
    Комментарий: добавлен новый тип цели."""
    
    def __init__(self, screen):
        super().__init__(screen, radius=20)
        self.color = CYAN
        self.vx = 3
        self.vy = 0
        self.amplitude = 3
        self.frequency = 0.05
        self.time = 0
        self.hits_to_die = 2
    
    def move(self):
        if self.live:
            self.time += 1
            self.x += self.vx
            self.y += math.sin(self.time * self.frequency) * self.amplitude
            self.check_bounds(0, WIDTH, 0, HEIGHT)
            self.rotation += 5
            self.apply_burn_damage()
            self.bomb_timer -= 1
    
    def draw_special_effects(self):
        # Отображение траектории
        for i in range(5):
            t = self.time - i * 5
            trail_x = self.x - i * self.vx * 5
            trail_y = self.y - math.sin(t * self.frequency) * self.amplitude
            alpha = 150 - i * 30
            pygame.draw.circle(self.screen, (0, int(200 - i*40), int(200 - i*40)), 
                             (int(trail_x), int(trail_y)), self.r - i*3)
    
    def calculate_points(self):
        return 20


class CircularTarget(TargetBase):
    """Круговая цель - движение по орбите.
    Комментарий: добавлен новый тип цели."""
    
    def __init__(self, screen):
        super().__init__(screen, radius=22)
        self.color = PINK
        self.orbit_center_x = random.randint(200, 600)
        self.orbit_center_y = random.randint(150, 450)
        self.orbit_radius = random.randint(80, 150)
        self.orbit_speed = random.uniform(0.02, 0.05)
        self.orbit_angle = random.uniform(0, 2 * math.pi)
        self.hits_to_die = 3
    
    def move(self):
        if self.live:
            self.orbit_angle += self.orbit_speed
            self.x = self.orbit_center_x + self.orbit_radius * math.cos(self.orbit_angle)
            self.y = self.orbit_center_y + self.orbit_radius * math.sin(self.orbit_angle)
            self.rotation += 3
            self.apply_burn_damage()
            self.bomb_timer -= 1
    
    def draw_special_effects(self):
        # Орбита
        pygame.draw.circle(self.screen, (100, 100, 100), 
                         (self.orbit_center_x, self.orbit_center_y), 
                         self.orbit_radius, 1)
        # Линия к центру
        pygame.draw.line(self.screen, (100, 100, 100), 
                       (self.orbit_center_x, self.orbit_center_y), 
                       (self.x, self.y), 1)
    
    def calculate_points(self):
        return 35
    
    def new_target(self):
        super().new_target()
        self.orbit_center_x = random.randint(200, 600)
        self.orbit_center_y = random.randint(150, 450)
        self.orbit_radius = random.randint(80, 150)
        self.orbit_angle = random.uniform(0, 2 * math.pi)


class BossTarget(TargetBase):
    """Босс - большая цель с большим здоровьем.
    Комментарий: добавлен новый тип цели."""
    
    def __init__(self, screen):
        super().__init__(screen, x=WIDTH//2, y=100, radius=50)
        self.color = PURPLE
        self.vx = 2
        self.vy = 1
        self.hits_to_die = 5
        self.shield_active = False
        self.shield_timer = 0
    
    def move(self):
        if self.live:
            super().move()
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = not self.shield_active
                self.shield_timer = 120 if self.shield_active else 60
    
    def hit(self, damage=1, burn=False):
        if self.shield_active:
            return False
        return super().hit(damage, burn)
    
    def draw_special_effects(self):
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 10
        pygame.draw.circle(self.screen, YELLOW, 
                         (int(self.x), int(self.y)), 
                         int(self.r * 0.6 + pulse))
        pygame.draw.circle(self.screen, BLACK, (int(self.x), int(self.y)), self.r // 3)
        
        # Полоса здоровья
        health_width = int((self.hits_to_die - self.current_hits) / self.hits_to_die * self.r * 2)
        pygame.draw.rect(self.screen, GREEN, 
                       (self.x - self.r, self.y - self.r - 12, health_width, 6))
        pygame.draw.rect(self.screen, WHITE, 
                       (self.x - self.r, self.y - self.r - 12, self.r * 2, 6), 1)
        
        # Щит
        if self.shield_active:
            pygame.draw.circle(self.screen, LIGHT_BLUE, 
                             (int(self.x), int(self.y)), 
                             self.r + 8, 3)
    
    def calculate_points(self):
        return 100


# =====================================================
# БОМБА - новый класс
# Комментарий: реализация функционала бомб
# =====================================================

class Bomb(MovableObject):
    """Бомба, которую сбрасывают цели на пушку."""
    
    def __init__(self, screen, x, y, target_x, target_y):
        super().__init__(screen, x, y)
        self.r = 15
        self.color = RED
        self.target_x = target_x
        self.target_y = target_y
        self.explosion_radius = 50
        self.warning_timer = 30  # Время предупреждения
        self.activated = False
        
        # Расчет скорости к цели
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        speed = 5
        self.vx = (dx / distance) * speed if distance > 0 else 0
        self.vy = (dy / distance) * speed * (-1) if distance > 0 else 0
    
    def move(self):
        if self.warning_timer > 0:
            self.warning_timer -= 1
            return
        
        self.activated = True
        self.x += self.vx
        self.y -= self.vy
        
        # Проверка достижения цели
        if math.hypot(self.x - self.target_x, self.y - self.target_y) < 20:
            self.live = False
    
    def draw(self):
        if self.warning_timer > 0:
            # Предупреждающий индикатор
            alpha = abs(math.sin(pygame.time.get_ticks() * 0.01))
            warning_radius = self.explosion_radius * alpha
            pygame.draw.circle(self.screen, (255, 0, 0, 100), 
                             (self.target_x, self.target_y), 
                             int(warning_radius), 2)
            pygame.draw.circle(self.screen, RED, 
                             (int(self.x), int(self.y)), self.r)
        else:
            # Падающая бомба
            pygame.draw.circle(self.screen, RED, (int(self.x), int(self.y)), self.r)
            pygame.draw.circle(self.screen, YELLOW, (int(self.x), int(self.y)), self.r - 5)
            
            # Хвост
            for i in range(3):
                tail_x = self.x - self.vx * i * 3
                tail_y = self.y + self.vy * i * 3
                tail_r = self.r - i * 3
                pygame.draw.circle(self.screen, ORANGE, 
                                 (int(tail_x), int(tail_y)), max(2, tail_r))
    
    def should_remove(self):
        return not self.live and self.warning_timer <= 0


# =====================================================
# ПУШКА - теперь движущийся объект
# Комментарий: пушка теперь может двигаться
# =====================================================

class Gun:
    """Пушка с возможностью движения.
    Рефакторинг: добавлена возможность перемещения."""
    
    def __init__(self, screen, x=40, y=450, color=GREY, is_player=True):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = color
        self.base_color = color
        self.x = x
        self.y = y
        self.base_y = y  # Базовая позиция Y
        self.ammo = -1  # -1 = бесконечные патроны
        self.reload_time = 0
        self.shake = 0
        self.health = 3
        self.max_health = 3
        self.rapid_fire_timer = 0
        self.triple_shot_timer = 0
        self.invulnerable_timer = 0
        self.is_player = is_player
        
        # Движение
        self.move_speed = 3
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        
        # Текущий тип снаряда
        self.projectile_type = "normal"
        
        # Для AI
        self.ai_shoot_timer = 0
    
    def move(self):
        """Движение пушки."""
        if self.moving_left:
            self.x -= self.move_speed
        if self.moving_right:
            self.x += self.move_speed
        if self.moving_up and self.y > self.base_y - 100:
            self.y -= self.move_speed
        if self.moving_down and self.y < self.base_y:
            self.y += self.move_speed
        
        # Ограничения
        self.x = max(30, min(WIDTH - 30, self.x))
        self.y = max(self.base_y - 100, min(self.base_y, self.y))
    
    def fire2_start(self, event=None):
        if self.ammo > 0 or self.ammo == -1:
            self.f2_on = 1
    
    def fire2_end(self, event=None, target_x=None, target_y=None):
        """Выстрел снаряда."""
        global projectiles, bullet
        
        if (self.ammo > 0 or self.ammo == -1) and self.f2_on:
            if self.ammo > 0:
                self.ammo -= 1
            
            bullet += 1
            bullet_count = 3 if self.triple_shot_timer > 0 else 1
            
            for i in range(bullet_count):
                spread = 0.15 if bullet_count > 1 else 0
                angle_offset = (i - 1) * spread if bullet_count > 1 else 0
                
                if target_x is not None and target_y is not None:
                    self.an = math.atan2((target_y - self.y), (target_x - self.x))
                elif event:
                    self.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
                
                new_proj = ProjectileFactory.create_projectile(
                    self.projectile_type, self.screen,
                    self.x, self.y,
                    self.f2_power,
                    self.an,
                    angle_offset
                )
                projectiles.append(new_proj)
            
            self.shake = 7
        
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
            self.color = self.base_color
    
    def ai_shoot(self, target):
        """AI стрельба по цели."""
        if self.ai_shoot_timer <= 0:
            self.an = math.atan2((target.y - self.y), (target.x - self.x))
            self.fire2_start()
            self.fire2_end(target_x=target.x, target_y=target.y)
            self.ai_shoot_timer = random.randint(30, 90)
        else:
            self.ai_shoot_timer -= 1
    
    def draw(self):
        """Рисование пушки."""
        shake_offset_x = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        shake_offset_y = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        if self.shake > 0:
            self.shake -= 1
        
        power_bonus = self.f2_power if self.f2_on else 0
        end_x = self.x + (50 + power_bonus * 0.3) * math.cos(self.an)
        end_y = self.y + (50 + power_bonus * 0.3) * math.sin(self.an)
        
        # Основание
        base_width = 30
        pygame.draw.rect(self.screen, DARK_GREY,
                       (self.x - base_width, self.base_y - 10, base_width * 2, 15))
        pygame.draw.rect(self.screen, WHITE,
                       (self.x - base_width, self.base_y - 10, base_width * 2, 15), 1)
        
        # Дуло
        pygame.draw.line(self.screen, self.color,
                       (self.x + shake_offset_x, self.y + shake_offset_y),
                       (end_x + shake_offset_x, end_y + shake_offset_y), 7)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 12)
        pygame.draw.circle(self.screen, DARK_GREY, (self.x, self.y), 12, 2)
        
        # Индикатор типа снаряда
        type_colors = {
            "normal": GREY,
            "heavy": MAROON,
            "fire": ORANGE,
            "split": GREEN
        }
        indicator_color = type_colors.get(self.projectile_type, GREY)
        pygame.draw.circle(self.screen, indicator_color, (int(end_x), int(end_y)), 5)
        
        if self.f2_on:
            power_width = int(self.f2_power * 1.5)
            pygame.draw.rect(self.screen, RED,
                           (self.x - 20, self.y - 50, power_width, 8))
            pygame.draw.rect(self.screen, WHITE,
                           (self.x - 20, self.y - 50, 150, 8), 1)
        
        # Полоса здоровья
        self.draw_health_bar()
    
    def draw_health_bar(self):
        """Отрисовка полосы здоровья."""
        bar_width = 150
        bar_height = 15
        x = self.x - bar_width // 2
        y = self.base_y + 15
        
        pygame.draw.rect(self.screen, DARK_GREY, (x, y, bar_width, bar_height))
        health_width = int((self.health / self.max_health) * bar_width)
        health_color = GREEN if self.health > 1 else YELLOW if self.health == 1 else RED
        pygame.draw.rect(self.screen, health_color, (x, y, health_width, bar_height))
        pygame.draw.rect(self.screen, WHITE, (x, y, bar_width, bar_height), 1)
        
        # Подпись
        font = pygame.font.Font(None, 15)
        text = font.render("PLAYER" if self.is_player else "ENEMY", True, WHITE)
        self.screen.blit(text, (x, y - 15))
    
    def power_up(self):
        """Увеличение мощности."""
        if self.f2_on and (self.ammo > 0 or self.ammo == -1):
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = self.base_color
    
    def reload(self):
        """Перезарядка."""
        if self.ammo < 10:
            self.reload_time = 60
    
    def update_reload(self):
        """Обновление перезарядки."""
        if self.reload_time > 0:
            self.reload_time -= 1
            if self.reload_time == 0:
                self.ammo = min(self.ammo + 10, 20)
    
    def take_damage(self, damage=1):
        """Получение урона."""
        if self.invulnerable_timer <= 0:
            self.health -= damage
            self.invulnerable_timer = 60


# =====================================================
# ЧАСТИЦЫ ДЛЯ ЭФФЕКТОВ
# =====================================================

class Particle(MovableObject):
    """Частица для эффекта взрыва."""
    
    def __init__(self, screen, x, y, color=None):
        super().__init__(screen, x, y)
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.color = color if color else random.choice([RED, ORANGE, YELLOW, WHITE])
        self.r = random.randint(2, 6)
        self.life = random.randint(20, 40)
        self.gravity = 0.2
        self.friction = 0.98
    
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 1
        self.vx *= self.friction
        self.vy *= self.friction
    
    def draw(self):
        alpha = self.life / 40
        if isinstance(self.color, int):
            r = (self.color >> 16) & 0xFF
            g = (self.color >> 8) & 0xFF
            b = self.color & 0xFF
            color = (int(r * alpha), int(g * alpha), int(b * alpha))
        else:
            color = tuple(int(c * alpha) for c in self.color)
        pygame.draw.circle(self.screen, color, (int(self.x), int(self.y)), int(self.r * alpha))


# =====================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =====================================================

def draw_text(screen, text, x, y, size=30, color=BLACK, bold=False):
    """Вывод текста на экран."""
    font = pygame.font.Font(None, size)
    if bold:
        font.set_bold(True)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def create_explosion(screen, x, y, particles_list, color=None, count=15):
    """Создание эффекта взрыва."""
    for _ in range(count):
        particles_list.append(Particle(screen, x, y, color))


def draw_stars(screen, stars):
    """Отрисовка звездного фона."""
    for star in stars:
        brightness = int(255 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.001 * star[2])))
        pygame.draw.circle(screen, (brightness, brightness, brightness), (star[0], star[1]), 1)


# =====================================================
# ГЛАВНАЯ ФУНКЦИЯ
# =====================================================

def main():
    global projectiles, bullet
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🔥 ПУШКА: ULTRA v2.0 🔥")
    
    bullet = 0
    projectiles = []
    particles = []
    bombs = []
    
    clock = pygame.time.Clock()
    
    # Создание пушек
    player_gun = Gun(screen, WIDTH // 2, HEIGHT - 100, GREY, True)
    enemy_guns = [
        Gun(screen, 100, 80, NAVY, False),
        Gun(screen, WIDTH - 100, 80, MAROON, False)
    ]
    
    # Настройка вражеских пушек
    for gun in enemy_guns:
        gun.base_y = gun.y
        gun.health = 2
        gun.max_health = 2
        gun.ammo = -1
    
    all_guns = [player_gun] + enemy_guns
    
    # Создание целей разных типов
    targets = [
        NormalTarget(screen),
        FastTarget(screen),
        ZigzagTarget(screen),
        CircularTarget(screen),
        BossTarget(screen)
    ]
    
    total_score = 0
    combo = 0
    combo_timer = 0
    finished = False
    paused = False
    game_over = False
    
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.random()) for _ in range(100)]
    
    while not finished:
        if not paused and not game_over:
            screen.fill(DARK_GREY)
            draw_stars(screen, stars)
            
            # Земля
            pygame.draw.rect(screen, BROWN, (0, HEIGHT - 20, WIDTH, 20))
            pygame.draw.rect(screen, GREEN, (0, HEIGHT - 25, WIDTH, 10))
            
            # Отрисовка всех объектов
            for gun in all_guns:
                gun.draw()
            
            for t in targets:
                t.draw()
            
            for p in projectiles:
                p.draw()
            
            for p in particles:
                p.draw()
            
            for b in bombs:
                b.draw()
            
            # Интерфейс
            draw_text(screen, f"Счёт: {total_score}", 10, 10, 35, WHITE, True)
            draw_text(screen, f"Выстрелов: {bullet}", 10, 45, 25, WHITE)
            
            ammo_color = YELLOW if player_gun.ammo < 5 and player_gun.ammo > 0 else WHITE
            ammo_text = f"Патроны: {player_gun.ammo if player_gun.ammo > 0 else '∞'}"
            draw_text(screen, ammo_text, 10, 75, 25, ammo_color)
            
            # Тип снаряда
            type_names = {"normal": "Обычный", "heavy": "Тяжелый", "fire": "Огненный", "split": "Разделяющийся"}
            draw_text(screen, f"Снаряд: {type_names.get(player_gun.projectile_type, 'Обычный')}", 10, 105, 20, CYAN)
            
            if combo > 1:
                draw_text(screen, f"COMBO x{combo}!", WIDTH - 180, 10, 45, ORANGE, True)
            
            pygame.display.update()
            clock.tick(FPS)
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        player_gun.reload()
                    elif event.key == pygame.K_p:
                        paused = True
                    elif event.key == pygame.K_SPACE:
                        if combo >= 3:
                            for _ in range(5):
                                new_proj = FireBullet(
                                    screen, player_gun.x, player_gun.y,
                                    random.uniform(-25, 25),
                                    random.uniform(-25, 25)
                                )
                                projectiles.append(new_proj)
                            combo = 0
                            create_explosion(screen, player_gun.x, player_gun.y, particles, ORANGE, 30)
                    
                    # Смена типа снаряда
                    elif event.key == pygame.K_1:
                        player_gun.projectile_type = "normal"
                    elif event.key == pygame.K_2:
                        player_gun.projectile_type = "heavy"
                    elif event.key == pygame.K_3:
                        player_gun.projectile_type = "fire"
                    elif event.key == pygame.K_4:
                        player_gun.projectile_type = "split"
                    
                    # Движение пушки
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        player_gun.moving_left = True
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        player_gun.moving_right = True
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        player_gun.moving_up = True
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        player_gun.moving_down = True
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        player_gun.moving_left = False
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        player_gun.moving_right = False
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        player_gun.moving_up = False
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        player_gun.moving_down = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        player_gun.fire2_start(event)
                    elif event.button == 3:
                        player_gun.reload()
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        player_gun.fire2_end(event)
                
                elif event.type == pygame.MOUSEMOTION:
                    player_gun.targetting(event)
            
            # Обновление игрока
            player_gun.move()
            player_gun.update_reload()
            
            if player_gun.rapid_fire_timer > 0:
                player_gun.rapid_fire_timer -= 1
            if player_gun.triple_shot_timer > 0:
                player_gun.triple_shot_timer -= 1
            if player_gun.invulnerable_timer > 0:
                player_gun.invulnerable_timer -= 1
            
            # AI вражеских пушек
            for enemy_gun in enemy_guns:
                if enemy_gun.health > 0:
                    if random.random() < 0.7:
                        enemy_gun.ai_shoot(player_gun)
                    elif targets:
                        enemy_gun.ai_shoot(random.choice(targets))
                    enemy_gun.update_reload()
            
            # Сброс бомб от целей
            for t in targets:
                if t.live and t.should_drop_bomb():
                    bomb = Bomb(screen, t.x, t.y, player_gun.x, player_gun.y)
                    bombs.append(bomb)
            
            # Game over
            if player_gun.health <= 0:
                game_over = True
            
            # Обработка снарядов
            for proj in projectiles[:]:
                proj.move()
                
                if proj.should_remove():
                    if proj in projectiles:
                        projectiles.remove(proj)
                    continue
                
                if proj.live and not proj.stopped:
                    # Попадание в цели
                    for t in targets:
                        if t.live and proj.hittest(t):
                            is_burn = isinstance(proj, FireBullet)
                            if t.hit(proj.damage, is_burn):
                                total_score += t.calculate_points()
                                combo += 1
                                combo_timer = 60
                                create_explosion(screen, t.x, t.y, particles,
                                               ORANGE if is_burn else None,
                                               proj.explosion_particles)
                                t.new_target()
                            
                            # Разделение SplitBullet
                            if isinstance(proj, SplitBullet):
                                for i in range(proj.splits_into):
                                    angle = random.uniform(0, 2 * math.pi)
                                    split_proj = NormalBullet(
                                        screen, proj.x, proj.y,
                                        math.cos(angle) * 8,
                                        -math.sin(angle) * 8
                                    )
                                    projectiles.append(split_proj)
                            
                            # Взрывной урон HeavyBullet
                            if isinstance(proj, HeavyBullet) and proj.explosion_radius > 0:
                                for other_t in targets:
                                    if other_t != t and other_t.live:
                                        dist = math.hypot(proj.x - other_t.x, proj.y - other_t.y)
                                        if dist < proj.explosion_radius:
                                            other_t.hit(1)
                                            create_explosion(screen, other_t.x, other_t.y, particles)
                            
                            proj.live = False
                            create_explosion(screen, proj.x, proj.y, particles, ORANGE, 10)
                            if proj in projectiles:
                                projectiles.remove(proj)
                            break
                    
                    # Попадание во вражеские пушки
                    if proj.live:
                        for enemy_gun in enemy_guns:
                            if enemy_gun.health > 0:
                                dx = proj.x - enemy_gun.x
                                dy = proj.y - enemy_gun.y
                                if math.hypot(dx, dy) < proj.r + 12:
                                    enemy_gun.take_damage(proj.damage)
                                    create_explosion(screen, enemy_gun.x, enemy_gun.y, particles, RED, 20)
                                    if enemy_gun.health <= 0:
                                        total_score += 50
                                        create_explosion(screen, enemy_gun.x, enemy_gun.y, particles, YELLOW, 30)
                                    proj.live = False
                                    if proj in projectiles:
                                        projectiles.remove(proj)
                                    break
                    
                    # Попадание в игрока
                    if proj.live:
                        dx = proj.x - player_gun.x
                        dy = proj.y - player_gun.y
                        if math.hypot(dx, dy) < proj.r + 12:
                            player_gun.take_damage(proj.damage)
                            create_explosion(screen, player_gun.x, player_gun.y, particles, RED, 15)
                            proj.live = False
                            if proj in projectiles:
                                projectiles.remove(proj)
            
            # Движение целей
            for t in targets:
                t.move()
                
                # Столкновение с пушками
                for gun in all_guns:
                    if gun.health > 0 and t.live:
                        if math.hypot(t.x - gun.x, t.y - gun.y) < t.r + 20:
                            gun.take_damage()
                            create_explosion(screen, t.x, t.y, particles)
                            t.new_target()
            
            # Обработка бомб
            for bomb in bombs[:]:
                bomb.move()
                
                if bomb.activated and not bomb.live:
                    create_explosion(screen, bomb.x, bomb.y, particles, RED, 20)
                    # Урон в радиусе
                    for gun in all_guns:
                        if gun.health > 0:
                            dist = math.hypot(bomb.x - gun.x, bomb.y - gun.y)
                            if dist < bomb.explosion_radius:
                                gun.take_damage(2)
                                create_explosion(screen, gun.x, gun.y, particles, RED, 10)
                    if bomb in bombs:
                        bombs.remove(bomb)
                elif bomb.should_remove():
                    if bomb in bombs:
                        bombs.remove(bomb)
            
            # Обновление частиц
            for p in particles[:]:
                p.move()
                if p.life <= 0:
                    if p in particles:
                        particles.remove(p)
            
            # Автострельба при rapid fire
            if player_gun.rapid_fire_timer > 0 and player_gun.f2_on and player_gun.ammo != 0:
                if pygame.time.get_ticks() % 6 == 0:
                    player_gun.fire2_end(pygame.event.Event(pygame.MOUSEBUTTONUP,
                                     {'pos': pygame.mouse.get_pos()}))
                    player_gun.f2_on = 1
            
            player_gun.power_up()
            
            if combo_timer > 0:
                combo_timer -= 1
            else:
                combo = 0
            
            # Удаление уничтоженных врагов
            enemy_guns = [gun for gun in enemy_guns if gun.health > 0]
            all_guns = [player_gun] + enemy_guns
        
        elif paused:
            screen.fill(DARK_GREY)
            draw_text(screen, "ПАУЗА", WIDTH // 2 - 100, HEIGHT // 2 - 50, 70, WHITE, True)
            draw_text(screen, "Нажмите P для продолжения", WIDTH // 2 - 160, HEIGHT // 2 + 10, 30, WHITE)
            
            controls = [
                "WASD/Стрелки - движение пушки",
                "ЛКМ - стрельба, ПКМ/R - перезарядка",
                "1-4 - смена типа снаряда",
                "Пробел - супер-атака (x3 комбо)",
                "P - пауза"
            ]
            for i, text in enumerate(controls):
                draw_text(screen, text, WIDTH // 2 - 150, HEIGHT // 2 + 50 + i * 25, 20, WHITE)
            
            pygame.display.update()
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
        
        elif game_over:
            screen.fill(BLACK)
            draw_text(screen, "ИГРА ОКОНЧЕНА!", WIDTH // 2 - 180, HEIGHT // 2 - 80, 60, RED, True)
            draw_text(screen, f"Финальный счёт: {total_score}", WIDTH // 2 - 130, HEIGHT // 2, 40, WHITE)
            draw_text(screen, f"Выстрелов: {bullet}", WIDTH // 2 - 80, HEIGHT // 2 + 40, 30, GREY)
            draw_text(screen, "Нажмите любую клавишу для выхода", WIDTH // 2 - 170, HEIGHT // 2 + 80, 25, WHITE)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.KEYDOWN:
                    finished = True
    
    pygame.quit()


if __name__ == "__main__":
    main()