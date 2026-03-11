import pygame
from pygame.draw import *

pygame.init()



def draw_hare(surface, x, y, width, height, color):
    '''
    Рисует зайца на экране.
    surface - объект pygame.Surface
    x, y - координаты центра изображения
    width, height - ширина и высота изображения
    color - основной цвет (RGB)
    '''
    # Тело
    body_width = width // 2
    body_height = height // 2
    body_y = y + body_height // 2
    draw_body(surface, x, body_y, body_width, body_height, color)
    
    # Голова
    head_size = height // 4
    head_y = y - head_size // 2
    draw_head(surface, x, head_y, head_size, color)
    
    # Уши
    ear_height = height // 3
    ear_y = y - height // 2 + ear_height // 2
    for ear_x in (x - head_size // 4, x + head_size // 4):
        draw_ear(surface, ear_x, ear_y, width // 8, ear_height, color)
    
    # Ноги
    leg_height = height // 16
    leg_y = y + height // 2 - leg_height // 2
    for leg_x in (x - width // 4, x + width // 4):
        draw_leg(surface, leg_x, leg_y, width // 4, leg_height, color)
    
    # Глаза
    eye_size = head_size // 6
    eye_y = head_y - head_size // 8
    for eye_x in (x - head_size // 4, x + head_size // 4):
        draw_eye(surface, eye_x, eye_y, eye_size)
    
    # Нос
    nose_size = head_size // 8
    nose_y = head_y + head_size // 8
    draw_nose(surface, x, nose_y, nose_size)
    
    # Усы (теперь короче)
    whisker_length = head_size // 3  # Уменьшил с //2 до //3
    whisker_y = nose_y
    for side in (-1, 1):
        draw_whiskers(surface, x, whisker_y, whisker_length, side)


def draw_body(surface, x, y, width, height, color):
    '''Рисует тело зайца (овал).'''
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_head(surface, x, y, size, color):
    '''Рисует голову зайца (круг).'''
    circle(surface, color, (x, y), size // 2)


def draw_ear(surface, x, y, width, height, color):
    '''Рисует ухо зайца (овал).'''
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_leg(surface, x, y, width, height, color):
    '''Рисует ногу зайца (овал).'''
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_eye(surface, x, y, size):
    '''Рисует глаз (белый с чёрным зрачком).'''
    # Белок
    circle(surface, (255, 255, 255), (x, y), size)
    # Зрачок
    circle(surface, (0, 0, 0), (x, y), size // 2)


def draw_nose(surface, x, y, size):
    '''Рисует нос (розовый треугольник).'''
    points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
    polygon(surface, (255, 192, 203), points)


def draw_whiskers(surface, x, y, length, side):
    '''Рисует усы (по 3 линии с каждой стороны).'''
    for i in range(-1, 2):
        start_x = x + side * length // 4
        start_y = y + i * length // 4
        end_x = x + side * length
        end_y = y + i * length // 2
        line(surface, (0, 0, 0), (start_x, start_y), (end_x, end_y), 1)

        
FPS = 30
screen = pygame.display.set_mode((600, 600))
screen.fill((255, 255, 255))  # белый фон

# Рисуем зайца
draw_hare(screen, 300, 300, 200, 400, (210, 180, 140))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()