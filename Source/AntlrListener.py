from antlr4 import *

from Source.AST import *
from Source.CLexer import CLexer
from Source.CListener import CListener
from Source.CParser import CParser


class CPrintListener(CListener):

    def __init__(self):
        super(CPrintListener, self).__init__()
        self.depthStack = []
        self.tt = AST()

    '''Core'''

    def parse_string(self, _str):
        self.tt = AST()
        self.depthStack = []

        lexer = CLexer(_str)
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        tree = parser.library()

        walker = ParseTreeWalker()
        walker.walk(self, tree)

        # from antlr4.tree.Trees import Trees
        # print(Trees.toStringTree(tree, None, parser))
        self.tt.simplify()
        _file = open('Source/out.txt', 'w+')
        self.tt.print_tree(_file)

    '''Rules'''

    def exitEveryRule(self, ctx: ParserRuleContext):
        self.depthStack.pop()

    def enterEveryRule(self, ctx: ParserRuleContext):
        pass

    def enterLibrary(self, ctx: CParser.LibraryContext):
        expr = ASTNodeLib()
        self.tt.root = expr
        self.depthStack.append(expr)

    def enterAdditional_expression(self, ctx: CParser.Additional_expressionContext):
        expr = ASTNodeAddition()
        self.add_node(expr)

    def enterBracket_expression(self, ctx: CParser.Bracket_expressionContext):
        self.skip_node()

    def enterBreak_statement(self, ctx: CParser.Break_statementContext):
        expr = ASTNodeBreak()
        self.add_node(expr)

    def enterCompound_statement(self, ctx: CParser.Compound_statementContext):
        expr = ASTNodeCompound()
        self.add_node(expr)

    def enterLiteral_expression(self, ctx: CParser.Literal_expressionContext):
        expr = None
        if ctx.ID():
            expr = ASTNodeLiteral(ctx.ID())
        else:
            expr = ASTNodeLiteral(ctx.Int())
        self.add_node(expr)

    def enterExpression_statement(self, ctx: CParser.Expression_statementContext):
        expr = ASTNodeExpressionStatement()
        self.add_node(expr)

    def enterExpression(self, ctx: CParser.ExpressionContext):
        expr = ASTNodeExpression()
        self.add_node(expr)

    def enterTernary_expression(self, ctx: CParser.Ternary_expressionContext):
        expr = ASTNodeTernaryExpr()
        self.add_node(expr)

    def enterConditional_expression(self, ctx: CParser.Conditional_expressionContext):
        expr = ASTNodeConditional()
        self.add_node(expr)

    def enterMultiplicational_expression(self, ctx: CParser.Multiplicational_expressionContext):
        expr = ASTNodeMult()
        self.add_node(expr)

    def enterUnary_expression(self, ctx: CParser.Unary_expressionContext):
        expr = ASTNodeUnaryExpr()
        self.add_node(expr)

    def enterVariable_definition(self, ctx: CParser.Variable_definitionContext):
        expr = ASTNodeDefinition()
        expr.type = ctx.ID()
        expr.name = ctx.Type()
        self.add_node(expr)

    def enterConditional_statement(self, ctx: CParser.Conditional_statementContext):
        expr = ASTNodeIf()
        self.add_node(expr)

    def enterContinue_statement(self, ctx: CParser.Continue_statementContext):
        expr = ASTNodeContinue()
        self.add_node(expr)

    def enterDecrement(self, ctx: CParser.DecrementContext):
        expr = ASTNodeDecrement()
        self.add_node(expr)

    def enterEquality_expression(self, ctx: CParser.Equality_expressionContext):
        expr = ASTNodeEqualityExpr()
        expr.id = ctx.ID()
        expr.equality = ctx.equality_symbol().getText()
        self.add_node(expr)

    def enterEquality_symbol(self, ctx: CParser.Equality_symbolContext):
        self.skip_node()

    def enterFunction(self, ctx: CParser.FunctionContext):
        expr = ASTNodeFunction()
        self.add_node(expr)

    def enterFunction_call_expression(self, ctx: CParser.Function_call_expressionContext):
        expr = ASTNodeFunctionCallExpr()
        self.add_node(expr)

    def enterIncrement(self, ctx: CParser.IncrementContext):
        expr = ASTNodeIncrement()
        self.add_node(expr)

    def enterIndexing_expression(self, ctx: CParser.Indexing_expressionContext):
        expr = ASTNodeIndexingExpr()
        self.add_node(expr)

    def enterInverse(self, ctx: CParser.InverseContext):
        expr = ASTNodeInverseExpr()
        self.add_node(expr)

    def enterLoop_statement(self, ctx: CParser.Loop_statementContext):
        expr = ASTNodeLoopStatement()
        self.add_node(expr)

    def enterNegative(self, ctx: CParser.NegativeContext):
        expr = ASTNodeNegativeExpr()
        self.add_node(expr)

    def enterParam(self, ctx: CParser.ParamContext):
        expr = ASTNodeParam()
        self.add_node(expr)

    def enterParams(self, ctx: CParser.ParamsContext):
        expr = ASTNodeParams()
        self.add_node(expr)

    def enterPositive(self, ctx: CParser.PositiveContext):
        expr = ASTNodePositiveExpr()
        self.add_node(expr)

    def enterReturn_statement(self, ctx: CParser.Return_statementContext):
        expr = ASTNodeReturn()
        self.add_node(expr)

    def enterStatement(self, ctx: CParser.StatementContext):
        expr = ASTNodeStatement()
        self.add_node(expr)

    def visitErrorNode(self, node: ErrorNode):
        print("Error")

    '''helper functions'''

    def add_node(self, node):
        self.depthStack[-1].add_child(node)
        self.depthStack.append(node)

    def skip_node(self):
        self.depthStack.append(self.depthStack[-1])
