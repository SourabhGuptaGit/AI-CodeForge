import sys

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file


WORKING_DIR = "calculator"

def test_get_files_info():
    
    test_case_file = [
        (WORKING_DIR, "."),
        (WORKING_DIR, "pkg"),
        (WORKING_DIR, "/bin"),
        (WORKING_DIR, "../"),
    ]
    
    for element, sub_element in test_case_file:
        result = get_files_info(element, sub_element)
        if sub_element == ".":
            sub_element = "Current"
        print(f"Result for {sub_element} directory:\n{result}")
    return

def test_get_file_content():
    test_case_file = [
        (WORKING_DIR, "main.py"),
        (WORKING_DIR, "pkg/calculator.py"),
        (WORKING_DIR, "/bin/cat"),
        (WORKING_DIR, "pkg/does_not_exist.py"),
    ]
    
    for element, sub_element in test_case_file:
        result = get_file_content(element, sub_element)
        if sub_element == ".":
            sub_element = "Current"
        print(result)
    return


def test_write_file():
    test_case = [
        (WORKING_DIR, "lorem.txt", "wait, this isn't lorem ipsum"),
        (WORKING_DIR, "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        (WORKING_DIR, "pkg/test/morelorem.txt", "lorem ipsum dolor sit amet"),
        (WORKING_DIR, "/tmp/temp.txt", "this should not be allowed"),
    ]
    for element, sub_element, content in test_case:
        result = write_file(element, sub_element, content)
        if sub_element == ".":
            sub_element = "Current"
        print(result)
    return

def test_run_python_file():
    test_case = [
        (WORKING_DIR, "main.py", []),
        (WORKING_DIR, "main.py", ["3 + 5"]),
        (WORKING_DIR, "test.py", []),
        (WORKING_DIR, "../main.py", []),
        (WORKING_DIR, "nonexistent.py", []),
        (WORKING_DIR, "lorem.txt", []),
    ]
    for element, sub_element, content in test_case:
        result = run_python_file(element, sub_element, content)
        if sub_element == ".":
            sub_element = "Current"
        print(result)
    return
    

if __name__ == "__main__":
    test_get_files_info()