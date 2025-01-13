import csv
from timeit import timeit
from BTrees.OOBTree import OOBTree

def load_data(file_path):
    """Завантаження даних з CSV-файлу."""
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['ID'] = int(row['ID'])
            row['Price'] = float(row['Price'])
            data.append(row)
    return data

def add_item_to_tree(tree, item):
    """Додавання товару в OOBTree."""
    tree[item['ID']] = {
        'Name': item['Name'],
        'Category': item['Category'],
        'Price': item['Price']
    }

def add_item_to_dict(dictionary, item):
    """Додавання товару в словник."""
    dictionary[item['ID']] = {
        'Name': item['Name'],
        'Category': item['Category'],
        'Price': item['Price']
    }

def range_query_tree(tree, min_price, max_price):
    """Діапазонний запит для OOBTree."""
    return list(tree.items(min_price, max_price))

def range_query_dict(dictionary, min_price, max_price):
    """Діапазонний запит для словника."""
    return [item for item in dictionary.values() if min_price <= item['Price'] <= max_price]

def benchmark_range_query(structure, query_function, min_price, max_price, iterations):
    """Вимірювання часу виконання діапазонного запиту."""
    return timeit(lambda: query_function(structure, min_price, max_price), number=iterations)

if __name__ == "__main__":
    # Шлях до файлу з даними
    file_path = "generated_items_data.csv"

    # Завантаження даних
    data = load_data(file_path)

    # Ініціалізація структур
    tree = OOBTree()
    dictionary = {}

    # Додавання даних до структур
    for item in data:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Визначення діапазону цін для тестування
    min_price = 10.0
    max_price = 50.0

    # Кількість ітерацій для тестування
    iterations = 100

    # Вимірювання продуктивності
    tree_time = benchmark_range_query(tree, range_query_tree, min_price, max_price, iterations)
    dict_time = benchmark_range_query(dictionary, range_query_dict, min_price, max_price, iterations)

    # Вивід результатів
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")
