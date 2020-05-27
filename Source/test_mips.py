import filecmp
import os


def run_command(input_file: str, output_file: str = "test.txt", expected_result_file: str = "test_expected.txt"):
    """
    Runs test for LLVM without propagation enabled
    :param input_file: code input file to compile
    :param output_file: temp output file used to write results to
    :param expected_result_file: expected output to compare with generated output
    :return:
    """
    try:
        os.system("clang -ansi -pedantic %s -o main && ./main > %s" % (input_file, expected_result_file))
        os.system("rm main")
        os.system("python3 Source/main.py -i %s -mips main.asm" % input_file)
        os.system("java -jar mars.jar me nc main.asm > %s" % output_file)
        os.system("rm main.asm")
        result = compare(output_file, expected_result_file)
    except Exception:
        result = False
    return result


def run_command_prop(input_file: str, output_file: str = "test.txt", expected_result_file: str = "test_expected.txt"):
    """
    Runs test for LLVM with propagation enabled
    :param input_file: code input file to compile
    :param output_file: temp output file used to write results to
    :param expected_result_file: expected output to compare with generated output
    :return:
    """
    try:
        os.system("clang -ansi -pedantic %s -o main && ./main > %s" % (input_file, expected_result_file))
        os.system("rm main")
        os.system("python3 Source/main.py -i %s -mips main.asm -prop" % input_file)
        os.system("java -jar mars.jar me nc main.asm > %s" % output_file)
        os.system("rm main.asm")
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

# def test_simple_expressions():
#     assert run_command("./Test/simple_expressions.txt", "test.txt", "test_expected.txt") is True
#
#
# def test_simple_expressions_prop():
#     assert run_command_prop("./Test/simple_expressions.txt", "test.txt", "test_expected.txt") is True
#
#
# def test_deadline1():
#     assert run_command("./Test/Deadline1.txt", "test.txt", "test_expected.txt") is True
#
#
# def test_deadline1_prop():
#     assert run_command_prop("./Test/Deadline1.txt", "test.txt", "test_expected.txt") is True
#
#
# def test_equality_operators():
#     assert run_command("./Test/equality_operators.c", "test.txt", "test_expected.txt") is True
#
#
# def test_equality_operators_prop():
#     assert run_command_prop("./Test/equality_operators.c", "test.txt", "test_expected.txt") is True
#
#
# def test_special_scope():
#     assert run_command("./Test/special_scope.txt", "test.txt", "test_expected.txt")is True
#
#
# def test_special_scope_prop():
#     assert run_command_prop("./Test/special_scope.txt", "test.txt", "test_expected.txt") is True
#
#
# def test_loops():
#     assert run_command("./Test/loops.c", "test.txt", "test_expected.txt") is True
#
#
# def test_loops_prop():
#     assert run_command_prop("./Test/loops.c", "test.txt", "test_expected.txt") is True


def test_binary_operations1():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/binaryOperations1.c") is True


def test_binary_operations1_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/binaryOperations1.c") is True


def test_binary_operations2():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/binaryOperations2.c") is True


def test_binary_operations2_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/binaryOperations2.c") is True


def test_break_continue():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/breakAndContinue.c") is True


def test_break_continue_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/breakAndContinue.c") is True


def test_comparisons1():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/comparisons1.c") is True


def test_comparisons1_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/comparisons1.c") is True


def test_comparisons2():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/comparisons2.c") is True


def test_comparisons2_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/comparisons2.c") is True


def test_dereference_assignment():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/dereferenceAssignment.c") is True


def test_dereference_assignment_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/dereferenceAssignment.c") is True


def test_fibonacci_recursive():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/fibonacciRecursive.c") is True


def test_fibonacci_recursive_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/fibonacciRecursive.c") is True


def test_float_int_conversion():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/floatToIntConversion.c") is True


def test_float_int_conversion_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/floatToIntConversion.c") is True


def test_for():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/for.c") is True


def test_for_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/for.c") is True


def test_forward_declaration():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/forwardDeclaration.c") is True


def test_forward_declaration_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/forwardDeclaration.c") is True


def test_if():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/if.c") is True


def test_if_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/if.c") is True


def test_if_else():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/ifElse.c") is True


def test_if_else_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/ifElse.c") is True


def test_int_float_conversion():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/intToFloatConversion.c") is True


def test_int_float_conversion_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/intToFloatConversion.c") is True


def test_modulo():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/modulo.c") is True


def test_modulo_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/modulo.c") is True


def test_pointer_argument():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/pointerArgument.c") is True


def test_pointer_argument_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/pointerArgument.c") is True


# def test_prime():
#     assert run_command("./Test/CompilersBenchmark/CorrectCode/prime.c") is True
#
#
# def test_prime_prop():
#     assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/prime.c") is True


def test_printf1():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/printf1.c") is True


def test_printf1_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/printf1.c") is True


def test_printf2():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/printf2.c") is True


def test_printf2_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/printf2.c") is True


def test_printf3():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/printf3.c") is True


def test_printf3_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/printf3.c") is True


def test_scoping():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/scoping.c") is True


def test_scoping_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/scoping.c") is True


def test_unary_operations():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/unaryOperations.c") is True


def test_unary_operations_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/unaryOperations.c") is True


def test_variables1():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/variables1.c") is True


def test_variables1_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/variables1.c") is True


def test_variables2():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/variables2.c") is True


def test_variables2_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/variables2.c") is True


def test_variables3():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/variables3.c") is True


def test_variables3_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/variables3.c") is True


def test_variables4():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/variables4.c") is True


def test_variables4_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/variables4.c") is True


def test_variables5():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/variables5.c") is True


def test_variables5_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/variables5.c") is True


def test_variables6():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/variables6.c") is True


def test_variables6_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/variables6.c") is True


def test_variables7():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/variables7.c") is True


def test_variables7_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/variables7.c") is True


def test_variables8():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/variables8.c") is True


def test_variables8_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/variables8.c") is True


def test_while():
    assert run_command("./Test/CompilersBenchmark/CorrectCode/while.c") is True


def test_while_prop():
    assert run_command_prop("./Test/CompilersBenchmark/CorrectCode/while.c") is True
