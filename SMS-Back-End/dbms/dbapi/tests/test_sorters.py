# Run: pytest in the same folder where is tests/ folder.
import json, imp
utils = imp.load_source("utils", "utils.py")


def test_special_sort_1():
    with open('tests/sorters_tests_files/original_list_1.json') as json_data_a:
        original = json.load(json_data_a)

    with open('tests/sorters_tests_files/expected_sorted_list_1.json') as json_data_b:
        expected = json.load(json_data_b)

    assert utils.sorters.special_sort(original) == expected


def test_special_sort_2():
    # To run only: > pytest test.py::test_special_sort_2

    with open('tests/sorters_tests_files/original_list_2.json') as json_data_a:
        original = json.load(json_data_a)

    with open('tests/sorters_tests_files/expected_sorted_list_2.json') as json_data_b:
        expected = json.load(json_data_b)

    assert utils.sorters.special_sort_2(original) == expected


def test_special_sort_3():

    with open('tests/sorters_tests_files/original_list_3.json') as json_data_a:
        data_block_a = json.load(json_data_a)

    with open('tests/sorters_tests_files/expected_sorted_list_3.json') as json_data_b:
        data_block_b = json.load(json_data_b)

    assert utils.sorters.special_sort_3(data_block_a) == data_block_b

def test_special_sort_4():

    with open('tests/sorters_tests_files/original_list_4.json') as json_data_a:
        data_block_a = json.load(json_data_a)

    with open('tests/sorters_tests_files/expected_sorted_list_4.json') as json_data_b:
        data_block_b = json.load(json_data_b)

    assert utils.sorters.special_sort_4(data_block_a) == data_block_b
