import filecmp
import os


def run_command(input_file: str, output_file: str):
    print("__________no propagation__________")
    os.system("python3 Source/main.py -i %s -llvm main.ll" % input_file)
    os.system("clang main.ll -o main && %s < ./main" % output_file)


def run_command_prop(input_file: str, output_file: str):
    print("__________w/ propagation__________")
    os.system("python3 Source/main.py -i %s -llvm main.ll -prop" % input_file)
    os.system("clang main.ll -o main && %s < ./main" % output_file)


def compare(result_file: str, expected_result_file: str):
    return filecmp.cmp(result_file, expected_result_file)


def run_test(input_file: str, output_file: str, output_file_prop: str, expected_result_file: str):
    run_command(input_file, output_file)
    run_command_prop(input_file, output_file_prop)
    return compare(output_file, expected_result_file) and compare(output_file_prop, expected_result_file)


def run_tests():
    test_files = ["./Test/Deadline1.txt"]
    result_files = ["./Test/Deadline1_result.txt"]

    for i in range(len(test_files)):
        print("__________Starting test %s__________" % test_files[i])
        try:
            result = run_test(test_files[i], "test.txt", "test_prop.txt", result_files[i])
        except Exception:
            result = False
        if result:
            print("TEST PASSED")
        else:
            print("TEST FAILED")


if __name__ == "__main__":
    run_tests()
