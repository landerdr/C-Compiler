from antlr4 import *
from gen.CLexer import CLexer
from gen.CListener import CListener
from gen.CParser import CParser

from Source.AST import *
from Source.TypeTable import TypeTable


class Reachability:
    def __init__(self):
        self.reachable = [True]

    def enter_scope(self):
        self.reachable.append(self.reachable[-1])

    def leave_scope(self):
        self.reachable.pop()

    def is_reachable(self):
        return self.reachable[-1]

    def set_not_reachable(self):
        self.reachable[-1] = False


class CPrintListener(CListener):

    def __init__(self):
        super(CPrintListener, self).__init__()
        self.typeTable = TypeTable()
        self.typeTable.enter_scope()
        self.depthStack = []
        self.tt = AST()
        self.propagation = False
        self.reachable = Reachability()
        self.propagation_ability_counter = 0

    '''Core'''

    def parse_string(self, _str):
        self.tt = AST()
        self.depthStack = []

        lexer = CLexer(_str)
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        tree = parser.library()

        if parser.getNumberOfSyntaxErrors() > 0:
            raise ParserException("%s parsing errors" % parser.getNumberOfSyntaxErrors())

        walker = ParseTreeWalker()
        walker.walk(self, tree)

        # print(self.typeTable)

    '''Rules'''

    def exitEveryRule(self, ctx: ParserRuleContext):
        if self.depthStack:
            # Get current node
            item = self.depthStack.pop()
            if item not in self.depthStack:
                item.unreachable = self.reachable.is_reachable()
                item.line_num = ctx.start.line
                item.optimise(self.typeTable, self.propagation)

    def enterEveryRule(self, ctx: ParserRuleContext):
        pass

    def enterLibrary(self, ctx: CParser.LibraryContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeLib()
        self.tt.root = expr
        self.depthStack.append(expr)

    def enterAdditional_expression(self, ctx: CParser.Additional_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeAddition()
        expr.operators = []
        self.add_node(expr)

    def enterBracket_expression(self, ctx: CParser.Bracket_expressionContext):
        self.skip_node()

    def enterBreak_statement(self, ctx: CParser.Break_statementContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeBreak()
        self.add_node(expr)

    def exitBreak_statement(self, ctx: CParser.Break_statementContext):
        self.reachable.set_not_reachable()

    def enterCompound_statement(self, ctx: CParser.Compound_statementContext):
        self.typeTable.enter_scope()
        self.reachable.enter_scope()
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeCompound()
        self.add_node(expr)

    def exitCompound_statement(self, ctx: CParser.Compound_statementContext):
        self.typeTable.leave_scope()
        self.reachable.leave_scope()

    def enterLiteral_expression(self, ctx: CParser.Literal_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        # Get txt
        txt = (ctx.ID() or ctx.Int() or ctx.Float() or ctx.Char() or ctx.String())

        expr = ASTNodeLiteral(txt)
        expr.line_num = ctx.start.line
        expr.prop_able = self.propagation_ability_counter == 0
        if ctx.Int():
            expr.isConst = True
            expr.value = int(txt.getText())
            expr.type = INT
        if ctx.Char():
            expr.isConst = True
            expr.value = str(txt.getText()[1])
            expr.type = CHAR
        if ctx.Float():
            expr.isConst = True
            expr.value = float(txt.getText())
            expr.type = FLOAT
        if ctx.String():
            expr.isString = True
            expr.isConst = True
            expr.value = txt.getText()[1:-1]
            expr.type = STRING
        self.add_node(expr)

    def enterExpression_statement(self, ctx: CParser.Expression_statementContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeExpressionStatement()
        self.add_node(expr)

    def enterExpression(self, ctx: CParser.ExpressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeExpression()
        self.add_node(expr)

    def enterTernary_expression(self, ctx: CParser.Ternary_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeTernaryExpr()
        self.add_node(expr)

    # ToDo: fix bitwise expressions
    def enterBitwise_and_expression(self, ctx: CParser.Bitwise_and_expressionContext):
        self.skip_node()

    def enterBitwise_or_expression(self, ctx: CParser.Bitwise_or_expressionContext):
        self.skip_node()

    def enterBitwise_xor_expression(self, ctx: CParser.Bitwise_xor_expressionContext):
        self.skip_node()

    def enterLogical_and_expression(self, ctx: CParser.Logical_and_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeConditional()
        self.add_node(expr)

    def enterLogical_or_expression(self, ctx: CParser.Logical_or_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeConditional()
        self.add_node(expr)

    def enterRelational_comparison_expression(self, ctx: CParser.Relational_comparison_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeConditional()
        self.add_node(expr)

    def enterRelational_equality_expression(self, ctx: CParser.Relational_equality_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeConditional()
        self.add_node(expr)

    def enterMultiplication_expression(self, ctx: CParser.Multiplication_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeMult()
        expr.operators = []
        expr.line_num = ctx.start.line
        self.add_node(expr)

    def enterUnary_expression(self, ctx: CParser.Unary_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeUnaryExpr()
        self.add_node(expr)

    def enterVariable_definition(self, ctx: CParser.Variable_definitionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeDefinition()
        expr.name = ctx.ID().getText()
        expr.type = string_to_type(ctx.value_type().Type().getText())
        if ctx.value_type().STAR() is not None:
            for i in range(len(ctx.value_type().STAR())):
                expr.type = Pointer(expr.type)
        expr.const = ctx.value_type().CONST() is not None
        if ctx.Int(0) is not None:
            expr.array = ctx.Int(0).getText()
        elif ctx.LSB():
            expr.array = -1
        self.add_node(expr)

    def enterConditional_statement(self, ctx: CParser.Conditional_statementContext):
        self.propagation_ability_counter += 1
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeIf()
        self.add_node(expr)

    def exitConditional_statement(self, ctx: CParser.Conditional_statementContext):
        self.propagation_ability_counter -= 1

    def enterContinue_statement(self, ctx: CParser.Continue_statementContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeContinue()
        self.add_node(expr)

    def exitContinue_statement(self, ctx: CParser.Continue_statementContext):
        self.reachable.set_not_reachable()

    def enterPost_xcrement(self, ctx: CParser.Post_xcrementContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodePostcrement()
        expr.operator = (ctx.DECREMENT() or ctx.INCREMENT()).getText()
        self.add_node(expr)

    def enterPre_xcrement(self, ctx: CParser.Pre_xcrementContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodePrecrement()
        expr.operator = (ctx.DECREMENT() or ctx.INCREMENT()).getText()
        self.add_node(expr)

    def enterEquality_expression(self, ctx: CParser.Equality_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeEqualityExpr()
        expr.equality = ctx.equality_symbol().getText()
        self.add_node(expr)

    def enterEquality_symbol(self, ctx: CParser.Equality_symbolContext):
        self.skip_node()

    def enterFunction(self, ctx: CParser.FunctionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeFunction()
        expr.name = ctx.ID().getText()
        if ctx.value_type():
            expr.type = string_to_type(ctx.value_type().Type().getText())
            if ctx.value_type().STAR():
                expr.type = Pointer(expr.type)
        else:
            expr.type = string_to_type(ctx.Void().getText())

        expr.fwd = ctx.TERMINUS() is not None

        self.typeTable.insert_function(expr.name, expr.type)
        self.add_node(expr)

    def enterFunction_call_expression(self, ctx: CParser.Function_call_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeFunctionCallExpr()
        expr.name = ctx.ID().getText()
        self.add_node(expr)

    def enterIndexing_expression(self, ctx: CParser.Indexing_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeIndexingExpr()
        expr.value = None
        self.add_node(expr)

    def enterInverse(self, ctx: CParser.InverseContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeInverseExpr()
        self.add_node(expr)

    def enterLoop_statement(self, ctx: CParser.Loop_statementContext):
        self.propagation_ability_counter += 1
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeLoopStatement()
        expr.loop_type = (ctx.Do() or ctx.For() or ctx.While()).getText()
        self.add_node(expr)

    def exitLoop_statement(self, ctx: CParser.Loop_statementContext):
        self.propagation_ability_counter -= 1

    def enterNegative(self, ctx: CParser.NegativeContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeNegativeExpr()
        self.add_node(expr)

    def enterParam(self, ctx: CParser.ParamContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeParam()
        expr.name = ctx.ID().getText()
        expr.type = string_to_type(ctx.value_type().Type().getText())
        if ctx.value_type().STAR() is not None:
            for i in range(len(ctx.value_type().STAR())):
                expr.type = Pointer(expr.type)

        expr.const = ctx.value_type().CONST() is not None
        if ctx.Int():
            expr.array = int(ctx.Int().getText())
        self.add_node(expr)

    def enterParams(self, ctx: CParser.ParamsContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeParams()
        self.add_node(expr)

    def enterPositive(self, ctx: CParser.PositiveContext):
        self.skip_node()

    def enterReturn_statement(self, ctx: CParser.Return_statementContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeReturn()
        self.add_node(expr)

    def exitReturn_statement(self, ctx: CParser.Return_statementContext):
        self.reachable.set_not_reachable()

    def enterStatement(self, ctx: CParser.StatementContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeStatement()
        self.add_node(expr)

    def enterAddopp(self, ctx: CParser.AddoppContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterMultopp(self, ctx: CParser.MultoppContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterLog_or(self, ctx: CParser.Log_orContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterLog_and(self, ctx: CParser.Log_andContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterBinor(self, ctx: CParser.BinorContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterBinxor(self, ctx: CParser.BinxorContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterBinand(self, ctx: CParser.BinandContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterLog_eq(self, ctx: CParser.Log_eqContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterRel_com(self, ctx: CParser.Rel_comContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        x = self.depthStack[-1]
        x.operators.append(ctx.getText())
        self.skip_node()

    def enterLeft_value(self, ctx: CParser.Left_valueContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeLeftValue()
        if ctx.ID():
            expr.name = ctx.ID().getText()
        self.add_node(expr)

    def enterDereference(self, ctx: CParser.DereferenceContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        self.add_node(ASTNodeDereference())

    def enterReference(self, ctx: CParser.ReferenceContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        self.add_node(ASTNodeReference())

    def enterL_indexing_expression(self, ctx: CParser.L_indexing_expressionContext):
        if not self.reachable.is_reachable():
            return self.skip_node()
        expr = ASTNodeIndexingExpr()
        expr.value = ctx.ID().getText()
        self.add_node(expr)

    def enterValue_type(self, ctx: CParser.Value_typeContext):
        self.skip_node()

    def enterInclude(self, ctx:CParser.IncludeContext):
        expr = ASTNodeInclude()
        expr.name = ctx.HeaderFile().getText()
        self.add_node(expr)

    def enterList_expression(self, ctx:CParser.List_expressionContext):
        expr = ASTNodeList()
        self.add_node(expr)

    def visitErrorNode(self, node: ErrorNode):
        print("Error", node.getText())

    '''helper functions'''

    def add_node(self, node):
        if self.depthStack:
            self.depthStack[-1].add_child(node)
        self.depthStack.append(node)

    def skip_node(self):
        self.depthStack.append(self.depthStack[-1])
