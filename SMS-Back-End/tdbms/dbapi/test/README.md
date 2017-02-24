### Ways to execute tests in **dbapi**:


-   Inside of **dbapi** package folder. 
    Only executing `pytest` (it will search all test files).
-   Inside of **dbapi** package folder, especify the name of test file inside of tests folder:
        `pytest tests/test_sorters.py::test_special_sort_1`
       
       
-    `pytest --cov-report term-missing --cov=.  test/`  
       
-    `pytest --pep8`
       
       
Is not allowed executed test inside of tests folders because the way to import files.