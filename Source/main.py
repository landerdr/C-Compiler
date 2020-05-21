import fileinput
import sys

from Source.AntlrListener import *
from Source.AST_Mips import AST

def main():
    file_input = None
    file_llvm = None
    file_mips = None
    file_dot = None
    listener = CPrintListener()

    n = len(sys.argv)
    for i in range(1, n):
        if sys.argv[i] == "-i":
            file_input = sys.argv[i + 1]
        if sys.argv[i] == '-dot':
            file_dot = sys.argv[i + 1]
        if sys.argv[i] == '-llvm':
            file_llvm = sys.argv[i + 1]
        if sys.argv[i] == '-mips':
            file_mips = sys.argv[i + 1]
        if sys.argv[i] == '-prop':
            listener.propagation = True

    if file_input == '':
        print("no input file specified")
        return

    text = FileStream(file_input)
    #print(text)
    try:
        listener.parse_string(text)
        if file_dot:
            _file_dot = open(file_dot, 'w+')
            listener.tt.print_tree(_file_dot)
        if file_llvm:
            listener.tt.print_llvm_ir(file_llvm)
        if file_mips:

            import Source.AST_Mips as AST_Source
            listener2 = CPrintListener(AST_Source)
            text = FileStream(file_input)
            listener2.parse_string(text)
            listener2.tt.print_mips(file_mips)

    except ParserException as e:
        print("Parser error:", e)


if __name__ == '__main__':
    main()
