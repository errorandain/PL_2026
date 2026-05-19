import math
from random import *

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
ORANGE = 0xFFA500
DARK_RED = 0x8B0000
DARK_GREEN = 0x006400
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

pygame.font.init()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)


class Bomb:
    def __init__(self, screen: pygame.Surface, x, y):
        """Конструктор класса Bomb - бомбы, которые сбрасывают цели.
        
        Args:
        x - начальное положение бомбы по горизонтали
        y - начальное положение бомбы по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 8
        self.vx = randint(-2, 2)
        self.vy = randint(1, 3)  # Падает вниз
        self.color = DARK_RED
        self.live = True
        self.damage = 1

    def move(self):
        """Перемещение бомбы."""
        self.x += self.vx
        self.y += self.vy
        
        # Бомба исчезает, если выходит за границы экрана
        if (self.x > WIDTH + self.r or self.x < -self.r or 
            self.y > HEIGHT + self.r or self.y < -self.r):
            self.live = False

    def draw(self):
        """Рисование бомбы."""
        # Основной круг бомбы
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        # Фитиль бомбы
        pygame.draw.line(
            self.screen,
            ORANGE,
            (self.x, self.y - self.r),
            (self.x + 3, self.y - self.r - 5),
            3
        )
        # Искра на фитиле
        spark_color = choice([YELLOW, RED, ORANGE])
        pygame.draw.circle(
            self.screen,
            spark_color,
            (self.x + 3, self.y - self.r - 5),
            2
        )

    def hittest(self, obj):
        """Проверка столкновения бомбы с объектом (пушкой)."""
        dx = self.x - obj.x
        dy = self.y - obj.y
        dist = math.hypot(dx, dy)
        # Используем фиксированный радиус попадания для пушки
        obj_radius = getattr(obj, 'r', 20)
        return dist <= self.r + obj_radius


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450, ball_type="normal", owner=None):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        ball_type - тип снаряда (normal, heavy, bouncy)
        owner - пушка, которая выпустила снаряд
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.live = 30
        self.ball_type = ball_type
        self.owner = owner  # Пушка-владелец, чтобы не попадать в себя
        
        # Настройки для разных типов снарядов
        if ball_type == "normal":
            self.r = 10
            self.color = choice(GAME_COLORS)
            self.gravity = 1
            self.friction = 0.98
            self.bounce_factor = 1.0
            self.damage = 1
        elif ball_type == "heavy":
            self.r = 20
            self.color = BLACK
            self.gravity = 2
            self.friction = 0.95
            self.bounce_factor = 0.3
            self.damage = 2
        elif ball_type == "bouncy":
            self.r = 8
            self.color = ORANGE
            self.gravity = 0.5
            self.friction = 0.995
            self.bounce_factor = 1.2
            self.damage = 1

    def move(self):
        """Переместить мяч с учетом гравитации, трения и отскоков от стен."""
        # Гравитация
        self.vy -= self.gravity
        
        # Трение (замедление)
        self.vx *= self.friction
        self.vy *= self.friction
        
        # Перемещение
        self.x += self.vx
        self.y -= self.vy
        
        # Отскок от стен
        if self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            self.vx = -self.vx * self.bounce_factor
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx * self.bounce_factor
        if self.y + self.r >= HEIGHT:
            self.y = HEIGHT - self.r
            self.vy = -self.vy * self.bounce_factor
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = -self.vy * self.bounce_factor
        
        # Остановка при очень маленькой скорости
        if abs(self.vx) < 0.5:
            self.vx = 0
        if abs(self.vy) < 0.5:
            self.vy = 0

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Проверка столкновения с целью obj."""
        dx = self.x - obj.x
        dy = self.y - obj.y
        dist = math.hypot(dx, dy)
        # Используем getattr для получения радиуса, с значением по умолчанию 20
        obj_radius = getattr(obj, 'r', 20)
        return dist <= self.r + obj_radius


class Gun:
    def __init__(self, screen, x, y, color=GREY, is_player=False):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = color
        self.gun_size = 30
        self.selected_ammo = "normal"  # Текущий тип снаряда
        self.ammo_colors = {
            "normal": GREY,
            "heavy": BLACK,
            "bouncy": ORANGE
        }
        # Позиция пушки
        self.x = x
        self.y = y
        self.r = 15  # Радиус пушки для столкновений
        # Скорость движения пушки
        self.speed = 3
        # Границы движения пушки по X
        self.min_x = 30
        self.max_x = WIDTH - 30
        # Здоровье пушки
        self.health = 5
        self.max_health = 5
        # Очки за уничтожение
        self.points_value = 10 if not is_player else 0
        # Флаги
        self.is_player = is_player  # Игрок или бот
        self.live = True
        
        # AI параметры для ботов
        self.ai_timer = 0
        self.ai_target = None
        self.ai_fire_delay = randint(60, 120)  # Задержка между выстрелами

    def move_left(self):
        """Движение пушки влево."""
        self.x -= self.speed
        if self.x < self.min_x:
            self.x = self.min_x

    def move_right(self):
        """Движение пушки вправо."""
        self.x += self.speed
        if self.x > self.max_x:
            self.x = self.max_x

    def move_up(self):
        """Движение пушки вверх."""
        self.y -= self.speed
        if self.y < 50:
            self.y = 50

    def move_down(self):
        """Движение пушки вниз."""
        self.y += self.speed
        if self.y > HEIGHT - 30:
            self.y = HEIGHT - 30

    def fire(self, target_x, target_y):
        """Выстрел в указанную точку."""
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, x=self.x, y=self.y, ball_type=self.selected_ammo, owner=self)
        new_ball.r += 5 if self.selected_ammo == "normal" else 0
        self.an = math.atan2((target_y - self.y), (target_x - self.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        
        # Бонусная скорость для легких снарядов
        if self.selected_ammo == "bouncy":
            new_ball.vx *= 1.5
            new_ball.vy *= 1.5
        
        balls.append(new_ball)

    def fire2_start(self, event):
        self.f2_on = 1
        self.gun_size = 30

    def fire2_end(self, event):
        """Выстрел мячом (для игрока)."""
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, x=self.x, y=self.y, ball_type=self.selected_ammo, owner=self)
        new_ball.r += 5 if self.selected_ammo == "normal" else 0
        self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        
        # Бонусная скорость для легких снарядов
        if self.selected_ammo == "bouncy":
            new_ball.vx *= 1.5
            new_ball.vy *= 1.5
        
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        self.gun_size = 30

    def targetting(self, event):
        """Прицеливание для игрока."""
        if event:
            self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = self.ammo_colors.get(self.selected_ammo, GREY)

    def ai_update(self, all_guns):
        """AI поведение для ботов."""
        if not self.is_player and self.live:
            self.ai_timer += 1
            
            # Выбираем цель
            if self.ai_target is None or not self.ai_target.live or randint(0, 100) == 0:
                # Выбираем случайную живую цель, кроме себя
                alive_targets = [g for g in all_guns if g != self and g.live]
                if alive_targets:
                    self.ai_target = choice(alive_targets)
            
            # Двигаемся к цели или от неё
            if self.ai_target and self.ai_target.live:
                # Случайное движение с уклонением
                if randint(0, 50) == 0:
                    if randint(0, 1) == 0:
                        self.move_left()
                    else:
                        self.move_right()
                
                # Прицеливаемся на цель
                self.an = math.atan2((self.ai_target.y - self.y), 
                                   (self.ai_target.x - self.x))
                
                # Стреляем с задержкой
                if self.ai_timer >= self.ai_fire_delay:
                    self.fire(self.ai_target.x, self.ai_target.y)
                    self.ai_timer = 0
                    self.ai_fire_delay = randint(60, 120)
                    # Меняем тип снаряда случайно
                    if randint(0, 5) == 0:
                        self.selected_ammo = choice(["normal", "heavy", "bouncy"])

    def draw(self):
        if not self.live:
            return
            
        # Рисуем платформу пушки
        platform_width = 30
        platform_height = 8
        pygame.draw.rect(
            self.screen, 
            self.color, 
            (self.x - platform_width//2, self.y - platform_height//2, 
             platform_width, platform_height)
        )
        
        # Рисуем ствол
        length = self.gun_size
        x_end = self.x + length * math.cos(self.an)
        y_end = self.y + length * math.sin(self.an)
        pygame.draw.line(self.screen, self.color, (self.x, self.y), (x_end, y_end), 6)
        
        # Рисуем полоску здоровья над пушкой
        health_bar_width = 40
        health_bar_height = 4
        health_x = self.x - health_bar_width // 2
        health_y = self.y - 25
        
        # Фон полоски здоровья (красный)
        pygame.draw.rect(
            self.screen,
            RED,
            (health_x, health_y, health_bar_width, health_bar_height)
        )
        # Текущее здоровье (зеленый)
        current_health_width = int(health_bar_width * (self.health / self.max_health))
        if current_health_width > 0:
            pygame.draw.rect(
                self.screen,
                GREEN,
                (health_x, health_y, current_health_width, health_bar_height)
            )
        
        # Метка игрока или бота
        if self.is_player:
            label = "Player"
            label_color = BLUE
        else:
            label = "Bot"
            label_color = RED
        label_text = small_font.render(label, True, label_color)
        label_rect = label_text.get_rect(center=(self.x, self.y - 35))
        self.screen.blit(label_text, label_rect)

    def take_damage(self, damage):
        """Получение урона пушкой."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.live = False

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                self.gun_size += 0.4
            self.color = RED
        else:
            self.color = self.ammo_colors.get(self.selected_ammo, GREY)
    
    def switch_ammo(self, ammo_type):
        """Переключение типа снаряда."""
        if ammo_type in self.ammo_colors:
            self.selected_ammo = ammo_type


class Target:
    def __init__(self, target_type=None):
        self.screen = screen
        self.points = 0
        self.live = 1
        
        # Типы целей: "normal", "fast", "tank"
        if target_type is None:
            self.target_type = choice(["normal", "fast", "tank"])
        else:
            self.target_type = target_type
        
        self.new_target()
        
        # Таймер для сбрасывания бомб
        self.bomb_timer = randint(60, 180)  # От 2 до 6 секунд при 30 FPS
        self.bomb_cooldown = 0

    def move(self):
        """Движение цели в зависимости от её типа."""
        if self.target_type == "normal":
            self.move_normal()
        elif self.target_type == "fast":
            self.move_fast()
        elif self.target_type == "tank":
            self.move_tank()

    def move_normal(self):
        """Обычное движение с отскоком от стен."""
        self.x += self.vx
        self.y += self.vy
        
        self.bounce_off_walls()

    def move_fast(self):
        """Быстрое хаотичное движение."""
        # Случайное изменение направления
        if randint(0, 30) == 0:
            self.vx = randint(-8, 8)
            self.vy = randint(-8, 8)
            if self.vx == 0:
                self.vx = choice([-4, 4])
            if self.vy == 0:
                self.vy = choice([-4, 4])
        
        self.x += self.vx
        self.y += self.vy
        
        self.bounce_off_walls()

    def move_tank(self):
        """Медленное, но упорное движение."""
        # Медленное движение
        self.x += self.vx
        self.y += self.vy
        
        self.bounce_off_walls()

    def bounce_off_walls(self):
        """Отскок от стен."""
        if self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            self.vx = -self.vx
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -self.vx
        
        if self.y + self.r >= HEIGHT:
            self.y = HEIGHT - self.r
            self.vy = -self.vy
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = -self.vy

    def drop_bomb(self):
        """Создание бомбы под целью."""
        global bombs
        if self.bomb_cooldown <= 0:
            new_bomb = Bomb(self.screen, self.x, self.y + self.r)
            bombs.append(new_bomb)
            self.bomb_cooldown = self.bomb_timer
            self.bomb_timer = randint(60, 180)

    def update_bomb_timer(self):
        """Обновление таймера бомб."""
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= 1

    def new_target(self):
        """ Инициализация новой цели с параметрами в зависимости от типа."""
        # Базовые параметры
        x = self.x = randint(200, 780)
        y = self.y = randint(100, 500)
        r = self.r = randint(15, 40)
        
        if self.target_type == "normal":
            self.color = RED
            self.vx = randint(-5, 5)
            self.vy = randint(-5, 5)
            if self.vx == 0:
                self.vx = choice([-2, 2])
            if self.vy == 0:
                self.vy = choice([-2, 2])
            self.points_value = 1
            
        elif self.target_type == "fast":
            self.color = YELLOW
            self.r = randint(10, 20)  # Маленькая и быстрая
            self.vx = randint(-8, 8)
            self.vy = randint(-8, 8)
            if self.vx == 0:
                self.vx = choice([-4, 4])
            if self.vy == 0:
                self.vy = choice([-4, 4])
            self.points_value = 2
            
        elif self.target_type == "tank":
            self.color = DARK_GREEN
            self.r = randint(35, 55)  # Большая цель
            self.vx = randint(-2, 2)
            self.vy = randint(-2, 2)
            if self.vx == 0:
                self.vx = choice([-1, 1])
            if self.vy == 0:
                self.vy = choice([-1, 1])
            self.points_value = 1
        
        self.bomb_timer = randint(60, 180)
        self.bomb_cooldown = 0

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        # Рисуем основную цель
        if self.target_type == "normal":
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        elif self.target_type == "fast":
            # Маленький быстрый ромб
            points = [
                (self.x, self.y - self.r),
                (self.x + self.r, self.y),
                (self.x, self.y + self.r),
                (self.x - self.r, self.y)
            ]
            pygame.draw.polygon(self.screen, self.color, points)
        elif self.target_type == "tank":
            # Квадрат (большая цель)
            pygame.draw.rect(self.screen, self.color, 
                           (self.x - self.r, self.y - self.r, 
                            self.r * 2, self.r * 2))
        
        # Индикатор готовности бомбы
        if self.bomb_cooldown <= 0:
            pygame.draw.circle(
                self.screen,
                DARK_RED,
                (self.x, self.y - self.r - 5),
                3
            )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Битва пушек")
bullet = 0
balls = []
bombs = []

clock = pygame.time.Clock()

# Общий счет игры
total_score = 0

# Создаем пушки (одна для игрока, остальные боты)
guns = [
    Gun(screen, 400, 560, GREY, True),   # Игрок внизу по центру
    Gun(screen, 200, 100, RED, False),    # Бот 1 сверху слева
    Gun(screen, 600, 100, BLUE, False),   # Бот 2 сверху справа
    Gun(screen, 100, 300, GREEN, False),  # Бот 3 слева
    Gun(screen, 700, 300, MAGENTA, False) # Бот 4 справа
]

# Создаем цели
targets = [
    Target("normal"),
    Target("fast"),
    Target("tank")
]

finished = False
game_over = False
player_gun = guns[0]  # Первая пушка - игрок

while not finished:
    screen.fill(WHITE)
    
    if not game_over:
        # Проверка, жив ли игрок
        if not player_gun.live:
            game_over = True
        
        # Проверка, остались ли боты
        alive_bots = [g for g in guns if not g.is_player and g.live]
        if len(alive_bots) == 0:
            # Все боты уничтожены - победа!
            victory_text = font.render("ПОБЕДА! Все боты уничтожены!", True, GREEN)
            screen.blit(victory_text, (WIDTH//2 - 250, HEIGHT//2))
            pygame.display.update()
            pygame.time.wait(3000)
            game_over = True
        
        # Отображение статистики
        score_text = font.render(f"Очки: {total_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        alive_text = font.render(f"Ботов осталось: {len(alive_bots)}", True, BLACK)
        screen.blit(alive_text, (10, 40))
        
        
        # Обновление AI для ботов
        for gun in guns:
            if not gun.is_player and gun.live:
                gun.ai_update(guns)
        
        # Отрисовка всех пушек
        for gun in guns:
            gun.draw()
        
        # Обновление и отрисовка всех целей
        for target in targets:
            target.draw()
            target.move()
            target.update_bomb_timer()
            target.drop_bomb()
        
        # Отрисовка и перемещение бомб
        for bomb in bombs[:]:
            bomb.move()
            bomb.draw()
            
            # Проверка попадания бомбы в любую пушку
            for gun in guns:
                if gun.live and bomb.hittest(gun):
                    gun.take_damage(bomb.damage)
                    if bomb in bombs:
                        bombs.remove(bomb)
                    break
            
            # Удаление бомб, вышедших за экран
            if bomb in bombs and not bomb.live:
                bombs.remove(bomb)
        
        # Отрисовка снарядов
        for b in balls:
            b.draw()
        
        pygame.display.update()

        clock.tick(FPS)
        
        # Обработка управления игроком
        keys = pygame.key.get_pressed()
        if player_gun.live:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_gun.move_left()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_gun.move_right()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_gun.move_up()
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_gun.move_down()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN and player_gun.live:
                player_gun.fire2_start(event)
            elif event.type == pygame.MOUSEBUTTONUP and player_gun.live:
                player_gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION and player_gun.live:
                player_gun.targetting(event)
            elif event.type == pygame.KEYDOWN:
                if player_gun.live:
                    # Переключение типов снарядов клавишами 1-3
                    if event.key == pygame.K_1:
                        player_gun.switch_ammo("normal")
                    elif event.key == pygame.K_2:
                        player_gun.switch_ammo("heavy")
                    elif event.key == pygame.K_3:
                        player_gun.switch_ammo("bouncy")

        # Обновление снарядов и проверка попаданий
        for b in balls[:]:
            b.move()
            
            # Проверка попадания в цели
            hit_target = False
            for target in targets[:]:
                if b.hittest(target) and target.live:
                    total_score += target.points_value  # Добавляем очки
                    target.live = 0
                    # Создаем новую цель того же типа
                    new_target = Target(target.target_type)
                    targets.remove(target)
                    targets.append(new_target)
                    new_target.live = 1
                    hit_target = True
                    break
            
            if hit_target:
                if b in balls:
                    balls.remove(b)
                continue
            
            # Проверка попадания в пушки (кроме владельца)
            hit_gun = False
            for gun in guns:
                if gun != b.owner and gun.live and b.hittest(gun):
                    gun.take_damage(b.damage)
                    if not gun.live and not gun.is_player:
                        # Если уничтожили бота, начисляем очки
                        total_score += gun.points_value
                    hit_gun = True
                    break
            
            if hit_gun:
                if b in balls:
                    balls.remove(b)
        
        player_gun.power_up()
    
    else:
        # Экран Game Over
        if not player_gun.live:
            game_over_text = font.render("GAME OVER! Вас уничтожили!", True, RED)
        else:
            game_over_text = font.render("ПОБЕДА!", True, GREEN)
        
        score_text = font.render(f"Итоговый счет: {total_score}", True, BLACK)
        restart_text = font.render("Нажмите R для перезапуска или Q для выхода", True, GREY)
        
        screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
        screen.blit(score_text, (WIDTH//2 - 100, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - 250, HEIGHT//2 + 50))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Перезапуск игры
                    total_score = 0
                    guns = [
                        Gun(screen, 400, 560, GREY, True),
                        Gun(screen, 200, 100, RED, False),
                        Gun(screen, 600, 100, BLUE, False),
                        Gun(screen, 100, 300, GREEN, False),
                        Gun(screen, 700, 300, MAGENTA, False)
                    ]
                    player_gun = guns[0]
                    targets = [
                        Target("normal"),
                        Target("fast"),
                        Target("tank")
                    ]
                    balls = []
                    bombs = []
                    game_over = False
                elif event.key == pygame.K_q:
                    finished = True

pygame.quit()