import pygame
import math

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Котик на левом боку")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
LIGHT_ORANGE = (255, 200, 100)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BROWN = (139, 69, 19)

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Заливка фона
    screen.fill(LIGHT_GRAY)
    
    # === РИСУЕМ КОТА, ЛЕЖАЩЕГО НА ЛЕВОМ БОКУ ===
    
    # Тело кота (овал, лежащий горизонтально)
    body_x, body_y = 300, 300
    body_width, body_height = 250, 120
    pygame.draw.ellipse(screen, ORANGE, (body_x, body_y, body_width, body_height))
    
    # Животик (светлая часть)
    belly_x, belly_y = body_x + 30, body_y + 20
    belly_width, belly_height = 150, 60
    pygame.draw.ellipse(screen, LIGHT_ORANGE, (belly_x, belly_y, belly_width, belly_height))
    
    # Голова (слева от тела)
    head_x, head_y = body_x - 40, body_y + 20
    head_radius = 50
    pygame.draw.circle(screen, ORANGE, (head_x, head_y), head_radius)
    
    # Левое ухо (первое)
    ear1_points = [
        (head_x - 30, head_y - 30),
        (head_x - 10, head_y - 50),
        (head_x + 10, head_y - 30)
    ]
    pygame.draw.polygon(screen, ORANGE, ear1_points)
    
    # Правое ухо (второе)
    ear2_points = [
        (head_x + 20, head_y - 35),
        (head_x + 40, head_y - 50),
        (head_x + 45, head_y - 25)
    ]
    pygame.draw.polygon(screen, ORANGE, ear2_points)
    
    # Внутренняя часть ушей (розовая)
    inner_ear1_points = [
        (head_x - 25, head_y - 30),
        (head_x - 10, head_y - 45),
        (head_x + 5, head_y - 30)
    ]
    pygame.draw.polygon(screen, PINK, inner_ear1_points)
    
    inner_ear2_points = [
        (head_x + 25, head_y - 35),
        (head_x + 35, head_y - 45),
        (head_x + 40, head_y - 30)
    ]
    pygame.draw.polygon(screen, PINK, inner_ear2_points)
    
    # Глаза (зеленые, смотрят влево)
    # Левый глаз (ближе к носу)
    pygame.draw.circle(screen, GREEN, (head_x - 15, head_y - 5), 10)
    pygame.draw.circle(screen, DARK_GREEN, (head_x - 18, head_y - 8), 4)  # Зрачок
    pygame.draw.circle(screen, WHITE, (head_x - 20, head_y - 10), 2)  # Блик
    
    # Правый глаз
    pygame.draw.circle(screen, GREEN, (head_x + 10, head_y - 10), 9)
    pygame.draw.circle(screen, DARK_GREEN, (head_x + 7, head_y - 13), 3)  # Зрачок
    pygame.draw.circle(screen, WHITE, (head_x + 5, head_y - 15), 2)  # Блик
    
    # Носик (розовый треугольник)
    nose_points = [
        (head_x - 5, head_y + 5),
        (head_x + 5, head_y + 5),
        (head_x, head_y + 12)
    ]
    pygame.draw.polygon(screen, PINK, nose_points)
    
    # Ротик
    pygame.draw.arc(screen, BLACK, (head_x - 10, head_y + 10, 20, 10), 0.1, math.pi - 0.1, 2)
    
    # Усы
    for i in range(3):
        offset = i * 5 - 5
        # Усы слева
        pygame.draw.line(screen, BLACK, (head_x - 25, head_y + offset), (head_x - 50, head_y - 5 + offset), 1)
        # Усы справа
        pygame.draw.line(screen, BLACK, (head_x + 25, head_y + offset), (head_x + 50, head_y - 5 + offset), 1)
    
    # Лапки
    # Передняя лапка (видна)
    pygame.draw.ellipse(screen, ORANGE, (body_x + 20, body_y + 80, 40, 25))
    # Задняя лапка
    pygame.draw.ellipse(screen, ORANGE, (body_x + 180, body_y + 80, 45, 30))
    
    # Хвост (пушистый, закрученный)
    tail_points = [
        (body_x + 250, body_y + 40),
        (body_x + 280, body_y + 30),
        (body_x + 290, body_y + 50),
        (body_x + 270, body_y + 60)
    ]
    pygame.draw.polygon(screen, ORANGE, tail_points)
    
    # Полоски на спине (для окраса)
    for i in range(3):
        x = body_x + 50 + i * 40
        pygame.draw.arc(screen, BROWN, (x, body_y + 10, 30, 40), 0, math.pi, 3)
    
    # Добавим подушку или фон для уюта
    pygame.draw.ellipse(screen, (150, 150, 150), (250, 400, 300, 30))  # Тень
    
    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

pygame.quit()