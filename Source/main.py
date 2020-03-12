import fileinput
import traceback

from Source.AntlrListener import *


def main():
    listener = CPrintListener()

    # input = fileinput.input()

    text = FileStream("Source/Test/simple_assignments.txt")
    print(text)
    try:
        listener.parse_string(text)
        _file = open('Source/Test/out.dot', 'w+')
        listener.tt.print_tree(_file)
    except ParserException as e:
        print("Parser error:", e)
    except Exception as e:
        print("Actual error: ", e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
