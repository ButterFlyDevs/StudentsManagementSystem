# Run: In the same folder where is  folder.

# pytest test/test_sorters.py -v

import json, os
import utils as utils

cwd = os.getcwd()

def test_special_sort_1():

    pathA = os.path.join(cwd, "test/sorters_tests_files/original_list_1.json")
    pathB = os.path.join(cwd, "test/sorters_tests_files/expected_sorted_list_1.json")

    with open(pathA) as json_data_a:
        original = json.load(json_data_a)

    with open(pathB) as json_data_b:
        expected = json.load(json_data_b)

    assert utils.sorters.special_sort(original) == expected


def test_special_sort_2():
    # To run only: > pytest test.py::test_special_sort_2

    pathA = os.path.join(cwd, "test/sorters_tests_files/original_list_2.json")
    pathB = os.path.join(cwd, "test/sorters_tests_files/expected_sorted_list_2.json")

    with open(pathA) as json_data_a:
        original = json.load(json_data_a)

    with open(pathB) as json_data_b:
        expected = json.load(json_data_b)

    assert utils.sorters.special_sort_2(original) == expected


def test_special_sort_3():

    pathA = os.path.join(cwd, "test/sorters_tests_files/original_list_3.json")
    pathB = os.path.join(cwd, "test/sorters_tests_files/expected_sorted_list_3.json")

    with open(pathA) as json_data_a:
        original = json.load(json_data_a)

    with open(pathB) as json_data_b:
        expected = json.load(json_data_b)

    assert utils.sorters.special_sort_3(original) == expected

def test_special_sort_4():

    pathA = os.path.join(cwd, "test/sorters_tests_files/original_list_4.json")
    pathB = os.path.join(cwd, "test/sorters_tests_files/expected_sorted_list_4.json")

    with open(pathA) as json_data_a:
        original = json.load(json_data_a)

    with open(pathB) as json_data_b:
        expected = json.load(json_data_b)

    assert utils.sorters.special_sort_4(original) == expected
