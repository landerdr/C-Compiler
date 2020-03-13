import fileinput
import sys
import traceback

from Source.AntlrListener import *


def main():
    listener = CPrintListener()

    file_input = None
    file_llvm = None
    file_dot = None
    propagation = False

    n = len(sys.argv)
    for i in range(1, n):
        if sys.argv[i] == "-i":
            file_input = sys.argv[i + 1]
        if sys.argv[i] == '-dot':
            file_dot = sys.argv[i + 1]
        if sys.argv[i] == '-llvm':
            file_llvm = sys.argv[i + 1]
        if sys.argv[i] == '--prop':
            propagation = True

    if file_input == '':
        print("no input file specified")
        return

    text = FileStream(file_input)
    print(text)
    try:
        listener.parse_string(text)
        if file_dot:
            _file_dot = open(file_dot, 'w+')
            listener.tt.print_tree(_file_dot)
        if file_llvm:
            _file_llvm = open(file_llvm, 'w+')
            listener.tt.print_llvm_ir(_file_llvm)

    except ParserException as e:
        print("Parser error:", e)
    except Exception as e:
        print("Actual error: ", e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
