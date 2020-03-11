from antlr4 import *
from gen.CLexer import CLexer
from gen.CListener import CListener
from gen.CParser import CParser

from Source.AST import *
from Source.TypeTable import TypeTable


class CPrintListener(CListener):

    def __init__(self):
        super(CPrintListener, self).__init__()
        self.typeTable = TypeTable()
        self.typeTable.enter_scope()
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
        # self.tt.simplify()
        _file = open('Source/Test/out.txt', 'w+')
        self.tt.print_tree(_file)
        print(self.typeTable)

    '''Rules'''

    def exitEveryRule(self, ctx: ParserRuleContext):
        if self.depthStack:
            try:
                # Get current node
                item = self.depthStack.pop()
                if item not in self.depthStack:
                    item.simplify()

            except Exception as e:
                print("failed on", item, e.__str__())
        else:
            print("!!Tried popping")

    def enterEveryRule(self, ctx: ParserRuleContext):
        pass

    def enterLibrary(self, ctx: CParser.LibraryContext):
        expr = ASTNodeLib()
        self.tt.root = expr
        self.depthStack.append(expr)

    def enterAdditional_expression(self, ctx: CParser.Additional_expressionContext):
        expr = ASTNodeAddition()
        expr.operators = []
        self.add_node(expr)

    def enterBracket_expression(self, ctx: CParser.Bracket_expressionContext):
        self.skip_node()

    def enterBreak_statement(self, ctx: CParser.Break_statementContext):
        expr = ASTNodeBreak()
        self.add_node(expr)

    def enterCompound_statement(self, ctx: CParser.Compound_statementContext):
        expr = ASTNodeCompound()
        self.typeTable.enter_scope()
        self.add_node(expr)

    def exitCompound_statement(self, ctx: CParser.Compound_statementContext):
        self.typeTable.leave_scope()
        pass

    def enterLiteral_expression(self, ctx: CParser.Literal_expressionContext):
        # Get txt
        txt = (ctx.ID() or ctx.Int() or ctx.Float() or ctx.Char())

        expr = ASTNodeLiteral(txt)
        if ctx.Int():
            expr.isConst = True
            expr.value = int(txt.getText())
        if ctx.Char():
            expr.isConst = True
            expr.value = ord(txt.getText()[1])
        if ctx.Float():
            expr.isConst = True
            expr.value = float(txt.getText())
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

    # ToDo: fix bitwise expressions
    def enterBitwise_and_expression(self, ctx: CParser.Bitwise_and_expressionContext):
        self.skip_node()

    def enterBitwise_or_expression(self, ctx: CParser.Bitwise_or_expressionContext):
        self.skip_node()

    def enterBitwise_xor_expression(self, ctx: CParser.Bitwise_xor_expressionContext):
        self.skip_node()

    # ToDo: fix logical expressions
    def enterLogical_and_expression(self, ctx: CParser.Logical_and_expressionContext):
        expr = ASTNodeStatement()
        self.add_node(expr)

    def enterLogical_or_expression(self, ctx: CParser.Logical_or_expressionContext):
        expr = ASTNodeStatement()
        self.add_node(expr)

    # ToDo: fix relational expressions
    def enterRelational_comparison_expression(self, ctx: CParser.Relational_comparison_expressionContext):
        expr = ASTNodeConditional()
        self.add_node(expr)

    def enterRelational_equality_expression(self, ctx: CParser.Relational_equality_expressionContext):
        expr = ASTNodeConditional()
        self.add_node(expr)

    def enterMultiplication_expression(self, ctx: CParser.Multiplication_expressionContext):
        expr = ASTNodeMult()
        expr.operators = []
        self.add_node(expr)

    def enterUnary_expression(self, ctx: CParser.Unary_expressionContext):
        expr = ASTNodeUnaryExpr()
        self.add_node(expr)

    def enterVariable_definition(self, ctx: CParser.Variable_definitionContext):
        expr = ASTNodeDefinition()
        expr.name = ctx.ID().getText()
        expr.type = ctx.value_type().Type().getText()

        self.typeTable.insert_variable(expr.name, expr.type, None, None)

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
        expr.id = ctx.left_value().getText()
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
        self.skip_node()

    def enterReturn_statement(self, ctx: CParser.Return_statementContext):
        expr = ASTNodeReturn()
        self.add_node(expr)

    def enterStatement(self, ctx: CParser.StatementContext):
        expr = ASTNodeStatement()
        self.add_node(expr)

    def enterAddopp(self, ctx: CParser.AddoppContext):
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()
        # self.add_node(ASTNodeOpp(ctx.getText()))

    def enterMultopp(self, ctx: CParser.MultoppContext):
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()
        # self.add_node(ASTNodeOpp(ctx.getText()))

    def enterLog_or(self, ctx: CParser.AddoppContext):
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterLog_and(self, ctx: CParser.AddoppContext):
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterBinor(self, ctx: CParser.AddoppContext):
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterBinxor(self, ctx: CParser.AddoppContext):
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterBinand(self, ctx: CParser.AddoppContext):
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterLog_eq(self, ctx: CParser.AddoppContext):
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterRel_com(self, ctx: CParser.AddoppContext):
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    # ToDo: fix
    def enterLeft_value(self, ctx: CParser.Left_valueContext):
        self.skip_node()

    def enterDereference(self, ctx: CParser.DereferenceContext):
        self.add_node(ASTNodeDereference())

    def enterReference(self, ctx: CParser.ReferenceContext):
        self.add_node(ASTNodeReference())

    def enterL_indexing_expression(self, ctx: CParser.L_indexing_expressionContext):
        self.add_node(ASTNodeIndexingExpr)

    # ToDo: fix
    def enterValue_type(self, ctx: CParser.Value_typeContext):
        self.skip_node()

    def visitErrorNode(self, node: ErrorNode):
        print("Error", node.getText())

    '''helper functions'''

    def add_node(self, node):
        if self.depthStack:
            self.depthStack[-1].add_child(node)
        self.depthStack.append(node)

    def skip_node(self):
        self.depthStack.append(self.depthStack[-1])
