import random
from collections import deque

def min_minutes_to_rot(matrix):
    """
    Возвращает минимальное количество минут, за которое все яблоки станут плохими.
    Если это невозможно, возвращает -1.
    Дополнительно возвращает количество итераций BFS (обработанных клеток).
    """
    if not matrix or not matrix[0]:
        return -1, 0
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Очередь для BFS: храним (строка, столбец, минута)
    q = deque()
    fresh_count = 0
    iterations = 0  # счётчик итераций (сколько клеток обработали)
    
    # Находим все плохие яблоки и считаем хорошие
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 2:
                q.append((i, j, 0))
            elif matrix[i][j] == 1:
                fresh_count += 1
    
    # Если нет хороших яблок, всё уже плохое
    if fresh_count == 0:
        return 0, 0
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    minutes = 0
    
    while q:
        x, y, t = q.popleft()
        iterations += 1
        minutes = max(minutes, t)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] == 1:
                matrix[nx][ny] = 2  # заражаем
                fresh_count -= 1
                q.append((nx, ny, t + 1))
    
    if fresh_count == 0:
        return minutes, iterations
    else:
        return -1, iterations


# ------------------- ДОПОЛНИТЕЛЬНЫЕ БАЛЛЫ -------------------
# Генерируем случайные матрицы до тех пор, пока не получим положительный результат
# (т.е. все яблоки смогут стать плохими)

def random_apple_matrix(rows, cols):
    """Создаёт матрицу rows x cols со случайными значениями 0, 1, 2"""
    return [[random.randint(0, 2) for _ in range(cols)] for _ in range(rows)]

print("Вариант 1, Задание 2 — заражение яблок")
print("Программа будет генерировать случайные матрицы до тех пор, пока не найдёт успешный случай.")
print("(Все яблоки смогут стать плохими)\n")

attempts = 0
success = False

while not success:
    # Случайные размеры от 3 до 8
    N = random.randint(3, 8)
    M = random.randint(3, 8)
    
    # Генерируем матрицу
    garden = random_apple_matrix(N, M)
    
    print(f"Попытка {attempts + 1}: матрица {N}x{M}")
    # Не выводим всю матрицу, чтобы не захламлять экран (можно раскомментировать для отладки)
    # for row in garden:
    #     print(row)
    
    # Копируем, чтобы не портить оригинал при повторных попытках (хотя мы каждый раз создаём новую)
    import copy
    garden_copy = copy.deepcopy(garden)
    
    minutes, iters = min_minutes_to_rot(garden_copy)
    attempts += 1
    
    if minutes != -1:
        print(f"   УСПЕХ! Попытка #{attempts}")
        print(f"   Минут потребовалось: {minutes}")
        print(f"   Итераций BFS: {iters}")
        print(f"   Количество неудачных попыток до успеха: {attempts - 1}")
        
        # Показываем исходную матрицу (первую, без изменений) и результат
        print("\nИсходная матрица (0-пусто, 1-хорошее, 2-плохое):")
        for row in garden:
            print(row)
        print("\nМатрица после заражения (все 2 и 0):")
        for row in garden_copy:
            print(row)
        success = True
    else:
        print(f"  Неудача (невозможно заразить все яблоки). Пробуем снова...\n")