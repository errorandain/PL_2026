import pygame
from pygame.draw import *
from random import *
import math

pygame.init()

FPS = 30
screen = pygame.display.set_mode((600, 500))

# цвета
light_brown = (181, 101, 29)
brown = (101, 67, 33)
light_blue = (173, 216, 230)
blue = (0, 0, 255)
grey = (150, 150, 150)
black = (0, 0, 0)

# фон
rect(screen, light_brown, (0, 0, 600, 300))
rect(screen, brown, (0, 200, 600, 400))

# окно
rect(screen, light_blue, (400, 25, 175, 150))
rect(screen, blue, (400+10, 25+10, 70, 60))
rect(screen, blue, (400+10, 25+10+70, 70, 60))
rect(screen, blue, (400+10+60+10+10, 25+10, 70, 60))
rect(screen, blue, (400+10+60+10+10, 25+10+70, 70, 60))

# клубок
circle(screen, black, (450, 450), 42)
circle(screen, grey, (450, 450), 40)

# ===== Цвета =====
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)

# ===== Тело (главный овал) =====
# Горизонтальный овал — кот лежит на левом боку
ellipse(screen, ORANGE, (150, 180, 250, 120))
ellipse(screen, BLACK, (150, 180, 250, 120), 2)

# ===== Голова (круг) — рядом с телом слева =====
circle(screen, ORANGE, (180, 200), 60)

# ===== УШИ С РОЗОВОЙ ВНУТРЕННЕЙ ЧАСТЬЮ =====
# Левое ухо (основная часть)
polygon(screen, ORANGE, [(125, 120),    # вершина
                         (125, 177),    # левая нижняя точка
                         (165, 145)])   # правая нижняя точка
polygon(screen, BLACK, [(125, 120), (125, 177), (165, 145)], 1)

# Внутренняя часть левого уха (розовая)
polygon(screen, PINK, [(130, 135),      # вершина (чуть ниже и правее)
                       (130, 167),      # левая нижняя точка
                       (158, 148)])     # правая нижняя точка
# Правое ухо (основная часть)
polygon(screen, ORANGE, [(235, 120),    # вершина
                         (195, 140),    # левая нижняя точка
                         (235, 177)])   # правая нижняя точка
polygon(screen, BLACK, [(235, 120), (195, 140), (235, 177)], 1)

# Внутренняя часть правого уха (розовая)
polygon(screen, PINK, [(225, 135),      # вершина (чуть ниже и левее)
                       (200, 145),      # левая нижняя точка
                       (225, 167)])     # правая нижняя точка

# ===== Глаза =====
# Левый глаз
circle(screen, WHITE, (160, 190), 10)
circle(screen, BLACK, (160, 190), 5)
circle(screen, WHITE, (157, 187), 2)  # блик
# Правый глаз
circle(screen, WHITE, (200, 190), 10)
circle(screen, BLACK, (200, 190), 5)
circle(screen, WHITE, (197, 187), 2)

# ===== Нос =====
polygon(screen, PINK, [(175, 210), (185, 210), (180, 220)])

# ===== Рот =====
line(screen, BLACK, (180, 220), (180, 235), 2)
line(screen, BLACK, (180, 235), (170, 250), 2)
line(screen, BLACK, (180, 235), (190, 250), 2)

# ===== Усы =====
# Левая сторона
line(screen, BLACK, (165, 215), (125, 200), 2)
line(screen, BLACK, (165, 220), (125, 220), 2)
line(screen, BLACK, (165, 225), (125, 240), 2)
# Правая сторона
line(screen, BLACK, (195, 215), (235, 200), 2)
line(screen, BLACK, (195, 220), (235, 220), 2)
line(screen, BLACK, (195, 225), (235, 240), 2)

# ===== Лапы (под телом) =====
# Передние лапы (под грудью)
ellipse(screen, ORANGE, (160, 260, 70, 45))   # левая передняя
ellipse(screen, BLACK, (160, 260, 70, 45), 2)   # левая передняя

# Задние лапы (под животом)
ellipse(screen, ORANGE, (310, 270, 70, 45))   # левая задняя
ellipse(screen, black, (310, 270, 70, 45), 2) 
ellipse(screen, ORANGE, (360, 275+25, 45/1.5, 65/1.5))   # правая задняя
ellipse(screen, black, (360, 275+25, 45/1.5, 65/1.5), 2)  

# ===== Обводка головы =====
circle(screen, BLACK, (180, 200), 60, 2)

# хвост
ellipse(screen, ORANGE, (150+180, 180, 250/1.7, 120/3.3))
ellipse(screen, BLACK, (150+180, 180, 250/1.7, 120/3.3), 2)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()