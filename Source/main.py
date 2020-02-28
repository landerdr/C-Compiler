from Source.AntlrListener import *


def main():
    listener = CPrintListener()
    listener.parse_string(StdinStream())


if __name__ == '__main__':
    main()
