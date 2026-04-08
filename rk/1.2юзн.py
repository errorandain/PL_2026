import random

def generate_unique_sorted_matrix(rows, cols, start=1, step_min=1, step_max=3):
    """
    Генерирует матрицу, где каждый следующий элемент больше предыдущего.
    Гарантирует уникальность всех чисел, а также возрастание строк, столбцов и диагонали.
    """
    matrix = [[0] * cols for _ in range(rows)]
    current = start
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = current
            # Увеличиваем на случайное число от step_min до step_max
            current += random.randint(step_min, step_max)
    return matrix

def search_in_sorted_matrix(matrix, K):
    """
    Поиск числа K в матрице, где строки и столбцы возрастают.
    Возвращает (найдено, количество_итераций)
    Алгоритм: начинаем с правого верхнего угла, сложность O(N+M).
    """
    if not matrix or not matrix[0]:
        return False, 0
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    row = 0
    col = cols - 1
    steps = 0
    
    while row < rows and col >= 0:
        steps += 1
        current = matrix[row][col]
        
        if current == K:
            return True, steps
        elif current > K:
            # Текущий элемент больше K → можно отбросить весь столбец
            col -= 1
        else:  # current < K
            # Текущий элемент меньше K → можно отбросить всю строку
            row += 1
    
    return False, steps

# Демонстрация
print("Вариант 1, Задание 1 — оптимальный поиск (O(N+M))")
N = int(input("Введите количество строк N: "))
M = int(input("Введите количество столбцов M: "))

matrix = generate_unique_sorted_matrix(N, M, start=random.randint(1, 10), step_min=1, step_max=3)

print("\nСгенерированная матрица (все числа уникальны, строки и столбцы возрастают):")
for row in matrix:
    print(row)

K = int(input("\nВведите число для поиска: "))

found, iterations = search_in_sorted_matrix(matrix, K)

print(f"\nРезультат поиска: {found}")
print(f"Количество итераций (сравнений): {iterations}")
if found:
    print("Число найдено.")
else:
    print("Число отсутствует в матрице.")