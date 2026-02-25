import pygame
from pygame.draw import *
from random import *
import math

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 700))

# цвета
light_brown = (181, 101, 29)
brown = (101, 67, 33)
light_blue = (173, 216, 230)
blue = (0, 0, 255)
grey = (150, 150, 150)
black = (0, 0, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)

def draw_background():
    """Рисует фон (землю и небо)"""
    rect(screen, light_brown, (0, 0, 1000, 400))
    rect(screen, brown, (0, 300, 1000, 400))

def draw_window(x, y, width=175, height=150):
    """Рисует окно с 4 стеклами"""
    # Основная рама окна
    rect(screen, light_blue, (x, y, width, height))
    rect(screen, blue, (x, y, width, height), 3)
    
    # Разделители (перекладины)
    line(screen, blue, (x + width//2, y), (x + width//2, y + height), 3)
    line(screen, blue, (x, y + height//2), (x + width, y + height//2), 3)
    
    # Стекла (можно закрасить голубым)
    rect(screen, light_blue, (x + 5, y + 5, width//2 - 10, height//2 - 10))
    rect(screen, light_blue, (x + width//2 + 5, y + 5, width//2 - 10, height//2 - 10))
    rect(screen, light_blue, (x + 5, y + height//2 + 5, width//2 - 10, height//2 - 10))
    rect(screen, light_blue, (x + width//2 + 5, y + height//2 + 5, width//2 - 10, height//2 - 10))

def draw_ball(x, y, radius=40):
    """Рисует клубок ниток"""
    circle(screen, black, (x, y), radius + 2)
    circle(screen, grey, (x, y), radius)
    
    # Рисуем несколько линий (нитки) внутри клубка
    for _ in range(8):
        angle = random() * 2 * math.pi
        length = radius * random() * 0.8
        x1 = x + length * math.cos(angle)
        y1 = y + length * math.sin(angle)
        x2 = x + length * math.cos(angle + math.pi)
        y2 = y + length * math.sin(angle + math.pi)
        line(screen, black, (x1, y1), (x2, y2), 2)

def draw_cat(x, y, scale=1.0, color=ORANGE):
    """
    Рисует лежащего кота
    x, y - центр тела кота
    scale - масштаб (1.0 = оригинальный размер)
    color - цвет кота
    """
    # Масштабируем все координаты
    body_width = int(250 * scale)
    body_height = int(120 * scale)
    head_radius = int(60 * scale)
    ear_size = int(50 * scale)
    
    # Центр головы относительно центра тела
    head_x = x - int(70 * scale)
    head_y = y - int(20 * scale)
    
    # Тело (главный овал)
    body_x = x - body_width//2
    body_y = y - body_height//2
    ellipse(screen, color, (body_x, body_y, body_width, body_height))
    ellipse(screen, black, (body_x, body_y, body_width, body_height), 2)
    
    # Голова
    circle(screen, color, (head_x, head_y), head_radius)
    circle(screen, black, (head_x, head_y), head_radius, 2)
    
    # Уши
    # Левое ухо
    left_ear = [(head_x - int(30 * scale), head_y - int(60 * scale)),  # вершина
                (head_x - int(55 * scale), head_y - int(15 * scale)),  # левая нижняя
                (head_x - int(15 * scale), head_y - int(25 * scale))]  # правая нижняя
    polygon(screen, color, left_ear)
    polygon(screen, black, left_ear, 2)
    
    # Внутренняя часть левого уха
    left_ear_inner = [(head_x - int(28 * scale), head_y - int(50 * scale)),
                      (head_x - int(45 * scale), head_y - int(20 * scale)),
                      (head_x - int(20 * scale), head_y - int(25 * scale))]
    polygon(screen, PINK, left_ear_inner)
    polygon(screen, black, left_ear_inner, 1)
    
    # Правое ухо
    right_ear = [(head_x + int(30 * scale), head_y - int(55 * scale)),  # вершина
                 (head_x + int(5 * scale), head_y - int(20 * scale)),   # левая нижняя
                 (head_x + int(45 * scale), head_y - int(25 * scale))]  # правая нижняя
    polygon(screen, color, right_ear)
    polygon(screen, black, right_ear, 2)
    
    # Внутренняя часть правого уха
    right_ear_inner = [(head_x + int(28 * scale), head_y - int(45 * scale)),
                       (head_x + int(10 * scale), head_y - int(25 * scale)),
                       (head_x + int(35 * scale), head_y - int(28 * scale))]
    polygon(screen, PINK, right_ear_inner)
    polygon(screen, black, right_ear_inner, 1)
    
    # Глаза
    eye_radius = int(10 * scale)
    pupil_radius = int(5 * scale)
    
    # Левый глаз
    circle(screen, WHITE, (head_x - int(20 * scale), head_y - int(10 * scale)), eye_radius)
    circle(screen, black, (head_x - int(20 * scale), head_y - int(10 * scale)), pupil_radius)
    circle(screen, WHITE, (head_x - int(22 * scale), head_y - int(12 * scale)), int(2 * scale))
    
    # Правый глаз
    circle(screen, WHITE, (head_x + int(20 * scale), head_y - int(10 * scale)), eye_radius)
    circle(screen, black, (head_x + int(20 * scale), head_y - int(10 * scale)), pupil_radius)
    circle(screen, WHITE, (head_x + int(18 * scale), head_y - int(12 * scale)), int(2 * scale))
    
    # Нос
    nose = [(head_x - int(5 * scale), head_y + int(10 * scale)),
            (head_x + int(5 * scale), head_y + int(10 * scale)),
            (head_x, head_y + int(20 * scale))]
    polygon(screen, PINK, nose)
    
    # Рот
    line(screen, black, (head_x, head_y + int(20 * scale)), 
         (head_x, head_y + int(35 * scale)), 2)
    line(screen, black, (head_x, head_y + int(35 * scale)), 
         (head_x - int(10 * scale), head_y + int(50 * scale)), 2)
    line(screen, black, (head_x, head_y + int(35 * scale)), 
         (head_x + int(10 * scale), head_y + int(50 * scale)), 2)
    
    # Усы
    # Левая сторона
    line(screen, black, (head_x - int(15 * scale), head_y + int(15 * scale)), 
         (head_x - int(40 * scale), head_y), 2)
    line(screen, black, (head_x - int(15 * scale), head_y + int(20 * scale)), 
         (head_x - int(40 * scale), head_y + int(20 * scale)), 2)
    line(screen, black, (head_x - int(15 * scale), head_y + int(25 * scale)), 
         (head_x - int(40 * scale), head_y + int(40 * scale)), 2)
    # Правая сторона
    line(screen, black, (head_x + int(15 * scale), head_y + int(15 * scale)), 
         (head_x + int(40 * scale), head_y), 2)
    line(screen, black, (head_x + int(15 * scale), head_y + int(20 * scale)), 
         (head_x + int(40 * scale), head_y + int(20 * scale)), 2)
    line(screen, black, (head_x + int(15 * scale), head_y + int(25 * scale)), 
         (head_x + int(40 * scale), head_y + int(40 * scale)), 2)
    
    # Лапы
    # Передние
    ellipse(screen, color, (x - int(70 * scale), y + int(50 * scale), 
                           int(70 * scale), int(45 * scale)))
    ellipse(screen, black, (x - int(70 * scale), y + int(50 * scale), 
                           int(70 * scale), int(45 * scale)), 2)
    
    # Задние
    ellipse(screen, color, (x + int(70 * scale), y + int(60 * scale), 
                           int(70 * scale), int(45 * scale)))
    ellipse(screen, black, (x + int(70 * scale), y + int(60 * scale), 
                           int(70 * scale), int(45 * scale)), 2)
    
    # Хвост
    tail_x = x + int(150 * scale)
    tail_y = y - int(20 * scale)
    ellipse(screen, color, (tail_x, tail_y, int(100 * scale), int(30 * scale)))
    ellipse(screen, black, (tail_x, tail_y, int(100 * scale), int(30 * scale)), 2)

def draw_wave(start_x, end_x, start_y, amplitude, frequency, color=grey, thickness=3):
    """Рисует волнистую линию"""
    points = []
    for x in range(start_x, end_x + 1):
        y = start_y + amplitude * math.sin(frequency * (x - start_x) * 2 * math.pi)
        points.append((x, int(y)))
    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, thickness)

# Основная программа
draw_background()

# Рисуем несколько окон
draw_window(400, 25)
draw_window(100, 50, 150, 120)
draw_window(700, 75, 200, 160)

# Рисуем несколько клубков
draw_ball(450, 450)
draw_ball(200, 550, 35)
draw_ball(600, 500, 45)
draw_ball(800, 600, 30)

# Рисуем несколько котов
draw_cat(300, 350)  # оригинальный кот
draw_cat(600, 400, 0.8, (200, 130, 0))  # кот поменьше, темнее
draw_cat(150, 500, 0.9, (220, 150, 50))  # еще один кот

# Рисуем волнистую линию
draw_wave(100, 900, 200, 50, 0.02, grey)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()