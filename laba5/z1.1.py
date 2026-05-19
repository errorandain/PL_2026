import math
import random
import pygame

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

GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, ORANGE, PURPLE, PINK, GOLD]
TARGET_COLORS = [RED, ORANGE, PURPLE, (255, 100, 100), (255, 165, 0), DARK_GREEN]

WIDTH = 800
HEIGHT = 600


class Particle:
    """Частица для эффекта взрыва."""
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.color = random.choice([RED, ORANGE, YELLOW, WHITE])
        self.r = random.randint(2, 6)
        self.life = random.randint(20, 40)
        self.gravity = 0.2
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 1
        self.vx *= 0.98
        self.vy *= 0.98
        
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


class PowerUp:
    """Бонусы, выпадающие с целей."""
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.type = random.choice(["ammo", "rapid_fire", "slow_motion", "health", "triple_shot"])
        self.r = 18
        self.vy = -2
        self.vx = random.uniform(-1, 1)
        self.gravity = 0.3
        self.live = True
        self.life_time = 300
        self.collected = False
        self.float_offset = 0
        
        self.powerup_config = {
            "ammo": {"color": YELLOW, "symbol": "A", "desc": "Патроны +5"},
            "rapid_fire": {"color": GREEN, "symbol": "R", "desc": "Скорострельность"},
            "slow_motion": {"color": LIGHT_BLUE, "symbol": "S", "desc": "Замедление"},
            "health": {"color": RED, "symbol": "H", "desc": "Доп. жизнь"},
            "triple_shot": {"color": ORANGE, "symbol": "T", "desc": "Тройной выстрел"}
        }
        
        config = self.powerup_config[self.type]
        self.color = config["color"]
        self.symbol = config["symbol"]
        self.description = config["desc"]
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life_time -= 1
        self.float_offset = math.sin(pygame.time.get_ticks() * 0.005) * 4
        
        if self.y + self.r >= HEIGHT:
            self.y = HEIGHT - self.r
            self.vy = -self.vy * 0.3
            self.vx *= 0.95
            if abs(self.vy) < 1:
                self.vy = 0
                self.vx = 0
        
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx * 0.5
        elif self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            self.vx = -self.vx * 0.5
            
        if self.life_time <= 0:
            self.live = False
            
    def draw(self):
        if self.live and not self.collected:
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 4
            pygame.draw.circle(self.screen, self.color, 
                             (int(self.x), int(self.y + self.float_offset)), 
                             int(self.r + pulse))
            pygame.draw.circle(self.screen, WHITE, 
                             (int(self.x), int(self.y + self.float_offset)), 
                             self.r, 2)
            
            font = pygame.font.Font(None, 28)
            text = font.render(self.symbol, True, BLACK)
            text_rect = text.get_rect(center=(self.x, self.y + self.float_offset))
            self.screen.blit(text, text_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            if math.hypot(mouse_pos[0] - self.x, mouse_pos[1] - self.y) < self.r + 10:
                font_small = pygame.font.Font(None, 18)
                desc_text = font_small.render(self.description, True, WHITE)
                desc_rect = desc_text.get_rect(center=(self.x, self.y - 35))
                pygame.draw.rect(self.screen, BLACK, desc_rect.inflate(10, 5))
                pygame.draw.rect(self.screen, WHITE, desc_rect.inflate(10, 5), 1)
                self.screen.blit(desc_text, desc_rect)
            
    def collect(self, gun):
        self.collected = True
        if self.type == "ammo":
            gun.ammo = min(gun.ammo + 5, 20)
        elif self.type == "rapid_fire":
            gun.rapid_fire_timer = 180
        elif self.type == "slow_motion":
            gun.slow_motion_timer = 180
        elif self.type == "health":
            gun.health = min(gun.health + 1, 5)
        elif self.type == "triple_shot":
            gun.triple_shot_timer = 150


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = True
        self.stopped = False
        self.stop_timer = 0
        self.bounce_count = 0
        self.max_bounces = 3
        self.trail = []
        self.hit_target = False
        
    def move(self):
        if self.stopped:
            self.stop_timer += 1
            return
        
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop(0)
        
        self.vy -= 0.5
        self.x += self.vx
        self.y -= self.vy
        
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx * 0.8
        elif self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            self.vx = -self.vx * 0.8
            
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = -self.vy * 0.8
        elif self.y + self.r >= HEIGHT:
            self.y = HEIGHT - self.r
            self.bounce_count += 1
            
            if self.bounce_count >= self.max_bounces:
                self.vy = 0
                self.vx = 0
                self.stopped = True
                self.live = False
            else:
                self.vy = -self.vy * 0.5
                self.vx *= 0.85
                
            if abs(self.vx) < 0.3:
                self.vx = 0
                
        if not self.stopped and abs(self.vx) < 0.1 and abs(self.vy) < 0.1:
            self.stopped = True
            self.live = False
            
    def draw(self):
        for i, pos in enumerate(self.trail):
            alpha = i / len(self.trail) * 0.7
            trail_color = self.color
            if isinstance(trail_color, int):
                r = ((trail_color >> 16) & 0xFF)
                g = ((trail_color >> 8) & 0xFF)
                b = (trail_color & 0xFF)
                trail_color = (int(r * alpha), int(g * alpha), int(b * alpha))
            pygame.draw.circle(self.screen, trail_color, (int(pos[0]), int(pos[1])), int(self.r * alpha))
        
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(self.screen, WHITE, (int(self.x - 3), int(self.y - 3)), 4)
        
        if self.stopped:
            pygame.draw.circle(self.screen, BLACK, (int(self.x), int(self.y)), self.r, 2)
            
    def hittest(self, obj):
        if not self.live or self.stopped:
            return False
        dx = self.x - obj.x
        dy = self.y - obj.y
        distance = math.hypot(dx, dy)
        return distance <= self.r + obj.r
    
    def hittest_powerup(self, powerup):
        if not self.live or self.stopped:
            return False
        dx = self.x - powerup.x
        dy = self.y - powerup.y
        distance = math.hypot(dx, dy)
        return distance <= self.r + powerup.r
        
    def should_remove(self):
        if self.stopped and self.stop_timer > 120:
            return True
        if self.x < -100 or self.x > WIDTH + 100 or self.y > HEIGHT + 100:
            return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 0
        self.color = GREY
        self.x = 40
        self.y = HEIGHT - 100
        self.ammo = -1
        self.reload_time = 0
        self.shake = 0
        self.health = 3
        self.max_health = 3
        self.rapid_fire_timer = 0
        self.slow_motion_timer = 0
        self.triple_shot_timer = 0
        self.invulnerable_timer = 0
        
    def fire2_start(self, event):
        if self.ammo > 0 or self.ammo == -1:
            self.f2_on = 1
        
    def fire2_end(self, event):
        global balls, bullet
        if (self.ammo > 0 or self.ammo == -1) and self.f2_on:
            bullet += 1
            if self.ammo > 0:
                self.ammo -= 1
                
            bullet_count = 3 if self.triple_shot_timer > 0 else 1
            
            for i in range(bullet_count):
                new_ball = Ball(self.screen, self.x, self.y)
                new_ball.r += 5
                
                spread = 0.15 if bullet_count > 1 else 0
                angle_offset = (i - 1) * spread if bullet_count > 1 else 0
                
                self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
                new_ball.vx = self.f2_power * math.cos(self.an + angle_offset)
                new_ball.vy = -self.f2_power * math.sin(self.an + angle_offset)
                balls.append(new_ball)
                
            self.shake = 7
            
        self.f2_on = 0
        self.f2_power = 10
        
    def targetting(self, event):
        if event:
            if event.pos[0] - self.x != 0:
                self.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY
            
    def draw(self):
        shake_offset_x = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        shake_offset_y = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        if self.shake > 0:
            self.shake -= 1
            
        power_bonus = self.f2_power if self.f2_on else 0
        end_x = self.x + (50 + power_bonus * 0.3) * math.cos(self.an)
        end_y = self.y + (50 + power_bonus * 0.3) * math.sin(self.an)
        
        pygame.draw.line(self.screen, DARK_GREY, (self.x - 5, self.y - 5), (self.x + 20, self.y + 20), 10)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 15)
        pygame.draw.circle(self.screen, DARK_GREY, (self.x, self.y), 15, 2)
        pygame.draw.line(self.screen, self.color, 
                        (self.x + shake_offset_x, self.y + shake_offset_y), 
                        (end_x + shake_offset_x, end_y + shake_offset_y), 8)
        
        if self.f2_on:
            power_width = int(self.f2_power * 1.5)
            pygame.draw.rect(self.screen, RED, (self.x - 20, self.y - 50, power_width, 8))
            pygame.draw.rect(self.screen, WHITE, (self.x - 20, self.y - 50, 150, 8), 1)
            
    def power_up(self):
        if self.f2_on and (self.ammo > 0 or self.ammo == -1):
            if self.f2_power < 100:
                self.f2_power += 2
            self.color = RED
        else:
            self.color = GREY
            
    def reload(self):
        if self.ammo < 10:
            self.reload_time = 60
            
    def update_reload(self):
        if self.reload_time > 0:
            self.reload_time -= 1
            if self.reload_time == 0:
                self.ammo = min(self.ammo + 10, 20)
                
    def take_damage(self, damage=1):
        if self.invulnerable_timer <= 0:
            self.health -= damage
            self.invulnerable_timer = 60
            
    def draw_health_bar(self):
        bar_width = 200
        bar_height = 20
        x = WIDTH - bar_width - 20
        y = 20
        
        pygame.draw.rect(self.screen, DARK_GREY, (x, y, bar_width, bar_height))
        health_width = int((self.health / self.max_health) * bar_width)
        health_color = GREEN if self.health > 1 else YELLOW if self.health == 1 else RED
        pygame.draw.rect(self.screen, health_color, (x, y, health_width, bar_height))
        pygame.draw.rect(self.screen, WHITE, (x, y, bar_width, bar_height), 2)
        
        font = pygame.font.Font(None, 20)
        text = font.render(f"{self.health}/{self.max_health}", True, WHITE)
        self.screen.blit(text, (x + bar_width // 2 - 15, y + 2))


class Target:
    def __init__(self, screen, target_type="normal"):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.type = target_type
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])
        self.hits_to_die = 1 if target_type == "normal" else 2 if target_type == "fast" else 3
        self.current_hits = 0
        self.rotation = 0
        self.new_target()
        
    def new_target(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 500)
        self.r = random.randint(15, 40)
        
        if self.type == "boss":
            self.r = 45
            self.color = PURPLE
            self.vx = random.choice([-3, 3])
            self.vy = random.choice([-3, 3])
        elif self.type == "fast":
            self.r = 18
            self.color = GREEN
            self.vx = random.choice([-4, -3, 3, 4])
            self.vy = random.choice([-4, -3, 3, 4])
        else:
            self.color = random.choice(TARGET_COLORS)
            
        self.live = 1
        self.current_hits = 0
        
    def move(self):
        if self.live:
            self.x += self.vx
            self.y += self.vy
            self.rotation += 5
            
            if self.x - self.r <= 0 or self.x + self.r >= WIDTH:
                self.vx = -self.vx
            if self.y - self.r <= 0 or self.y + self.r >= HEIGHT:
                self.vy = -self.vy
                
    def hit(self, points=1):
        self.current_hits += 1
        if self.current_hits >= self.hits_to_die:
            self.points += points * (3 if self.type == "boss" else 2 if self.type == "fast" else 1)
            self.live = 0
            return True
        return False
        
    def draw(self):
        if self.live:
            pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.r)
            
            if self.type == "boss":
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 8
                pygame.draw.circle(self.screen, YELLOW, (int(self.x), int(self.y)), int(self.r * 0.6 + pulse))
                pygame.draw.circle(self.screen, BLACK, (int(self.x), int(self.y)), self.r // 3)
                
                health_width = int((self.hits_to_die - self.current_hits) / self.hits_to_die * self.r * 2)
                pygame.draw.rect(self.screen, GREEN, (self.x - self.r, self.y - self.r - 12, health_width, 6))
                pygame.draw.rect(self.screen, WHITE, (self.x - self.r, self.y - self.r - 12, self.r * 2, 6), 1)
            else:
                angle = math.radians(self.rotation)
                inner_x = self.x + self.r * 0.3 * math.cos(angle)
                inner_y = self.y + self.r * 0.3 * math.sin(angle)
                pygame.draw.circle(self.screen, BLACK, (int(inner_x), int(inner_y)), self.r // 3)
                pygame.draw.circle(self.screen, WHITE, (int(self.x - 5), int(self.y - 5)), 5)


def draw_text(screen, text, x, y, size=30, color=BLACK, bold=False):
    font = pygame.font.Font(None, size)
    if bold:
        font.set_bold(True)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def create_explosion(screen, x, y, particles_list):
    for _ in range(15):
        particles_list.append(Particle(screen, x, y))


def draw_stars(screen, stars):
    for star in stars:
        brightness = int(255 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.001 * star[2])))
        pygame.draw.circle(screen, (brightness, brightness, brightness), (star[0], star[1]), 1)


# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔥 ПУШКА: ULTRA EDITION 🔥")

bullet = 0
balls = []
particles = []
powerups = []

clock = pygame.time.Clock()
gun = Gun(screen)

targets = [
    Target(screen, "normal"),
    Target(screen, "fast"),
    Target(screen, "boss")
]

total_score = 0
combo = 0
combo_timer = 0
finished = False
paused = False
game_over = False

stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.random()) for _ in range(150)]

while not finished:
    if not paused and not game_over:
        screen.fill(DARK_GREY)
        draw_stars(screen, stars)
        
        pygame.draw.rect(screen, BROWN, (0, HEIGHT - 20, WIDTH, 20))
        pygame.draw.rect(screen, GREEN, (0, HEIGHT - 25, WIDTH, 10))
        
        gun.draw()
        gun.draw_health_bar()
        
        for t in targets:
            t.draw()
            
        for b in balls:
            b.draw()
            
        for p in particles:
            p.draw()
            
        for pu in powerups:
            pu.draw()
        
        draw_text(screen, f"Счёт: {total_score}", 10, 10, 35, WHITE, True)
        draw_text(screen, f"Выстрелов: {bullet}", 10, 45, 25, WHITE)
        
        ammo_color = YELLOW if gun.ammo < 5 and gun.ammo > 0 else WHITE
        ammo_text = f"Патроны: {gun.ammo if gun.ammo > 0 else '∞' if gun.ammo == -1 else '0'}"
        draw_text(screen, ammo_text, 10, 75, 25, ammo_color)
        
        if combo > 1:
            draw_text(screen, f"COMBO x{combo}!", WIDTH - 180, 10, 45, ORANGE, True)
            
        if gun.rapid_fire_timer > 0:
            draw_text(screen, "RAPID FIRE!", WIDTH - 200, 55, 25, GREEN)
            
        if gun.slow_motion_timer > 0:
            draw_text(screen, "SLOW MOTION", WIDTH - 200, 85, 25, LIGHT_BLUE)
            
        if gun.triple_shot_timer > 0:
            draw_text(screen, "TRIPLE SHOT!", WIDTH - 200, 115, 25, ORANGE)
            
        pygame.display.update()
        
        current_fps = FPS
        if gun.slow_motion_timer > 0:
            current_fps = FPS // 2
            gun.slow_motion_timer -= 1
        clock.tick(current_fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    picked = False
                    for pu in powerups[:]:
                        dx = event.pos[0] - pu.x
                        dy = event.pos[1] - pu.y
                        if math.hypot(dx, dy) <= pu.r + 10:
                            pu.collect(gun)
                            create_explosion(screen, pu.x, pu.y, particles)
                            powerups.remove(pu)
                            picked = True
                            break
                    if not picked:
                        gun.fire2_start(event)
                elif event.button == 3:
                    gun.reload()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    gun.reload()
                elif event.key == pygame.K_p:
                    paused = True
                elif event.key == pygame.K_SPACE:
                    if combo >= 3:
                        for _ in range(5):
                            new_ball = Ball(screen, gun.x, gun.y)
                            new_ball.r += 3
                            new_ball.vx = random.uniform(-25, 25)
                            new_ball.vy = random.uniform(-25, 25)
                            balls.append(new_ball)
                        combo = 0
                        create_explosion(screen, gun.x, gun.y, particles)
        
        gun.update_reload()
        if gun.rapid_fire_timer > 0:
            gun.rapid_fire_timer -= 1
        if gun.triple_shot_timer > 0:
            gun.triple_shot_timer -= 1
        if gun.invulnerable_timer > 0:
            gun.invulnerable_timer -= 1
            
        if combo_timer > 0:
            combo_timer -= 1
        else:
            combo = 0
            
        if gun.health <= 0:
            game_over = True
            
        for b in balls[:]:
            b.move()
            if b.should_remove():
                balls.remove(b)
                continue
                
            if b.live:
                for t in targets:
                    if t.live and b.hittest(t):
                        if t.hit():
                            points_earned = 10
                            if t.type == "fast":
                                points_earned = 20
                            elif t.type == "boss":
                                points_earned = 50
                            total_score += points_earned
                            combo += 1
                            combo_timer = 60
                            
                            create_explosion(screen, t.x, t.y, particles)
                            
                            if random.random() < 0.6:
                                powerups.append(PowerUp(screen, t.x, t.y))
                                
                            t.new_target()
                        b.live = False
                        break
                        
                for pu in powerups[:]:
                    if b.hittest_powerup(pu):
                        pu.collect(gun)
                        create_explosion(screen, pu.x, pu.y, particles)
                        powerups.remove(pu)
                        break
        
        for t in targets:
            t.move()
            
            if t.live:
                if math.hypot(t.x - gun.x, t.y - gun.y) < t.r + 20:
                    gun.take_damage()
                    create_explosion(screen, t.x, t.y, particles)
                    t.new_target()
            
        for p in particles[:]:
            p.move()
            if p.life <= 0:
                particles.remove(p)
                
        for pu in powerups[:]:
            pu.move()
            if not pu.live:
                powerups.remove(pu)
                
        if gun.rapid_fire_timer > 0 and gun.f2_on and gun.ammo != 0:
            if pygame.time.get_ticks() % 6 == 0:
                event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': pygame.mouse.get_pos()})
                gun.fire2_end(event)
                gun.f2_on = 1
                
        gun.power_up()
        
    elif paused:
        screen.fill(DARK_GREY)
        draw_text(screen, "ПАУЗА", WIDTH // 2 - 100, HEIGHT // 2 - 30, 70, WHITE, True)
        draw_text(screen, "Нажмите P для продолжения", WIDTH // 2 - 160, HEIGHT // 2 + 30, 30, WHITE)
        draw_text(screen, "Управление:", WIDTH // 2 - 80, HEIGHT // 2 + 80, 25, WHITE)
        draw_text(screen, "ЛКМ - стрельба", WIDTH // 2 - 80, HEIGHT // 2 + 110, 20, WHITE)
        draw_text(screen, "ПКМ/R - перезарядка", WIDTH // 2 - 80, HEIGHT // 2 + 135, 20, WHITE)
        draw_text(screen, "Пробел - супер-атака", WIDTH // 2 - 80, HEIGHT // 2 + 160, 20, WHITE)
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
        draw_text(screen, "ИГРА ОКОНЧЕНА!", WIDTH // 2 - 180, HEIGHT // 2 - 50, 60, RED, True)
        draw_text(screen, f"Финальный счёт: {total_score}", WIDTH // 2 - 130, HEIGHT // 2 + 10, 40, WHITE)
        draw_text(screen, f"Всего выстрелов: {bullet}", WIDTH // 2 - 110, HEIGHT // 2 + 50, 30, GREY)
        draw_text(screen, "Нажмите любую клавишу для выхода", WIDTH // 2 - 170, HEIGHT // 2 + 100, 25, WHITE)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                finished = True

pygame.quit()