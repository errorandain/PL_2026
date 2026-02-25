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
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)

# ===== фон =====
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

# ===== функция для рисования одного кота с заданным смещением и масштабом =====
def draw_cat(surface, shift_x, shift_y, scale, mirrored=False):
    if not mirrored:
        # Обычный кот (смотрит вправо)
        # Тело (главный овал)
        ellipse(surface, ORANGE, (shift_x + 150*scale, shift_y + 180*scale, 250*scale, 120*scale))
        ellipse(surface, black, (shift_x + 150*scale, shift_y + 180*scale, 250*scale, 120*scale), 2)

        # Голова
        circle(surface, ORANGE, (int(shift_x + 180*scale), int(shift_y + 200*scale)), int(60*scale))
        circle(surface, black, (int(shift_x + 180*scale), int(shift_y + 200*scale)), int(60*scale), 2)

        # Левое ухо (основное)
        polygon(surface, ORANGE,
                [(shift_x + 125*scale, shift_y + 120*scale),
                 (shift_x + 125*scale, shift_y + 177*scale),
                 (shift_x + 165*scale, shift_y + 145*scale)])
        polygon(surface, black,
                [(shift_x + 125*scale, shift_y + 120*scale),
                 (shift_x + 125*scale, shift_y + 177*scale),
                 (shift_x + 165*scale, shift_y + 145*scale)], 1)

        # Внутренняя часть левого уха
        polygon(surface, PINK,
                [(shift_x + 130*scale, shift_y + 135*scale),
                 (shift_x + 130*scale, shift_y + 167*scale),
                 (shift_x + 158*scale, shift_y + 148*scale)])

        # Правое ухо (основное)
        polygon(surface, ORANGE,
                [(shift_x + 235*scale, shift_y + 120*scale),
                 (shift_x + 195*scale, shift_y + 140*scale),
                 (shift_x + 235*scale, shift_y + 177*scale)])
        polygon(surface, black,
                [(shift_x + 235*scale, shift_y + 120*scale),
                 (shift_x + 195*scale, shift_y + 140*scale),
                 (shift_x + 235*scale, shift_y + 177*scale)], 1)

        # Внутренняя часть правого уха
        polygon(surface, PINK,
                [(shift_x + 225*scale, shift_y + 135*scale),
                 (shift_x + 200*scale, shift_y + 145*scale),
                 (shift_x + 225*scale, shift_y + 167*scale)])

        # Глаза
        # Левый
        circle(surface, WHITE, (int(shift_x + 160*scale), int(shift_y + 190*scale)), int(10*scale))
        circle(surface, black, (int(shift_x + 160*scale), int(shift_y + 190*scale)), int(5*scale))
        circle(surface, WHITE, (int(shift_x + 157*scale), int(shift_y + 187*scale)), int(2*scale))
        # Правый
        circle(surface, WHITE, (int(shift_x + 200*scale), int(shift_y + 190*scale)), int(10*scale))
        circle(surface, black, (int(shift_x + 200*scale), int(shift_y + 190*scale)), int(5*scale))
        circle(surface, WHITE, (int(shift_x + 197*scale), int(shift_y + 187*scale)), int(2*scale))

        # Нос
        polygon(surface, PINK,
                [(shift_x + 175*scale, shift_y + 210*scale),
                 (shift_x + 185*scale, shift_y + 210*scale),
                 (shift_x + 180*scale, shift_y + 220*scale)])

        # Рот
        line(surface, black, (shift_x + 180*scale, shift_y + 220*scale), (shift_x + 180*scale, shift_y + 235*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + 180*scale, shift_y + 235*scale), (shift_x + 170*scale, shift_y + 250*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + 180*scale, shift_y + 235*scale), (shift_x + 190*scale, shift_y + 250*scale), max(1, int(2*scale)))

        # Усы
        # Левая сторона
        line(surface, black, (shift_x + 165*scale, shift_y + 215*scale), (shift_x + 125*scale, shift_y + 200*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + 165*scale, shift_y + 220*scale), (shift_x + 125*scale, shift_y + 220*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + 165*scale, shift_y + 225*scale), (shift_x + 125*scale, shift_y + 240*scale), max(1, int(2*scale)))
        # Правая сторона
        line(surface, black, (shift_x + 195*scale, shift_y + 215*scale), (shift_x + 235*scale, shift_y + 200*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + 195*scale, shift_y + 220*scale), (shift_x + 235*scale, shift_y + 220*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + 195*scale, shift_y + 225*scale), (shift_x + 235*scale, shift_y + 240*scale), max(1, int(2*scale)))

        # Передние лапы
        ellipse(surface, ORANGE, (shift_x + 160*scale, shift_y + 260*scale, 70*scale, 45*scale))
        ellipse(surface, black, (shift_x + 160*scale, shift_y + 260*scale, 70*scale, 45*scale), 2)

        # Задние лапы
        ellipse(surface, ORANGE, (shift_x + 310*scale, shift_y + 270*scale, 70*scale, 45*scale))
        ellipse(surface, black, (shift_x + 310*scale, shift_y + 270*scale, 70*scale, 45*scale), 2)
        ellipse(surface, ORANGE, (shift_x + 360*scale, shift_y + (275+25)*scale, (45/1.5)*scale, (65/1.5)*scale))
        ellipse(surface, black, (shift_x + 360*scale, shift_y + (275+25)*scale, (45/1.5)*scale, (65/1.5)*scale), 2)

        # Хвост
        ellipse(surface, ORANGE, (shift_x + (150+180)*scale, shift_y + 180*scale, (250/1.7)*scale, (120/3.3)*scale))
        ellipse(surface, black, (shift_x + (150+180)*scale, shift_y + 180*scale, (250/1.7)*scale, (120/3.3)*scale), 2)
    
    else:
        # Отзеркаленный кот (смотрит влево)
        # Для отзеркаливания меняем x координаты: новый_x = shift_x + 400*scale - (старый_x - shift_x)
        # Но проще пересчитать все координаты заново с зеркальным отображением
        
        # Тело
        ellipse(surface, ORANGE, (shift_x + (400-150-250)*scale, shift_y + 180*scale, 250*scale, 120*scale))
        ellipse(surface, black, (shift_x + (400-150-250)*scale, shift_y + 180*scale, 250*scale, 120*scale), 2)

        # Голова
        circle(surface, ORANGE, (int(shift_x + (400-180)*scale), int(shift_y + 200*scale)), int(60*scale))
        circle(surface, black, (int(shift_x + (400-180)*scale), int(shift_y + 200*scale)), int(60*scale), 2)

        # Левое ухо (теперь это правое ухо в отражении)
        polygon(surface, ORANGE,
                [(shift_x + (400-235)*scale, shift_y + 120*scale),
                 (shift_x + (400-195)*scale, shift_y + 140*scale),
                 (shift_x + (400-235)*scale, shift_y + 177*scale)])
        polygon(surface, black,
                [(shift_x + (400-235)*scale, shift_y + 120*scale),
                 (shift_x + (400-195)*scale, shift_y + 140*scale),
                 (shift_x + (400-235)*scale, shift_y + 177*scale)], 1)

        # Внутренняя часть (розовая)
        polygon(surface, PINK,
                [(shift_x + (400-225)*scale, shift_y + 135*scale),
                 (shift_x + (400-200)*scale, shift_y + 145*scale),
                 (shift_x + (400-225)*scale, shift_y + 167*scale)])

        # Правое ухо (теперь это левое ухо в отражении)
        polygon(surface, ORANGE,
                [(shift_x + (400-125)*scale, shift_y + 120*scale),
                 (shift_x + (400-125)*scale, shift_y + 177*scale),
                 (shift_x + (400-165)*scale, shift_y + 145*scale)])
        polygon(surface, black,
                [(shift_x + (400-125)*scale, shift_y + 120*scale),
                 (shift_x + (400-125)*scale, shift_y + 177*scale),
                 (shift_x + (400-165)*scale, shift_y + 145*scale)], 1)

        # Внутренняя часть (розовая)
        polygon(surface, PINK,
                [(shift_x + (400-130)*scale, shift_y + 135*scale),
                 (shift_x + (400-130)*scale, shift_y + 167*scale),
                 (shift_x + (400-158)*scale, shift_y + 148*scale)])

        # Глаза (меняем местами)
        # Левый глаз (в отражении это правый)
        circle(surface, WHITE, (int(shift_x + (400-200)*scale), int(shift_y + 190*scale)), int(10*scale))
        circle(surface, black, (int(shift_x + (400-200)*scale), int(shift_y + 190*scale)), int(5*scale))
        circle(surface, WHITE, (int(shift_x + (400-197)*scale), int(shift_y + 187*scale)), int(2*scale))
        # Правый глаз (в отражении это левый)
        circle(surface, WHITE, (int(shift_x + (400-160)*scale), int(shift_y + 190*scale)), int(10*scale))
        circle(surface, black, (int(shift_x + (400-160)*scale), int(shift_y + 190*scale)), int(5*scale))
        circle(surface, WHITE, (int(shift_x + (400-157)*scale), int(shift_y + 187*scale)), int(2*scale))

        # Нос
        polygon(surface, PINK,
                [(shift_x + (400-185)*scale, shift_y + 210*scale),
                 (shift_x + (400-175)*scale, shift_y + 210*scale),
                 (shift_x + (400-180)*scale, shift_y + 220*scale)])

        # Рот
        line(surface, black, (shift_x + (400-180)*scale, shift_y + 220*scale), (shift_x + (400-180)*scale, shift_y + 235*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + (400-180)*scale, shift_y + 235*scale), (shift_x + (400-190)*scale, shift_y + 250*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + (400-180)*scale, shift_y + 235*scale), (shift_x + (400-170)*scale, shift_y + 250*scale), max(1, int(2*scale)))

        # Усы
        # Левая сторона (в отражении)
        line(surface, black, (shift_x + (400-195)*scale, shift_y + 215*scale), (shift_x + (400-235)*scale, shift_y + 200*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + (400-195)*scale, shift_y + 220*scale), (shift_x + (400-235)*scale, shift_y + 220*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + (400-195)*scale, shift_y + 225*scale), (shift_x + (400-235)*scale, shift_y + 240*scale), max(1, int(2*scale)))
        # Правая сторона (в отражении)
        line(surface, black, (shift_x + (400-165)*scale, shift_y + 215*scale), (shift_x + (400-125)*scale, shift_y + 200*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + (400-165)*scale, shift_y + 220*scale), (shift_x + (400-125)*scale, shift_y + 220*scale), max(1, int(2*scale)))
        line(surface, black, (shift_x + (400-165)*scale, shift_y + 225*scale), (shift_x + (400-125)*scale, shift_y + 240*scale), max(1, int(2*scale)))

        # Передние лапы
        ellipse(surface, ORANGE, (shift_x + (400-160-70)*scale, shift_y + 260*scale, 70*scale, 45*scale))
        ellipse(surface, black, (shift_x + (400-160-70)*scale, shift_y + 260*scale, 70*scale, 45*scale), 2)

        # Задние лапы
        ellipse(surface, ORANGE, (shift_x + (400-310-70)*scale, shift_y + 270*scale, 70*scale, 45*scale))
        ellipse(surface, black, (shift_x + (400-310-70)*scale, shift_y + 270*scale, 70*scale, 45*scale), 2)
        ellipse(surface, ORANGE, (shift_x + (400-360-(45/1.5))*scale, shift_y + (275+25)*scale, (45/1.5)*scale, (65/1.5)*scale))
        ellipse(surface, black, (shift_x + (400-360-(45/1.5))*scale, shift_y + (275+25)*scale, (45/1.5)*scale, (65/1.5)*scale), 2)

        # Хвост
        ellipse(surface, ORANGE, (shift_x + (400-150-180-(250/1.7))*scale, shift_y + 180*scale, (250/1.7)*scale, (120/3.3)*scale))
        ellipse(surface, black, (shift_x + (400-150-180-(250/1.7))*scale, shift_y + 180*scale, (250/1.7)*scale, (120/3.3)*scale), 2)

# ===== рисуем орду котов =====
num_cats = 5  # количество котов в орде
for _ in range(num_cats):
    scale = uniform(0.3, 0.7)                # случайный размер
    mirrored = choice([True, False])         # случайное направление
    
    # Коты должны быть только на коричневом фоне (нижняя часть)
    min_y = 200 - 120 * scale
    max_y = 500 - 330 * scale
    
    if max_y > min_y:
        y = randint(int(min_y), int(max_y))
    else:
        y = int(min_y)
    
    # Случайное положение по x с учетом размера
    max_x = 600 - 400 * scale
    if max_x > 0:
        x = randint(0, int(max_x))
    else:
        x = 0
    
    draw_cat(screen, x, y, scale, mirrored)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()