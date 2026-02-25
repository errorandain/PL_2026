import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((500, 500))
screen.fill((255, 255, 255))  # белый фон

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

# ===== УШИ с розовой внутренней частью =====
# Левое ухо (основная часть)
polygon(screen, ORANGE, [(125, 120),    # вершина
                         (125, 177),    # левая нижняя точка
                         (165, 145)])   # правая нижняя точка




# Правое ухо (основная часть)
polygon(screen, ORANGE, [(235, 120),    # вершина
                         (195, 140),    # левая нижняя точка
                         (235, 177)])   # правая нижняя точка
polygon(screen, BLACK, [(235, 120),(195, 140),(235, 177)], 1)


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
ellipse(screen, ORANGE, (160, 260, 45, 70))   # левая передняя
ellipse(screen, ORANGE, (210, 265, 45, 65))   # правая передняя

# Задние лапы (под животом)
ellipse(screen, ORANGE, (310, 270, 45, 70))   # левая задняя
ellipse(screen, ORANGE, (360, 275, 45, 65))   # правая задняя

# ===== Обводка головы =====
circle(screen, BLACK, (180, 200), 60, 2)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()