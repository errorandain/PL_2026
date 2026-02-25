import pygame
from pygame.draw import *

pygame.init()
screen = pygame.display.set_mode((400, 400))

# Цвета
GRAY = (211, 211, 211)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GRAY)

    # Лицо
    circle(screen, YELLOW, (200, 200), 100)
    circle(screen, BLACK, (200, 200), 100, 1) # Тонкий контур

    # Красные глаза с черными зрачками
    # Левый
    circle(screen, RED, (160, 180), 18)
    circle(screen, BLACK, (160, 180), 6)
    # Правый
    circle(screen, RED, (240, 180), 18)
    circle(screen, BLACK, (240, 180), 6)

    # Брови (толстые наклонные линии)
    line(screen, BLACK, (120, 120), (185, 170), 12) # Левая
    line(screen, BLACK, (280, 140), (215, 175), 12) # Правая

    # Рот (черный прямоугольник)
    # rect: [отступ слева, отступ сверху, ширина, высота]
    rect(screen, BLACK, (150, 250, 100, 20))

    pygame.display.flip()

pygame.quit()
