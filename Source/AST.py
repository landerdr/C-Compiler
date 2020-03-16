"""Abstract Syntax Tree"""
from Source.TypeTable import *


# ToDo: add print_llvm_ir where necessary
# ToDo: make print_llvm_ir differentiate between data types
# ToDo: make print_llvm_it differentiate between operator types
# ToDo: splits simplify into Const collapse / propagation / gwn verwijdere van onnodige stuff, zoda we da zonder kunne runne


class ParserException(Exception):
    pass


class AST:
    def __init__(self):
        self.root = None
        self.depthStack = []
        self.typeTable = TypeTable()
        self.typeTable.enter_scope()

    # Deprecated function
    def simplify(self):
        self.depthStack = [self.root]
        while len(self.depthStack) > 0:
            item = self.depthStack.pop()
            if len(item.children) == 1:
                if (isinstance(item, ASTNodeExpression) or isinstance(item, ASTNodeStatement)) and item.canReplace:
                    item.parent.replace_child(item.index, item.children[0])

            for i in reversed(item.children):
                self.depthStack.append(i)

        temp = [self.root]
        self.depthStack = [self.root]
        while len(self.depthStack) > 0:
            item = self.depthStack.pop()
            for i in reversed(item.children):
                self.depthStack.append(i)
                temp.append(i)

        while len(temp) > 0:
            item = temp.pop()
            item.simplify()

    # Prints the tree in dot format to a specified file (terminal if no file was given.)
    def print_tree(self, _file=None):

        print("digraph G {", file=_file)

        self.depthStack = [self.root]

        while len(self.depthStack) > 0:
            item = self.depthStack.pop()

            item.print_dot(_file)

            for i in item.children:
                print('"', item, '" -> "', i, '"', file=_file)

            for i in reversed(item.children):
                self.depthStack.append(i)

        print("}", file=_file)

    # Builds the symbol table
    def build_symbol_table(self):

        self.depthStack = [self.root]

        while len(self.depthStack) > 0:
            item = self.depthStack.pop()

            for i in reversed(item.children):
                self.depthStack.append(i)

    # (Hopefully) Prints it's equivalent as llvm IR code
    def print_llvm_ir(self, _file=None):

        type_table = TypeTable()
        type_table.enter_scope()

        prestack = [self.root]
        grey = []
        visited = []

        while len(prestack) > 0:
            item = prestack.pop()

            # if entering this node for the first time -> print stuff
            if not (item in grey):
                grey.append(item)
                item.print_llvm_ir_pre(type_table, _file, len(type_table.tables))

            # check if a child hasn't been visited yet
            found = False
            for i in item.children:
                if not (i in visited):
                    prestack.append(item)
                    prestack.append(i)
                    found = True
                    break

            # no new nodes were found -> all children visited -> time to exit this node -> print stuff
            if not found:
                item.print_llvm_ir_post(type_table, _file, len(type_table.tables))
                visited.append(item)


'''Core'''


# Base node class
class ASTNode:
    def __init__(self, _val='Undefined'):
        self.canReplace = True
        self.parent = None
        self.index = 0
        self.children = []
        self.value = _val
        self.line_num = ""

    # Adds a child to it's list of children
    def add_child(self, child):
        child.parent = self
        child.index = len(self.children)
        self.children.append(child)

    # Remove a child from it's list of children
    def remove_child(self, child):
        self.children.remove(child)
        # Update children index
        for i in range(len(self.children)):
            self.children[i].index = i

    # Replace child at a certain position with the given new child
    def replace_child(self, index, new_child):
        new_child.parent = self
        new_child.index = index
        self.children[index] = new_child

    # Print dot format name and label
    def print_dot(self, _file=None):
        print('"', self, '"', '[label = "', self.value, '"]', file=_file)

    # Simplify this node structure if possible
    def optimise(self, symboltable):
        pass

    def const_folding(self):
        pass

    def const_propagation(self, symboltable):
        pass

    # Simplify this node structure if possible
    def simplify(self, symboltable):
        if len(self.children) == 1 and self.canReplace and self.parent is not None:
            self.delete()
        else:
            propagation = True
            self.optimise(symboltable)
            if propagation:
                self.const_propagation(symboltable)
            self.const_folding()

    # Deletes a node and connects it's first child to the former parent of this node
    def delete(self):
        # Put child in parent
        self.parent.replace_child(self.index, self.children[0])
        # Remove parent and children from node
        self.parent = None
        self.children = []

    # Prints it's equivalent as llvm IR code
    def print_llvm_ir_pre(self, _type_table, _file=None, _indent=0):
        pass

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0):
        pass

    def get_llvm_addr(self):
        return "%t" + str(id(self))

    def load_if_necessary(self, _file=None, _indent=0):
        if isinstance(self, ASTNodeLiteral):
            if not self.isConst:
                v1 = self.get_llvm_addr()
                print('  ' * _indent + v1 + " = load i32, i32* %" +
                      str(self.value) + ", align 4", file=_file)
                return v1
            else:
                return str(self.value)
        elif isinstance(self, ASTNodeLeftValue):
            v1 = self.get_llvm_addr()
            print('  ' * _indent + v1 + " = load i32, i32* %" +
                  str(self.name) + ", align 4", file=_file)
            return v1
        else:
            return "%t" + str(id(self))


# Base Library node
class ASTNodeLib(ASTNode):
    def __init__(self):
        super().__init__("Lib")


# Base function declaration node
class ASTNodeFunction(ASTNode):
    def __init__(self):
        super().__init__("Function")
        self.canReplace = False

    def print_llvm_ir_pre(self, _type_table, _file=None, _indent=0):
        print('  ' * _indent + "\ndefine i32 @main() #0 ", file=_file, end='')
        # print("%tmp" + str(id(self)) + " = mul i32 " + v1 + "," + v2, file=_file)

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0):
        pass


# Base list of parameters node
class ASTNodeParams(ASTNode):
    def __init__(self):
        super().__init__("Params")


# Single parameter node
class ASTNodeParam(ASTNode):
    def __init__(self):
        super().__init__("Param")
        self.name = ""
        self.type = ""

    def optimise(self, symboltable):
        symboltable.insert_variable(self.name, self.type)


class ASTNodeLeftValue(ASTNode):
    def __init__(self):
        super().__init__("Left Value")
        self.name = ""

    def print_dot(self, _file=None):
        print('"', self, '"', '[label = "', self.value, ":", self.name, '"]', file=_file)


'''Statements'''


# Base statement node
class ASTNodeStatement(ASTNode):
    def __init__(self, _val="Statement"):
        super().__init__(_val)


# Break statement node
class ASTNodeBreak(ASTNodeStatement):
    def __init__(self):
        super().__init__("Break")


# Continue statement node
class ASTNodeContinue(ASTNodeStatement):
    def __init__(self):
        super().__init__("Continue")


# Base expression statement node
class ASTNodeExpressionStatement(ASTNodeStatement):
    def __init__(self, _val="Expression statement"):
        super().__init__(_val)


# Compound statement node
class ASTNodeCompound(ASTNodeStatement):
    def __init__(self, _val="Compound statement"):
        super().__init__(_val)

    def print_llvm_ir_pre(self, _type_table, _file=None, _indent=0):
        _type_table.enter_scope()
        print('  ' * _indent + "{", file=_file)

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0):
        _type_table.leave_scope()
        print('  ' * (_indent - 1) + "}", file=_file)


# Definition statement node
class ASTNodeDefinition(ASTNodeStatement):
    def __init__(self):
        super().__init__("Definition")
        self.canReplace = False
        self.type = None
        self.name = None
        self.const = False
        self.pointer = False

    # Print dot format name and label
    def print_dot(self, _file=None):
        print('"', self, '"', '[label = "', self.value, ":", self.name, self.type, '"]', file=_file)

    def optimise(self, symboltable):
        value = None
        if len(self.children) == 0:
            pass
        elif isinstance(self.children[0], ASTNodeLiteral) and self.children[0].isConst:
            value = self.children[0].value
        elif isinstance(self.children[0], ASTNodeEqualityExpr):
            entry = symboltable.lookup_variable(self.children[0].get_name())
            value = entry.value
        else:
            value = "Unknown"

        if not symboltable.insert_variable(self.name, self.type, value=value, pointer=self.pointer, const=self.const):
            raise ParserException("Trying to redeclare variable '%s' at line %s" % (self.name, self.type))

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0):

        print('  ' * _indent + "%" + self.name + " =  alloca i32 , align 4", file=_file)
        if len(self.children) > 0:
            val = self.children[0].load_if_necessary(_file, _indent)
            print('  ' * _indent + "store i32 " + val + ", i32* %" + self.name + ", align 4", file=_file)


# If statement node
class ASTNodeIf(ASTNodeStatement):
    def __init__(self):
        super().__init__("If statement")
        self.Condition = None
        self.body = None


# Loop statement node
class ASTNodeLoopStatement(ASTNodeStatement):
    def __init__(self):
        super().__init__("Loop statement")
        self.Condition = None
        self.body = None


# Return statement node
class ASTNodeReturn(ASTNodeStatement):
    def __init__(self):
        super().__init__("Return statement")
        self.canReplace = False

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0):
        rval = self.children[0].load_if_necessary(_file, _indent)
        print('  ' * _indent + "ret i32 " + rval, file=_file)


'''Expressions'''


# Base expression node
class ASTNodeExpression(ASTNode):
    def __init__(self, val="Expression"):
        super().__init__(val)


# Unary expression node
class ASTNodeUnaryExpr(ASTNodeExpression):
    def __init__(self, _val="Unary expression"):
        super().__init__(_val)


# Ternary expression node
class ASTNodeTernaryExpr(ASTNodeExpression):
    def __init__(self):
        super().__init__("Ternary expression")


# Node literal
class ASTNodeLiteral(ASTNode):
    def __init__(self, value="Value"):
        super().__init__(value)
        self.isConst = False
        self.canReplace = False

    def const_propagation(self, symboltable):
        if not self.isConst:
            # Lookup variable in type table
            entry = symboltable.lookup_variable(str(self.value))
            # Replace with value from symboltable
            replacement = ASTNodeLiteral(entry.value)
            replacement.isConst = True
            # Give child temporary values
            replacement.parent = self
            replacement.index = 0
            # Insert child at front of children
            self.children.insert(0, replacement)
            self.delete()

    # Simplify this node structure if possible
    def optimise(self, symboltable):
        # Check if literal is variable
        if not self.isConst:
            # Lookup variable in type table
            entry = symboltable.lookup_variable(str(self.value))
            if not entry:
                raise ParserException("Non declared variable '%s' at line %s" % (self.value, self.line_num))
            if entry.value is None:
                raise ParserException("Non defined variable '%s' at line %s" % (self.value, self.line_num))


# Decrement expression node
class ASTNodePostcrement(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Post in/decrement")
        self.canReplace = False
        self.operator = None

    def optimise(self, symboltable):
        entry = symboltable.lookup_variable(self.children[0].name)
        if not entry:
            raise ParserException("Non declared variable '%s' at line %s" % (self.children[0].name, self.line_num))
        if entry.value is None:
            raise ParserException("Non defined variable '%s' at line %s" % (self.children[0].name, self.line_num))

        if entry.value == "Unknown":
            return

        new_child = ASTNodeLiteral(entry.value)
        new_child.canReplace = True
        new_child.parent = self
        self.children = [new_child]
        self.delete()

        if self.operator == "++":
            entry.value += 1
        elif self.operator == "--":
            entry.value -= 1


# Increment expression node
class ASTNodePrecrement(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Pre in/decrement")
        self.canReplace = False
        self.operator = None

    def optimise(self, symboltable):
        entry = symboltable.lookup_variable(self.children[0].name)
        if not entry:
            raise ParserException("Non declared variable '%s' at line %s" % (self.children[0].name, self.line_num))
        if entry.value is None:
            raise ParserException("Non defined variable '%s' at line %s" % (self.children[0].name, self.line_num))

        if entry.value == "Unknown":
            return

        if self.operator == "++":
            entry.value += 1
        elif self.operator == "--":
            entry.value -= 1

        new_child = ASTNodeLiteral(entry.value)
        new_child.canReplace = True
        new_child.parent = self
        self.children = [new_child]
        self.delete()


# Equality expression node
class ASTNodeEqualityExpr(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Equality expression")
        self.canReplace = False
        self.equality = None

    def get_name(self):
        return self.children[0].name

    # Print dot format name and label
    def print_dot(self, _file=None):
        print('"', self, '"', '[label = "', self.value, ":", self.equality, '"]', file=_file)

    def optimise(self, symboltable):
        entry = symboltable.lookup_variable(self.get_name())
        if not entry:
            raise ParserException("Non declared variable '%s' at line %s" % (self.get_name(), self.line_num))
        if entry.const:
            raise ParserException("Trying to redefine variable '%s' at line %s" % (self.get_name(), self.line_num))
        if len(self.children) == 2 and isinstance(self.children[1], ASTNodeLiteral) and self.children[1].isConst:
            value = self.children[1].value
            if self.equality == "=":
                pass
            elif self.equality == "+=":
                value = entry.value + value
            elif self.equality == "-=":
                value = entry.value - value
            elif self.equality == "/=":
                value_type = get_type(entry.value, value)
                if value == 0:
                    raise ParserException("division by zero at line %s" % self.line_num)
                value = entry.value / value
                if value_type != float:
                    value = int(value)
            elif self.equality == "*=":
                value = entry.value * value
            elif self.equality == "%=":
                value = entry.value % value
            else:
                raise ParserException("Not implemented yet")
        else:
            value = "Unknown"
        entry.value = value

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0):
        v1 = self.children[1].load_if_necessary(_file, _indent)

        if self.equality != "=":
            opp = 'add'
            if self.equality == "-=":
                opp = "sub"
            if self.equality == "/=":
                opp = 'sdiv'
            if self.equality == "*=":
                opp = 'mul'
            if self.equality == "%=":
                opp = 'srem'

            new_v1 = self.get_llvm_addr()
            print('  ' * _indent + new_v1 + " = " + opp + " i32 " + self.children[0].load_if_necessary(_file, _indent) + "," + v1, file=_file)
            v1 = new_v1

        print('  ' * _indent + "store i32 " + v1 + ", i32* %" + self.get_name() + ", align 4", file=_file)


# Function call expression node
class ASTNodeFunctionCallExpr(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Function call expression")
        self.name = None
        self.canReplace = False
    def print_llvm_ir_pre(self, _type_table, _file=None, _indent=0):
        print("  "*_indent + self.get_llvm_addr() + " = call i32 (i8*, ...) @" + self.name + "(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @.str, i32 0, i32 0))", file=_file)


# Indexing expression node
class ASTNodeIndexingExpr(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Indexing expression")


# Inverse expression node
class ASTNodeInverseExpr(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Inverse expression")
        self.canReplace = False

    # Simplify this node structure if possible
    def optimise(self, symboltable):
        if isinstance(self.children[0], ASTNodeLiteral):
            if self.children[0].isConst:
                self.children[0].value = not self.children[0].value
                self.delete()


# Negative expression node
class ASTNodeNegativeExpr(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Negative expression")
        self.canReplace = False

    # Simplify this node structure if possible
    def optimise(self, symboltable):
        if isinstance(self.children[0], ASTNodeLiteral):
            if self.children[0].isConst:
                self.children[0].value *= -1
                self.delete()


# Reference expression node
class ASTNodeReference(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Reference expression")


# Dereference expression node
class ASTNodeDereference(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Dereference expression")


'''Operations'''


# Base operation expression node
class ASTNodeOp(ASTNodeExpression):
    def __init__(self, tt="expr_op"):
        super().__init__(tt)
        self.operators = []


# Addition expression node
class ASTNodeAddition(ASTNodeOp):
    def __init__(self):
        super().__init__("Addition")

    def print_dot(self, _file=None):
        print('"', self, '"', '[label = "', self.value, ":", self.operators, '"]', file=_file)

    # Simplify this node structure if possible
    def optimise(self, symboltable):
        # Run over all operators
        for i in range(len(self.operators)):
            # Get relevant children and operator
            opp = self.operators[i]
            left = self.children[0]
            right = self.children[1]
            self.children = self.children[2:] if len(self.children) > 2 else []

            # Simplify if possible
            if isinstance(left, ASTNodeLiteral) and isinstance(right,
                                                               ASTNodeLiteral) and left.isConst and right.isConst:
                if opp == "+":
                    new_val = left.value + right.value
                else:
                    new_val = left.value - right.value

                new_child = ASTNodeLiteral(new_val)
                new_child.isConst = True
            # Create binary AST if we can't simplify
            else:
                new_child = ASTNodeAddition()
                new_child.add_child(left)
                new_child.add_child(right)
                new_child.operators = [opp]

            # Give child temporary values
            new_child.parent = self
            new_child.index = 0
            # Insert child at front of children
            self.children.insert(0, new_child)

        self.delete()

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0):
        v0 = self.children[0].load_if_necessary(_file, _indent)
        v1 = self.children[1].load_if_necessary(_file, _indent)
        opp = "add"
        if self.operators[0] == '-':
            opp = 'sub'
        print('  ' * _indent + "%t" + str(id(self)) + " = " + opp + " i32 " + v0 + "," + v1, file=_file)


# Multiplication expression node
class ASTNodeMult(ASTNodeOp):
    def __init__(self):
        super().__init__("Multiplication")

    # Simplify this node structure if possible
    def optimise(self, symboltable):
        # Run over all operators
        for i in range(len(self.operators)):
            # Get relevant children and operator
            opp = self.operators[i]
            left = self.children[0]
            right = self.children[1]
            self.children = self.children[2:] if len(self.children) > 2 else []

            # Simplify if possible
            if isinstance(left, ASTNodeLiteral) and isinstance(right,
                                                               ASTNodeLiteral) and left.isConst and right.isConst:
                value_type = get_type(left.value, right.value)
                if opp == "*":
                    new_val = left.value * right.value
                elif opp == "/":
                    if right.value == 0:
                        raise ParserException("division by zero at line %s" % self.line_num)
                    new_val = left.value / right.value
                    if value_type != float:
                        new_val = int(new_val)
                else:
                    new_val = left.value % right.value

                new_child = ASTNodeLiteral(new_val)
                new_child.isConst = True
            # Create binary AST if we can't simplify
            else:
                new_child = ASTNodeMult()
                new_child.add_child(left)
                new_child.add_child(right)
                new_child.operators = [opp]

            # Give child temporary values
            new_child.parent = self
            new_child.index = 0
            # Insert child at front of children
            self.children.insert(0, new_child)

        self.delete()

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0):
        v0 = self.children[0].load_if_necessary(_file, _indent)
        v1 = self.children[1].load_if_necessary(_file, _indent)
        opp = "mul"
        if self.operators[0] == '/':
            opp = 'sdiv'
        elif self.operators[0] == '%':
            opp = 'srem'

        print('  ' * _indent + "%t" + str(id(self)) + " = " + opp + " i32 " + v0 + "," + v1, file=_file)


# Conditional expression node
class ASTNodeConditional(ASTNodeOp):
    def __init__(self):
        super().__init__("Conditional expression")

    # Simplify this node structure if possible
    def optimise(self, symboltable):
        # Run over all operators
        for i in range(len(self.operators)):
            # Get relevant children and operator
            opp = self.operators[i]
            left = self.children[0]
            right = self.children[1]
            self.children = self.children[2:] if len(self.children) > 2 else []

            # Simplify if possible
            if isinstance(left, ASTNodeLiteral) and isinstance(right,
                                                               ASTNodeLiteral) and left.isConst and right.isConst:
                if opp == "==":
                    new_val = left.value == right.value
                elif opp == "<":
                    new_val = left.value < right.value
                elif opp == ">":
                    new_val = left.value > right.value
                elif opp == "&&":
                    new_val = left.value and right.value
                elif opp == "||":
                    new_val = left.value or right.value
                elif opp == "!=":
                    new_val = left.value != right.value
                elif opp == "<=":
                    new_val = left.value <= right.value
                elif opp == ">=":
                    new_val = left.value >= right.value
                else:
                    raise ParserException("Not implemented yet")

                new_child = ASTNodeLiteral(new_val)
                new_child.isConst = True
            # Create binary AST if we can't simplify
            else:
                new_child = ASTNodeConditional()
                new_child.add_child(left)
                new_child.add_child(right)
                new_child.operators = [opp]

            # Give child temporary values
            new_child.parent = self
            new_child.index = 0
            # Insert child at front of children
            self.children.insert(0, new_child)

        self.delete()
