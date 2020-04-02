import filecmp
import os


def run_command(input_file: str, output_file: str, expected_result_file: str):
    # print("__________no propagation__________")
    try:
        os.system("python3 Source/main.py -i %s -llvm main.ll" % input_file)
        os.system("clang main.ll -o main && ./main > %s" % output_file)
        result = compare(output_file, expected_result_file)
    except Exception:
        result = False
    return result


def run_command_prop(input_file: str, output_file: str, expected_result_file: str):
    # print("__________w/ propagation__________")
    try:
        os.system("python3 Source/main.py -i %s -llvm main.ll -prop" % input_file)
        os.system("clang main.ll -o main && ./main > %s" % output_file)
        result = compare(output_file, expected_result_file)
    except Exception:
        result = False
    return result


def compare(result_file: str, expected_result_file: str):
    return filecmp.cmp(result_file, expected_result_file)


# def run_test(input_file: str, output_file: str, expected_result_file: str):
#     print("__________Starting test %s__________" % input_file)
#     run_command(input_file, output_file, expected_result_file)
#     run_command_prop(input_file, output_file, expected_result_file)


# def run_tests():
#     test_files = ["./Test/simple_expressions.txt", "./Test/Deadline1.txt"]
#     result_files = ["./Test/simple_expressions_result.txt", "./Test/Deadline1_result.txt"]
#
#     for i in range(len(test_files)):
#         run_test(test_files[i], "test.txt", result_files[i])

def test_simple_expressions():
    assert run_command("./Test/simple_expressions.txt", "test.txt", "./Test/simple_expressions_result.txt") is True


def test_simple_expressions_prop():
    assert run_command_prop("./Test/simple_expressions.txt", "test.txt", "./Test/simple_expressions_result.txt") is True


def test_deadline1():
    assert run_command("./Test/Deadline1.txt", "test.txt", "./Test/Deadline1_result.txt") is True


def test_deadline1_prop():
    assert run_command_prop("./Test/Deadline1.txt", "test.txt", "./Test/Deadline1_result.txt") is True
