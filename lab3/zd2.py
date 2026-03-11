import pygame
from pygame.draw import *

pygame.init()

def choose_colors():
    '''
    Функция для выбора цветов зайца и глаз.
    Возвращает кортеж (цвет_зайца, цвет_глаз)
    '''
    # Список цветов для зайца
    hare_colors = [
        (210, 180, 140),  # 0 - коричневый
        (169, 169, 169),  # 1 - серый
        (255, 255, 255),  # 2 - белый
        (255, 140, 0),    # 3 - рыжий
        (50, 50, 50),     # 4 - чёрный
        (255, 255, 0),    # 5 - жёлтый
        (255, 192, 203),  # 6 - розовый
    ]
    
    # Список цветов для глаз
    eye_colors = [
        (0, 0, 255),      # 0 - синие
        (0, 255, 0),      # 1 - зелёные
        (139, 69, 19),    # 2 - карие
        (255, 0, 0),      # 3 - красные
        (255, 255, 0),    # 4 - жёлтые
        (128, 0, 128),    # 5 - фиолетовые
        (0, 0, 0),        # 6 - чёрные
    ]
    
    hare_names = ["коричневый", "серый", "белый", "рыжий", "чёрный", "жёлтый", "розовый"]
    eye_names = ["синие", "зелёные", "карие", "красные", "жёлтые", "фиолетовые", "чёрные"]
    
    print("=== Настройка зайца ===\n")
    
    # Вывод доступных цветов
    print("Доступные цвета зайца:")
    for i in range(len(hare_colors)):
        print(f"{i} - {hare_names[i]} {hare_colors[i]}")
    
    print("\nДоступные цвета глаз:")
    for i in range(len(eye_colors)):
        print(f"{i} - {eye_names[i]} {eye_colors[i]}")
    
    # Запрашиваем оба номера сразу
    print("\nВведи номера цветов через пробел (сначала заяц, потом глаза)")
    choices = input("Например: 3 1  (это рыжий заяц с зелёными глазами): ").split()
    
    # Проверяем, что ввели два числа
    if len(choices) == 2:
        hare_choice = int(choices[0])
        eye_choice = int(choices[1])
        
        # Проверяем, что числа в допустимом диапазоне
        if 0 <= hare_choice < len(hare_colors) and 0 <= eye_choice < len(eye_colors):
            hare_color = hare_colors[hare_choice]
            eye_color = eye_colors[eye_choice]
            
            print(f"\nВыбрано: {hare_names[hare_choice]} заяц ({hare_color}) с {eye_names[eye_choice]} глазами ({eye_color})")
            return hare_color, eye_color
    
    # Если что-то пошло не так, используем цвета по умолчанию
    print("\nНеверный ввод! Используются цвета по умолчанию: коричневый заяц с синими глазами")
    return hare_colors[0], eye_colors[0]


def draw_hare(surface, x, y, width, height, hare_color, eye_color):
    '''
    Рисует зайца на экране.
    surface - объект pygame.Surface
    x, y - координаты центра изображения
    width, height - ширина и высота изображения
    hare_color - цвет зайца (RGB)
    eye_color - цвет глаз (RGB)
    '''
    # Тело
    body_width = width // 2
    body_height = height // 2
    body_y = y + body_height // 2
    draw_body(surface, x, body_y, body_width, body_height, hare_color)
    
    # Голова
    head_size = height // 4
    head_y = y - head_size // 2
    draw_head(surface, x, head_y, head_size, hare_color)
    
    # Уши
    ear_height = height // 3
    ear_y = y - height // 2 + ear_height // 2
    for ear_x in (x - head_size // 4, x + head_size // 4):
        draw_ear(surface, ear_x, ear_y, width // 8, ear_height, hare_color)
    
    # Ноги
    leg_height = height // 16
    leg_y = y + height // 2 - leg_height // 2
    for leg_x in (x - width // 4, x + width // 4):
        draw_leg(surface, leg_x, leg_y, width // 4, leg_height, hare_color)
    
    # Глаза
    eye_size = head_size // 6
    eye_y = head_y - head_size // 8
    for eye_x in (x - head_size // 4, x + head_size // 4):
        draw_eye(surface, eye_x, eye_y, eye_size, eye_color)
    
    # Нос
    nose_size = head_size // 8
    nose_y = head_y + head_size // 8
    draw_nose(surface, x, nose_y, nose_size)
    
    # Усы
    whisker_length = head_size // 3
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


def draw_eye(surface, x, y, size, eye_color):
    '''
    Рисует глаз заданного цвета.
    eye_color - цвет радужки (RGB)
    '''
    # Белок
    circle(surface, (255, 255, 255), (x, y), size)
    # Радужка (цветная часть)
    iris_size = size // 2
    circle(surface, eye_color, (x, y), iris_size)
    # Зрачок
    pupil_size = iris_size // 2
    circle(surface, (0, 0, 0), (x, y), pupil_size)


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
        
# Выбираем цвета
HARE_COLOR, EYE_COLOR = choose_colors()

# Создаём окно
screen = pygame.display.set_mode((600, 600))
screen.fill((255, 255, 255))  # белый фон

# Рисуем зайца с выбранными цветами
draw_hare(screen, 300, 300, 200, 400, HARE_COLOR, EYE_COLOR)

pygame.display.update()
clock = pygame.time.Clock()
FPS = 30
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
