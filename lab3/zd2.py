import pygame
import random
from pygame.draw import *

pygame.init()

# Константы
DEFAULT_EYE_COLOR = (0, 0, 0)          # чёрные глаза
DEFAULT_NOSE_COLOR = (255, 192, 203)   # розовый нос

# Параметры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)  # белый

# Список цветов для зайцев
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

COLOR_NAMES = [
    "коричневый", "серый", "белый", "рыжий", "чёрный", 
    "жёлтый", "розовый", "тёмно-коричневый", "светло-серый", "бежевый"
]

def generate_random_hares():
    '''
    Генерирует случайных зайцев.
    Возвращает список зайцев с их параметрами.
    '''
    # Случайное количество зайцев (от 1 до 8)
    count = random.randint(1, 8)
    
    print(f"=== ГЕНЕРАЦИЯ {count} СЛУЧАЙНЫХ ЗАЙЦЕВ ===\n")
    
    hares = []
    
    for i in range(count):
        # Случайные координаты (с отступом от краёв)
        x = random.randint(150, SCREEN_WIDTH - 150)
        y = random.randint(150, SCREEN_HEIGHT - 150)
        
        # Случайные размеры
        width = random.randint(80, 250)
        height = random.randint(150, 400)
        
        # Случайный цвет
        color_index = random.randint(0, len(HARE_COLORS) - 1)
        hare_color = HARE_COLORS[color_index]
        
        # Случайный размер глаз (немного варьируется)
        eye_color = (
            random.randint(0, 255),
            random.randint(0, 255), 
            random.randint(0, 255)
        )
        
        hares.append((x, y, width, height, hare_color, eye_color))
        
        print(f"Заяц {i+1}: {COLOR_NAMES[color_index]}, "
              f"позиция ({x}, {y}), размер {width}x{height}, "
              f"глаза RGB{eye_color}")
    
    return hares


def draw_hare(surface, x, y, width, height, main_color, eye_color, nose_color):
    '''
    Рисует зайца на экране.
    '''
    # Расчёт координат для всех частей
    head_size = height // 4
    head_y = y - head_size // 2
    
    # Тело
    body_width = width // 2
    body_height = height // 2
    body_y = y + body_height // 2
    draw_body(surface, x, body_y, body_width, body_height, main_color)

    # Голова
    draw_head(surface, x, head_y, head_size, main_color)

    # Уши
    ear_height = height // 3
    ear_width = width // 8
    ear_y = y - height // 2 + ear_height // 2
    ear_positions = (x - head_size // 4, x + head_size // 4)
    for ear_x in ear_positions:
        draw_ear(surface, ear_x, ear_y, ear_width, ear_height, main_color)
    
    # Ноги
    leg_height = height // 16
    leg_width = width // 4
    leg_y = y + height // 2 - leg_height // 2
    leg_positions = (x - width // 4, x + width // 4)
    for leg_x in leg_positions:
        draw_leg(surface, leg_x, leg_y, leg_width, leg_height, main_color)
    
    # Глаза
    eye_size = head_size // 6
    eye_y = head_y - head_size // 8
    eye_positions = (x - head_size // 4, x + head_size // 4)
    for eye_x in eye_positions:
        draw_eye(surface, eye_x, eye_y, eye_size, eye_color)
    
    # Нос
    nose_size = head_size // 8
    nose_y = head_y + head_size // 8
    draw_nose(surface, x, nose_y, nose_size, nose_color)
    
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
    Рисует глаз с белком и зрачком.
    '''
    # Белок
    circle(surface, (255, 255, 255), (x, y), size)
    # Радужка
    iris_size = size // 2
    circle(surface, eye_color, (x, y), iris_size)
    # Зрачок
    pupil_size = iris_size // 2
    circle(surface, (0, 0, 0), (x, y), pupil_size)
    # Блик (случайный для разнообразия)
    if random.random() > 0.3:  # 70% зайцев с бликом
        highlight_size = pupil_size // 3
        highlight_x = x - pupil_size // 3
        highlight_y = y - pupil_size // 3
        circle(surface, (255, 255, 255), (highlight_x, highlight_y), highlight_size)


def draw_nose(surface, x, y, size, nose_color):
    '''Рисует нос (треугольник).'''
    points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
    polygon(surface, nose_color, points)


def draw_whiskers(surface, x, y, length, side):
    '''Рисует усы (по 3 линии с каждой стороны).'''
    for i in range(-1, 2):
        start_x = x + side * length // 4
        start_y = y + i * length // 4
        end_x = x + side * length
        end_y = y + i * length // 2
        line(surface, (0, 0, 0), (start_x, start_y), (end_x, end_y), 1)


def main():
    '''Основная функция программы.'''
    
    # Спрашиваем только количество или генерировать автоматически
    print("=== ГЕНЕРАТОР СЛУЧАЙНЫХ ЗАЙЦЕВ ===\n")
    choice = input("Нажми Enter для случайной генерации или введи 's' для своей настройки: ")
    
    if choice.lower() == 's':
        # Своя настройка (можно добавить позже)
        print("Режим своей настройки пока не реализован. Генерируем случайно!")
        hares = generate_random_hares()
    else:
        hares = generate_random_hares()
    
    # Создаём окно
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"{len(hares)} случайных зайцев")
    screen.fill(BACKGROUND_COLOR)
    
    # Рисуем всех зайцев
    for hare in hares:
        x, y, width, height, hare_color, eye_color = hare
        draw_hare(screen, x, y, width, height, 
                 hare_color, eye_color, DEFAULT_NOSE_COLOR)
    
    # Добавляем номера зайцев
    font = pygame.font.Font(None, 20)
    for i, hare in enumerate(hares):
        x, y, width, height, _, _ = hare
        text = font.render(f"#{i+1}", True, (100, 100, 100))
        screen.blit(text, (x - 15, y - height//2 - 20))
    
    pygame.display.update()
    print(f"\n Нарисовано {len(hares)} случайных зайцев! Закрой окно, чтобы выйти.")
    
    # Основной цикл
    clock = pygame.time.Clock()
    FPS = 30
    running = True
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Нажатие пробела для новой генерации
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Очищаем экран и генерируем новых зайцев
                    screen.fill(BACKGROUND_COLOR)
                    hares = generate_random_hares()
                    for hare in hares:
                        x, y, width, height, hare_color, eye_color = hare
                        draw_hare(screen, x, y, width, height, 
                                 hare_color, eye_color, DEFAULT_NOSE_COLOR)
                    # Обновляем номера
                    for i, hare in enumerate(hares):
                        x, y, width, height, _, _ = hare
                        text = font.render(f"#{i+1}", True, (100, 100, 100))
                        screen.blit(text, (x - 15, y - height//2 - 20))
                    pygame.display.update()
                    print(f"\nСгенерировано {len(hares)} новых зайцев!")
    
    pygame.quit()


if __name__ == "__main__":
    main()