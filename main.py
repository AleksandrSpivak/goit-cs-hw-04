import concurrent.futures
import timeit

from multiprocessing import Pool, Process, Manager, Queue
from os import listdir
from os.path import isfile, join
from typing import Callable

# list of words to be find in the files
MY_LIST = [
        "compose",
        "agriculture",
        "surname",
        "legislation",
        "difference",
        "math",
        "list",
        "introduction",
        "annotation"
    ]

def check_my_list(filename):
    """
	check_my_list is a function that takes a filename as a parameter, checks all words from MY_LIST 
    whether they are in the file andreturns a dictionary with the word as key and the filename if present, otherwise None.
	"""

    dict = {}
    with open(filename, 'r') as f:
        text = f.read()
        for word in MY_LIST:
            if word in text:
                dict[word] = filename
            else:
                dict[word] = None
    return dict

def check_my_list_mpr(q, val):
    """
    This function has the same functionality as check_my_list, but 
    it has a different structure because of multiprocessing+Manager+Queue approach.
    Parameters:
    - q: a queue object that keeps file names
    - val: a dictionary to store the word-file associations
    Return type: None
    """

    filename = q.get()
    with open(filename, 'r') as f:
        text = f.read()
        for word in MY_LIST:
            if word in text:
                val[word] = filename
            else:
                val[word] = None
    return

def simple_check(files_list):
    """
    Function to perform a simple check on a list of files.
    
    Args:
    - files_list (list): A list of file names to be checked.
    
    Returns:
    - dict: A dictionary containing the results of the checks for each file.
    """
    result_list = []
    for file in files_list:
        result_list.append(check_my_list(file))
    return prepare_result_dict(result_list)


def multi_threading(files_list):
    """
    Perform multi-threading to process the files_list and return a result dictionary.

    Args:
    - files_list: A list of file paths to be processed.

    Returns:
    - A dictionary containing the results of processing the files.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        result_list = list(executor.map(check_my_list, files_list))
    return prepare_result_dict(result_list)

def multi_process_pool(files_list):
    """
    Perform multiprocessing using Pool class to process the files_list and return a result dictionary.

    Args:
    - files_list: A list of file paths to be processed.

    Returns:
    - A dictionary containing the results of processing the files.
    """
    with Pool(processes=2) as pool:
        result_list = pool.map(check_my_list, files_list)
    return prepare_result_dict(result_list)

def multi_process_manager_queue(files_list):
    """
    Perform multiprocessing using Manager & Queue classes to process the files_list and return a result dictionary.

    Args:
    - files_list: A list of file paths to be processed.

    Returns:
    - A dictionary containing the results of processing the files.
    """    
    with Manager() as manager:
        q = Queue()  
        processes = []
        shared_list = manager.list([manager.dict() for _ in range(len(files_list))])

        for i in range(len(files_list)):
            pr = Process(target=check_my_list_mpr, args=(q, shared_list[i]))
            pr.start()
            processes.append(pr)
        
        for f in files_list:
            q.put(f)    

        [pr.join() for pr in processes]

        reformated_list = [dict(d) for d in shared_list]
    return prepare_result_dict(reformated_list)

def benchmark(func: Callable, text_: str):
    """
    Function to benchmark the execution time of a given function with a specific input string.
    Parameters:
    - func: A callable function to be benchmarked.
    - text_: A string input for the benchmarked function.
    Returns:
    - The average execution time of the function over 10 runs.
    """
    setup_code = f"from __main__ import {func.__name__}"
    stmt = f"{func.__name__}(text)"
    return timeit.timeit(stmt=stmt, setup=setup_code, globals={'text': text_}, number=10)

def prepare_result_dict(result):
    """
    Formats output as requested in the task.  Create a dictionary from the list of dictionaries 'result', 
    where each key in the dictionaries becomes a key in the result_dict and the values associated with each key are collected in a list. 

    Parameters:
    - input: list of dictionaries.

    Returns:
    dict: The resulting dictionary with the words from MY_LIST as the keys and respective files as values.
    """
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
    """
    If you need to print the result dictionary, use this function.
    """
    for key, value in result_dict.items():
            print(f"{key}: {value}")


if __name__ == '__main__':
    # collects list of files from "texts" folder. 
    files_list = [join(".\\texts", f) for f in listdir(".\\texts") if isfile(join(".\\texts", f))]

    # prints table with the result of calculation
    title = f"{'Approach:':<40}| Time"
    print(title)
    print("-" * len(title))
    time = benchmark(simple_check, files_list)
    print(f"{'Standard approach:':<40}| {time:.3f}")

    time = benchmark(multi_threading, files_list)
    print(f"{'Multi-threading approach:':<40}| {time:.3f}")

    time = benchmark(multi_process_pool, files_list)
    print(f"{'Multi-process/Pool approach:':<40}| {time:.3f}")

    time = benchmark(multi_process_manager_queue, files_list)
    print(f"{'Multi-process/Manager+Queue approach:':<40}| {time:.3f}")

    # compares and prints results of searches
    print("\nResults of searches:")
    results_sch = simple_check(files_list)
    results_mth = multi_threading(files_list)
    results_mpr_pool = multi_process_pool(files_list)
    results_mpr_manager_queue = multi_process_manager_queue(files_list)

    if results_sch == results_mth:
        print(f"Standard approach results == Multi-threading approach results")
    else:
        print(f"Standard approach results != Multi-threading approach results")

    if results_sch == results_mpr_pool:
        print(f"Standard approach results == Multi-process/Pool approach results")
    else:
        print(f"Standard approach results != Multi-process/Pool approach results")

    if results_sch == results_mpr_manager_queue:
        print(f"Standard approach results == Multi-process/Manager+Queue approach results")
    else:
        print(f"Standard approach results != Multi-process/Manager+Queue approach results")
    print_result_dict(results_sch)