import pygame
import random  # Модуль для случайной генерации чисел
from pygame.draw import *

pygame.init()


DEFAULT_EYE_COLOR = (0, 0, 0)          # чёрные глаза (RGB: красный, зелёный, синий)
DEFAULT_NOSE_COLOR = (255, 192, 203)   # розовый нос

# Параметры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)  # белый фон

# Список цветов для зайцев - каждый цвет это кортеж из 3 чисел (R, G, B)
HARE_COLORS = [
    (210, 180, 140),  # коричневый
    (169, 169, 169),  # серый
    (255, 255, 255),  # белый
    (255, 140, 0),    # рыжий
    (50, 50, 50),     # чёрный
    (255, 255, 0),    # жёлтый
    (255, 192, 203),  # розовый
    (150, 75, 0),     # тёмно-коричневый
    (200, 200, 200),  # светло-серый
    (255, 200, 150),  # бежевый
]

# Названия цветов (для вывода в консоль)
COLOR_NAMES = [
    "коричневый", "серый", "белый", "рыжий", "чёрный", 
    "жёлтый", "розовый", "тёмно-коричневый", "светло-серый", "бежевый"
]


# ============================== ФУНКЦИЯ ГЕНЕРАЦИИ ==============================
def generate_random_hares():
    '''
    Генерирует случайных зайцев.
    Возвращает список зайцев с их параметрами.
    
    Функция не принимает параметры, но использует глобальные константы
    '''
    # random.randint(1, 8) генерирует случайное число от 1 до 8
    count = random.randint(1, 8)
    
    print(f"=== ГЕНЕРАЦИЯ {count} СЛУЧАЙНЫХ ЗАЙЦЕВ ===\n")
    
    hares = []  # пустой список для хранения зайцев
    
    # Цикл для создания каждого зайца
    for i in range(count):
        # Случайные координаты (с отступом от краёв)
        x = random.randint(150, SCREEN_WIDTH - 150)
        y = random.randint(150, SCREEN_HEIGHT - 150)
        
        # Случайные размеры
        width = random.randint(80, 250)
        height = random.randint(150, 400)
        
        # Случайный цвет из списка HARE_COLORS
        color_index = random.randint(0, len(HARE_COLORS) - 1)
        hare_color = HARE_COLORS[color_index]
        
        # Случайный цвет глаз (полностью случайный RGB)
        eye_color = (
            random.randint(0, 255),  # красный
            random.randint(0, 255),  # зелёный
            random.randint(0, 255)   # синий
        )
        
        # Добавляем зайца в список как кортеж из 6 элементов
        hares.append((x, y, width, height, hare_color, eye_color))
        
        # Выводим информацию в консоль
        print(f"Заяц {i+1}: {COLOR_NAMES[color_index]}, "
              f"позиция ({x}, {y}), размер {width}x{height}, "
              f"глаза RGB{eye_color}")
    
    return hares  # возвращаем список зайцев


# ============================ ФУНКЦИИ РИСОВАНИЯ ============================
# Все функции рисования принимают surface (поверхность для рисования)
# и координаты/размеры/цвета

def draw_hare(surface, x, y, width, height, main_color, eye_color, nose_color):
    '''
    ГЛАВНАЯ ФУНКЦИЯ: рисует целого зайца, вызывая другие функции
    
    Параметры:
    surface - где рисовать (экран или другая поверхность)
    x, y - координаты ЦЕНТРА зайца
    width, height - ширина и высота всего зайца
    main_color - цвет шерсти
    eye_color - цвет глаз
    nose_color - цвет носа
    
    ВАЖНО: все размеры частей рассчитываются относительно width и height
    Поэтому заяц автоматически масштабируется при изменении размеров
    '''
    # ---- Расчёт размеров головы ----
    # Голова занимает 1/4 от высоты всего зайца
    head_size = height // 4  # // это целочисленное деление
    head_y = y - head_size // 2  # голова выше центра
    
    # ---- Тело ----
    body_width = width // 2
    body_height = height // 2
    # Тело ниже центра (body_y)
    body_y = y + body_height // 2
    draw_body(surface, x, body_y, body_width, body_height, main_color)

    # ---- Голова ----
    draw_head(surface, x, head_y, head_size, main_color)

    # ---- Уши (2 штуки) ----
    ear_height = height // 3
    ear_width = width // 8
    ear_y = y - height // 2 + ear_height // 2  # уши вверху
    # Координаты X для левого и правого уха
    ear_positions = (x - head_size // 4, x + head_size // 4)
    # Цикл для рисования двух ушей
    for ear_x in ear_positions:
        draw_ear(surface, ear_x, ear_y, ear_width, ear_height, main_color)
    
    # ---- Ноги (2 штуки) ----
    leg_height = height // 16
    leg_width = width // 4
    leg_y = y + height // 2 - leg_height // 2  # ноги внизу
    leg_positions = (x - width // 4, x + width // 4)
    for leg_x in leg_positions:
        draw_leg(surface, leg_x, leg_y, leg_width, leg_height, main_color)
    
    # ---- Глаза (2 штуки) ----
    eye_size = head_size // 6
    eye_y = head_y - head_size // 8  # глаза в верхней части головы
    eye_positions = (x - head_size // 4, x + head_size // 4)
    for eye_x in eye_positions:
        draw_eye(surface, eye_x, eye_y, eye_size, eye_color)
    
    # ---- Нос (1 штука) ----
    nose_size = head_size // 8
    nose_y = head_y + head_size // 8  # нос ниже центра головы
    draw_nose(surface, x, nose_y, nose_size, nose_color)
    
    # ---- Усы (слева и справа) ----
    whisker_length = head_size // 3
    whisker_y = nose_y
    # side = -1 для левой стороны, side = 1 для правой
    for side in (-1, 1):
        draw_whiskers(surface, x, whisker_y, whisker_length, side)


def draw_body(surface, x, y, width, height, color):
    '''Рисует тело зайца (овал).'''
    # x - width//2, y - height//2 - это левый верхний угол овала
    # width, height - размеры овала
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_head(surface, x, y, size, color):
    '''Рисует голову зайца (круг).'''
    # size - диаметр, size//2 - радиус
    circle(surface, color, (x, y), size // 2)


def draw_ear(surface, x, y, width, height, color):
    '''Рисует ухо зайца (овал).'''
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_leg(surface, x, y, width, height, color):
    '''Рисует ногу зайца (овал).'''
    ellipse(surface, color, (x - width // 2, y - height // 2, width, height))


def draw_eye(surface, x, y, size, eye_color):
    '''
    Рисует глаз с белком, радужкой и зрачком.
    '''
    # Белок (внешний круг)
    circle(surface, (255, 255, 255), (x, y), size)
    
    # Радужка (цветная часть, размером в половину белка)
    iris_size = size // 2
    circle(surface, eye_color, (x, y), iris_size)
    
    # Зрачок (чёрный, размером в половину радужки)
    pupil_size = iris_size // 2
    circle(surface, (0, 0, 0), (x, y), pupil_size)
    
    # Блик (белая точка для объёма) - только у 70% зайцев
    if random.random() > 0.3:  # random() даёт число от 0 до 1
        highlight_size = pupil_size // 3
        highlight_x = x - pupil_size // 3
        highlight_y = y - pupil_size // 3
        circle(surface, (255, 255, 255), (highlight_x, highlight_y), highlight_size)


def draw_nose(surface, x, y, size, nose_color):
    '''Рисует нос (треугольник).'''
    # Три точки треугольника
    points = [
        (x, y - size),           # верхняя точка
        (x - size, y + size),    # левая нижняя
        (x + size, y + size)     # правая нижняя
    ]
    polygon(surface, nose_color, points)


def draw_whiskers(surface, x, y, length, side):
    '''
    Рисует усы с одной стороны.
    side: -1 для левой стороны, 1 для правой
    '''
    # Рисуем 3 уса: верхний, средний, нижний
    for i in range(-1, 2):  # i будет -1, 0, 1
        start_x = x + side * length // 4
        start_y = y + i * length // 4
        end_x = x + side * length
        end_y = y + i * length // 2
        # Толщина линии = 1 пиксель
        line(surface, (0, 0, 0), (start_x, start_y), (end_x, end_y), 1)


# =============================== ГЛАВНАЯ ФУНКЦИЯ ===============================
def main():
    '''
    Основная функция программы.
    Здесь происходит:
    1. Получение параметров
    2. Создание окна
    3. Рисование зайцев
    4. Главный цикл обработки событий
    '''
    
    print("=== ГЕНЕРАТОР СЛУЧАЙНЫХ ЗАЙЦЕВ ===\n")
    print("Нажми ПРОБЕЛ чтобы сгенерировать новых зайцев")
    print("Закрой окно для выхода\n")
    
    # Генерируем случайных зайцев
    hares = generate_random_hares()
    
    # Создаём окно
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"{len(hares)} случайных зайцев")
    screen.fill(BACKGROUND_COLOR)
    
    # Рисуем всех зайцев
    for hare in hares:
        # Распаковываем кортеж с параметрами зайца
        x, y, width, height, hare_color, eye_color = hare
        draw_hare(screen, x, y, width, height, 
                 hare_color, eye_color, DEFAULT_NOSE_COLOR)
    
    # Добавляем номера зайцев (для красоты)
    font = pygame.font.Font(None, 20)  # шрифт размера 20
    for i, hare in enumerate(hares):
        x, y, width, height, _, _ = hare
        text = font.render(f"#{i+1}", True, (100, 100, 100))
        screen.blit(text, (x - 15, y - height//2 - 20))
    
    pygame.display.update()  # обновляем экран
    
    # ============================ ГЛАВНЫЙ ЦИКЛ ============================
    # Здесь программа работает, пока пользователь не закроет окно
    
    clock = pygame.time.Clock()
    FPS = 30  # кадров в секунду
    running = True
    
    while running:
        clock.tick(FPS)  # ограничиваем скорость цикла
        
        # Обрабатываем все события (нажатия клавиш, движения мыши и т.д.)
        for event in pygame.event.get():
            # Если нажали крестик закрытия окна
            if event.type == pygame.QUIT:
                running = False
            
            # Если нажали клавишу
            elif event.type == pygame.KEYDOWN:
                # Если нажали ПРОБЕЛ
                if event.key == pygame.K_SPACE:
                    # Очищаем экран
                    screen.fill(BACKGROUND_COLOR)
                    
                    # Генерируем новых зайцев
                    hares = generate_random_hares()
                    
                    # Рисуем их
                    for hare in hares:
                        x, y, width, height, hare_color, eye_color = hare
                        draw_hare(screen, x, y, width, height, 
                                 hare_color, eye_color, DEFAULT_NOSE_COLOR)
                    
                    # Обновляем номера
                    for i, hare in enumerate(hares):
                        x, y, width, height, _, _ = hare
                        text = font.render(f"#{i+1}", True, (100, 100, 100))
                        screen.blit(text, (x - 15, y - height//2 - 20))
                    
                    # Показываем обновлённый экран
                    pygame.display.update()
                    print(f"\n Сгенерировано {len(hares)} новых зайцев!")
    
    # Выходим из pygame
    pygame.quit()

main()