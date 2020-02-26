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
            print(item.value)
            for i in reversed(item.children):
                self.depthStack.append(i)

        pass


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
