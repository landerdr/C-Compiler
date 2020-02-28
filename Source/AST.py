class AST:

    def __init__(self):
        self.root = None
        self.depthStack = []

    def simplify(self):
        pass

    def print_tree(self):
        self.depthStack = [self.root]
        while len(self.depthStack) > 0:
            item = self.depthStack.pop()

            print('"', item, '"', '[label = "', item.value, '"]')

            for i in item.children:
                print('"', item, '" -> "', i, '"')

            for i in reversed(item.children):
                self.depthStack.append(i)


class ASTNode:

    def __init__(self, _val='a'):
        self.children = []
        self.value = _val

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def remove_child_at_pos(self, index):
        pass


class ASTNodeAssignment(ASTNode):

    def __init__(self):
        super().__init__("Assignment")
        self.id = None
        self.exprNode = None


class ASTNodeDefinition(ASTNode):

    def __init__(self, ll):
        super().__init__("Assignment")
        self.children = ll
        self.datatype = ll[0]
        self.id = ll[1]
        self.exprNode = ll[2]


class ASTNodeExpression(ASTNode):

    def __init__(self):
        super().__init__("Expression")


class ASTNodeOpp(ASTNode):
    def __init__(self, tt ="opp"):
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


class ASTNodeIf(ASTNode):

    def __init__(self):
        super().__init__("If_Statement")
        self.Condition = None
        self.body = None


class ASTNodeValue(ASTNode):

    def __init__(self, value="Value"):
        super().__init__(value)


class ASTNodeProg(ASTNode):

    def __init__(self):
        super().__init__("Prog")