import filecmp
import os


def run_command(input_file: str, output_file: str, expected_result_file: str):
    """
    Runs test for LLVM without propagation enabled
    :param input_file: code input file to compile
    :param output_file: temp output file used to write results to
    :param expected_result_file: expected output to compare with generated output
    :return:
    """
    try:
        os.system("python3 Source/main.py -i %s -llvm main.ll" % input_file)
        os.system("clang main.ll -o main && ./main > %s" % output_file)
        result = compare(output_file, expected_result_file)
    except Exception:
        result = False
    return result


def run_command_prop(input_file: str, output_file: str, expected_result_file: str):
    """
    Runs test for LLVM with propagation enabled
    :param input_file: code input file to compile
    :param output_file: temp output file used to write results to
    :param expected_result_file: expected output to compare with generated output
    :return:
    """
    try:
        os.system("python3 Source/main.py -i %s -llvm main.ll -prop" % input_file)
        os.system("clang main.ll -o main && ./main > %s" % output_file)
        result = compare(output_file, expected_result_file)
    except Exception:
        result = False
    return result


def compare(result_file: str, expected_result_file: str):
    """
    Compares two files
    :param result_file:
    :param expected_result_file:
    :return: if the two files match
    """
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


def test_equality_operators():
    assert run_command("./Test/equality_operators.c", "test.txt", "./Test/equality_operators_result.txt") is True


def test_equality_operators_prop():
    assert run_command_prop("./Test/equality_operators.c", "test.txt", "./Test/equality_operators_result.txt") is True


def test_special_scope():
    assert run_command("./Test/special_scope.txt", "test.txt", "./Test/special_scope_result.txt") is True


def test_special_scope_prop():
    assert run_command_prop("./Test/special_scope.txt", "test.txt", "./Test/special_scope_result.txt") is True


def test_loops():
    assert run_command("./Test/loops.c", "test.txt", "./Test/loops_result.txt") is True


def test_loops_prop():
    assert run_command_prop("./Test/loops.c", "test.txt", "./Test/loops_result.txt") is True
