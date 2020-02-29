import fileinput

from Source.AntlrListener import *


def main():
    listener = CPrintListener()

    #input = fileinput.input()

    text = FileStream("Source/input1.txt")
    print(text)
    listener.parse_string(text)


if __name__ == '__main__':
    main()
