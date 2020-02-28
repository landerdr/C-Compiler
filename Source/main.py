from antlr4 import *
from Source.HelloLexer import HelloLexer
from Source.HelloListener import HelloListener
from Source.HelloParser import HelloParser
import sys

from Source.AST import *

tt = AST()
depthStack = []
item = None


def add_node(node):
    depthStack[-1].add_child(node)
    depthStack.append(node)


class HelloPrintListener(HelloListener):
    def enterAssignment(self, ctx):
        expr = ASTNodeAssignment()
        add_node(expr)
        pass

    def enterVal(self, ctx:HelloParser.ValContext):
        expr = ASTNodeValue(ctx.Int())
        add_node(expr)

    def enterExpr(self, ctx:HelloParser.ExprContext):
        expr = ASTNodeExpression()
        add_node(expr)

    def enterAdd_expr(self, ctx:HelloParser.Add_exprContext):
        expr = ASTNodeAddition()
        add_node(expr)

    def enterAtom(self, ctx:HelloParser.AtomContext):
        expr = ASTNodeValue(ctx.val())
        add_node(expr)

    def enterMult_expr(self, ctx:HelloParser.Mult_exprContext):

        expr = ASTNodeMult()
        add_node(expr)

    def enterProg(self, ctx:HelloParser.ProgContext):
        expr = ASTNodeProg()
        tt.root = expr
        depthStack.append(expr)

    def exitEveryRule(self, ctx:ParserRuleContext):
        depthStack.pop()


def main():
    lexer = HelloLexer(StdinStream())
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.prog()

    printer = HelloPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    tt.print_tree()

    from antlr4.tree.Trees import Trees
    # import your parser & lexer here

    # setup your lexer, stream, parser and tree like normal

    #print(Trees.toStringTree(tree, None, parser))


if __name__ == '__main__':
    main()
