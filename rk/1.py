import random

def generate_unique_sorted_matrix(rows, cols, start=1, step_min=1, step_max=3):
    """Генерирует матрицу с уникальными возрастающими числами"""
    matrix = [[0] * cols for _ in range(rows)]
    current = start
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = current
            current += random.randint(step_min, step_max)
    return matrix

def super_fast_search(matrix, K):
    """
    СУПЕР-БЫСТРЫЙ ПОИСК
    Сначала бинарным поиском находим примерную строку, затем идём по ней
    """
    if not matrix or not matrix[0]:
        return False, 0
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    min_val = matrix[0][0]
    max_val = matrix[rows-1][cols-1]

    if K < min_val or K > max_val:
        return False, 0
    
    steps = 0
    
    # БИНАРНЫЙ ПОИСК по первому столбцу (находим строку, где K может быть)
    top, bottom = 0, rows - 1
    target_row = 0
    
    while top <= bottom:
        steps += 1
        mid = (top + bottom) // 2
        if matrix[mid][0] == K:
            return True, steps
        elif matrix[mid][0] < K:
            target_row = mid
            top = mid + 1
        else:
            bottom = mid - 1
    
    # Теперь ищем в найденной строке (бинарный поиск по строке)
    left, right = 0, cols - 1
    while left <= right:
        steps += 1
        mid = (left + right) // 2
        if matrix[target_row][mid] == K:
            return True, steps
        elif matrix[target_row][mid] < K:
            left = mid + 1
        else:
            right = mid - 1
    
    # Если не нашли, пробуем соседние строки (на всякий случай)
    for row in range(max(0, target_row - 1), min(rows, target_row + 2)):
        left, right = 0, cols - 1
        while left <= right:
            steps += 1
            mid = (left + right) // 2
            if matrix[row][mid] == K:
                return True, steps
            elif matrix[row][mid] < K:
                left = mid + 1
            else:
                right = mid - 1
    
    return False, steps


# ============ ТЕСТИРОВАНИЕ ============

# Создаём матрицу
N = int(input("Введите количество строк N: "))
M = int(input("Введите количество столбцов M: "))

matrix = generate_unique_sorted_matrix(N, M, start=random.randint(1, 10), step_min=1, step_max=3)

print("\nСгенерированная матрица:")
for row in matrix:
    print(row)

print(f"\nМинимум: {matrix[0][0]}, Максимум: {matrix[N-1][M-1]}")


K = int(input("\nВведите число для поиска: "))

# Замеряем время выполнения (для больших матриц)
found, steps = super_fast_search(matrix, K)

print(f"\nРезультат: {found}")
print(f"Итераций: {steps}")

if found:
    print(" Число найдено!")
else:
    print(" Число не найдено")