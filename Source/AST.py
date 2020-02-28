"""Abstract Syntax Tree"""


class AST:

    def __init__(self):
        self.root = None
        self.depthStack = []

    def simplify(self):
        self.depthStack = [self.root]

        while len(self.depthStack) > 0:
            item = self.depthStack.pop()

            if len(item.children) == 1:
                if isinstance(item, ASTNodeExpression) or isinstance(item, ASTNodeStatement):
                    # print("replacing:", item.value, "at pos:", item.index)
                    item.parent.replace_child(item.index, item.children[0])

            for i in reversed(item.children):
                self.depthStack.append(i)

    def print_tree(self):
        self.depthStack = [self.root]

        while len(self.depthStack) > 0:
            item = self.depthStack.pop()

            item.print_dot()

            for i in item.children:
                print('"', item, '" -> "', i, '"')

            for i in reversed(item.children):
                self.depthStack.append(i)


'''Core'''


class ASTNode:

    def __init__(self, _val='Undefined'):
        # print("created:", _val)
        self.parent = None
        self.index = 0
        self.children = []
        self.value = _val

    def add_child(self, child):
        # print("added: ", child.value, "to:", self.value)
        child.parent = self
        child.index = len(self.children)
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def remove_child_at_pos(self, index):
        pass

    def replace_child(self, index, new_child):
        new_child.parent = self
        new_child.index = index
        self.children[index] = new_child

    def print_dot(self):
        print('"', self, '"', '[label = "', self.value, '"]')


class ASTNodeLib(ASTNode):

    def __init__(self):
        super().__init__("Lib")


'''Statements'''


class ASTNodeStatement(ASTNode):
    def __init__(self, _val="Statement"):
        super().__init__(_val)

    pass


class ASTNodeBreak(ASTNodeStatement):

    def __init__(self):
        super().__init__("Break")


class ASTNodeExpressionStatement(ASTNodeStatement):
    def __init__(self, _val="Expression statement"):
        super().__init__(_val)

    pass


class ASTNodeCompound(ASTNodeStatement):
    def __init__(self, _val="Compound statement"):
        super().__init__(_val)

    pass


class ASTNodeDefinition(ASTNode):

    def __init__(self):
        super().__init__("Definition")
        self.type = None
        self.name = None

    def print_dot(self):
        print('"', self, '"', '[label = "', self.value, ":", self.type, self.name, '"]')


class ASTNodeIf(ASTNode):

    def __init__(self):
        super().__init__("If_Statement")
        self.Condition = None
        self.body = None


'''Expressions'''


class ASTNodeExpression(ASTNode):

    def __init__(self, val="Expression"):
        super().__init__(val)


class ASTNodeConditional(ASTNodeExpression):
    def __init__(self):
        super().__init__("Conditional expression")


class ASTNodeUnaryExpr(ASTNodeExpression):
    def __init__(self):
        super().__init__("Unary expression")


class ASTNodeTernaryExpr(ASTNodeExpression):
    def __init__(self):
        super().__init__("Ternary expression")


class ASTNodeLiteral(ASTNode):

    def __init__(self, value="Value"):
        super().__init__(value)


'''Opperations'''


class ASTNodeOpp(ASTNodeExpression):
    def __init__(self, tt="opp"):
        super().__init__(tt)
        self.Left = None
        self.Right = None


class ASTNodeAddition(ASTNodeOpp):

    def __init__(self):
        super().__init__("Addition")
        self.Left = None
        self.Right = None


class ASTNodeMult(ASTNodeOpp):

    def __init__(self):
        super().__init__("Multiplication")
        self.Left = None
        self.Right = None
