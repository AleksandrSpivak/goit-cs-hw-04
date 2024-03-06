import timeit
from  typing import Callable


def build_shift_table(pattern):
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0  

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  

        if j < 0:
            return i 

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1

def read_file(filename):
    with open(filename, 'r', encoding='CP1125') as f:
        return f.read()
    
def benchmark(func: Callable, text_: str, pattern_: str):
    setup_code = f"from __main__ import {func.__name__}"
    stmt = f"{func.__name__}(text, pattern)"
    return timeit.timeit(stmt=stmt, setup=setup_code, globals={'text': text_, 'pattern': pattern_}, number=10)


if __name__ == "__main__":
    data = { # file name: [existing pattern, non-existing pattern]
        "стаття3.txt": ["вступ", "анотація"],
        "стаття2.txt": ["значна відмінність у часі", "Hello, world!"],
    }

    for file in data:
        print(f"\nДля файлу {file}")
        text = read_file(file)
        results = []
        for pattern in data[file]:
            time = benchmark(boyer_moore_search, text, pattern)
            results.append((boyer_moore_search.__name__, pattern, time))
        title = f"{'Алгоритм':<30} | {'Підрядок':<30} | {'Час виконання, сек'}"
        print(title)
        print("-" * len(title))
        for result in results:
            print(f"{result[0]:<30} | {result[1]:<30} | {result[2]:<15.5f}")
