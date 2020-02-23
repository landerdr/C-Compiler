from antlr4 import *
from HelloLexer import HelloLexer
from HelloListener import HelloListener
from HelloParser import HelloParser
import sys


class HelloPrintListener(HelloListener):
    def enterAssignment(self, ctx):
        print(ctx.ID(), "is of type", ctx.Type())


def main():
    lexer = HelloLexer(StdinStream())
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.prog()
    printer = HelloPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    from antlr4.tree.Trees import Trees
    # import your parser & lexer here

    # setup your lexer, stream, parser and tree like normal

    print(Trees.toStringTree(tree, None, parser))


if __name__ == '__main__':
    main()
