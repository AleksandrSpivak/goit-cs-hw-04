# this code works. lets add Queue into mulriprocess, as required in the tast. See main_3.py

import concurrent.futures
import timeit

from multiprocessing import Pool, Process, Manager
from os import listdir
from os.path import isfile, join
from typing import Callable


def check_my_list(filename):
    my_list = [
        "стаття",
        "agriculture",
        "surname",
        "legislation",
        "difference",
        "math",
        "list",
        "introduction",
        "annotation"
    ]
    dict = {}
    with open(filename, 'r') as f:
        text = f.read()
        for word in my_list:
            if word in text:
                dict[word] = filename
            else:
                dict[word] = None
    return dict

def benchmark(func: Callable, text_: str):
    setup_code = f"from __main__ import {func.__name__}"
    stmt = f"{func.__name__}(text)"
    return timeit.timeit(stmt=stmt, setup=setup_code, globals={'text': text_}, number=10)

def multi_threading(files_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        result_list = list(executor.map(check_my_list, files_list))
    return prepare_result_dict(result_list)

def multi_process(files_list):
    with Pool(processes=2) as pool:
        result_list = pool.map(check_my_list, files_list)
    return prepare_result_dict(result_list)

def multi_process_2(files_list):
    with Manager() as manager:
        shared_list = manager.list([manager.dict() for _ in range(len(files_list))])
        
        processes = []
        for i, f in enumerate(files_list):
            pr = Process(target=check_my_list_mpr, args=(f, shared_list[i]))
            pr.start()
            processes.append(pr)

        [pr.join() for pr in processes]

        reformated_list = [dict(d) for d in shared_list]
    return prepare_result_dict(reformated_list)

def simple_check(files_list):
    result_list = []
    for file in files_list:
        result_list.append(check_my_list(file))
    return prepare_result_dict(result_list)

def prepare_result_dict(result):
    collection_set = set()
    result_dict = {}
    for r in result:
        for key, value in r.items():
            if key not in collection_set:
                collection_set.add(key)
                result_dict[key] = []
            if value is not None:
                result_dict[key] = result_dict.get(key, []) + [value]
    return result_dict

def print_result_dict(result_dict):
    for key, value in result_dict.items():
            print(f"{key}: {value}")


def check_my_list_mpr(filename, val):
    my_list = [
        "стаття",
        "agriculture",
        "surname",
        "legislation",
        "difference",
        "math",
        "list",
        "introduction",
        "annotation"
    ]
    # dict = {}
    with open(filename, 'r') as f:
        text = f.read()
        for word in my_list:
            if word in text:
                val[word] = filename
            else:
                val[word] = None
    return


if __name__ == '__main__':

    files_list = [join(".\\texts", f) for f in listdir(".\\texts") if isfile(join(".\\texts", f))]

    title = f"{'Approach:':<35}| Time"
    print(title)
    print("-" * len(title))
    time = benchmark(simple_check, files_list)
    print(f"{'Standard approach:':<35}| {time:.3f}")
    results_sch = simple_check(files_list)

    time = benchmark(multi_threading, files_list)
    print(f"{'Multi-threading approach:':<35}| {time:.3f}")
    results_mth = multi_threading(files_list)

    time = benchmark(multi_process, files_list)
    print(f"{'Multi-process/Pool approach:':<35}| {time:.3f}")
    results_mpr = multi_process(files_list)

    time = benchmark(multi_process_2, files_list)
    print(f"{'Multi-process/Manager approach:':<35}| {time:.3f}")
    results_mpr2 = multi_process_2(files_list)

    print("\nResults of searches:")
    if results_sch == results_mth:
        print(f"Standard approach results == Multi-threading approach results")
    else:
        print(f"Standard approach results != Multi-threading approach results")

    if results_sch == results_mpr:
        print(f"Standard approach results == Multi-process/Pool approach results")
    else:
        print(f"Standard approach results != Multi-process/Pool approach results")

    if results_sch == results_mpr2:
        print(f"Standard approach results == Multi-process/Manager approach results")
    else:
        print(f"Standard approach results != Multi-process/Manager approach results")
