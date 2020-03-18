"""Abstract Syntax Tree"""
from Source.TypeTable import *


# ToDo: add print_llvm_ir where necessary
# ToDo: make print_llvm_ir differentiate between data types
# ToDo: make print_llvm_it differentiate between operator types
# ToDo: splits simplify into Const collapse / propagation / gwn verwijdere van onnodige stuff, zoda we da zonder kunne runne


class ParserException(Exception):
    pass


class ModuloException(Exception):
    pass


last_label = 0


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
            item.optimise()

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

    # ToDo: optimize if necessary
    # (Hopefully) Prints it's equivalent as llvm IR code
    def print_llvm_ir(self, _file_name=None):
        _file = open(_file_name, 'w+')

        type_table = TypeTable()
        type_table.enter_scope()

        string_list = []

        prestack = [self.root]
        grey = []
        visited = []

        while len(prestack) > 0:
            item = prestack[-1]

            # if entering this node for the first time -> print stuff
            if not (item in grey):
                grey.append(item)
                item.print_llvm_ir_pre(type_table, _file, len(type_table.tables), string_list)

            # check if a child hasn't been visited yet
            found = False
            for i in item.children:
                if not (i in visited):
                    # prestack.append(item)
                    prestack.append(i)
                    found = True
                    break

            # no new nodes were found -> all children visited -> time to exit this node -> print stuff
            if not found:
                prestack.pop()
                item.print_llvm_ir_post(type_table, _file, len(type_table.tables), string_list)
                visited.append(item)

        for i in range(0, len(string_list)):
            string_ref = "@.str"
            if i > 0:
                string_ref += '.' + str(i)
            print(string_ref + " = private unnamed_addr constant [3 x i8] c\"" + string_list[i] + "\\00\", align 1",
                  file=_file)

        print("\ndeclare i32 @printf(i8*, ...) #1\n", file=_file)
        print(
            '\nattributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }',
            file=_file)


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

    # Greatly simplifies the tree structure, removes redundant children, etc
    # Checks for errors in semantics
    def _reduce(self, symboltable):
        pass

    # Constant folds (expects reduced node)
    def _const_folding(self):
        pass

    # Constant propagation (expects reduced node)
    def _const_propagation(self, symboltable):
        pass

    # Optimises this node structure if possible
    def optimise(self, symboltable, propagation=False):
        if len(self.children) == 1 and self.canReplace and self.parent is not None:
            self.delete()
        else:
            self._reduce(symboltable)
            if propagation:
                self._const_propagation(symboltable)
            self._const_folding()

    # Deletes a node and connects it's first child to the former parent of this node
    def delete(self):
        # Put child in parent
        self.parent.replace_child(self.index, self.children[0])
        # Remove parent and children from node
        self.parent = None
        self.children = []

    # Prints it's equivalent as llvm IR code
    def print_llvm_ir_pre(self, _type_table, _file=None, _indent=0, _string_list=None):
        pass

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
        pass

    def get_llvm_addr(self):
        return "%t" + str(id(self))

    def _load(self, name, _type_table, _file=None, _indent=0):
        v1 = self.get_llvm_addr()
        entry = self.get_llvm_type(_type_table, str(name))
        llvm_type = entry[0]
        pointer = entry[1]
        allign = '4'
        if pointer:
            llvm_type += '*'
            allign = '8'
        print('    ' * _indent + v1 + " = load " + llvm_type + ", " + llvm_type + "* %" +
              str(name) + ", align " + allign, file=_file)
        return v1

    def load_if_necessary(self, _type_table, _file=None, _indent=0):
        if isinstance(self, ASTNodeLiteral):
            if not self.isConst:
                return self._load(self.value, _type_table, _file, _indent)
            else:
                return str(self.value)
        elif isinstance(self, ASTNodeLeftValue):
            return self._load(self.name, _type_table, _file, _indent)

        elif isinstance(self, ASTNodeEqualityExpr):
            return self._load(self.children[0].name, _type_table, _file, _indent)
        else:
            return self.get_llvm_addr()

    def get_llvm_type(self, _type_table, _var_name=None):
        if _var_name:
            entry = _type_table.lookup_variable(_var_name)
            return entry.type.get_llvm_type(), entry.pointer

        if isinstance(self, ASTNodeLiteral):
            if not self.isConst:
                entry = _type_table.lookup_variable(str(self.value))
                return entry.type.get_llvm_type(), entry.pointer
            else:
                if isinstance(self.value, int):
                    return 'i32'
                return 'float'
        elif isinstance(self, ASTNodeLeftValue):
            entry = _type_table.lookup_variable(self.name)
            if isinstance(entry.type, str):
                return entry.type, entry.pointer
            else:
                return entry.type.get_llvm_type(), entry.pointer
        elif isinstance(self, ASTNodeEqualityExpr):
            entry = _type_table.lookup_variable(self.children[0].name)
            if isinstance(entry.type, str):
                return entry.type, entry.pointer
            else:
                return entry.type.get_llvm_type(), entry.pointer
        else:
            entry = _type_table.lookup_variable(self.get_llvm_addr())
            if isinstance(entry.type, str):
                return entry.type, entry.pointer
            else:
                return entry.type.get_llvm_type(), entry.pointer


# Base Library node
class ASTNodeLib(ASTNode):
    def __init__(self):
        super().__init__("Lib")


# Base function declaration node
class ASTNodeFunction(ASTNode):
    def __init__(self):
        super().__init__("Function")
        self.canReplace = False

    def print_llvm_ir_pre(self, _type_table, _file=None, _indent=0, _string_list=None):
        print('\n' + '; Function Attrs: noinline nounwind optnone uwtable', file=_file)
        print("define i32 @main() #0 {", file=_file, )
        _type_table.enter_scope()
        _indent += 1
        print('    ' * _indent + self.get_llvm_addr() + " =  alloca i32, align 4", file=_file)
        # print("%tmp" + str(id(self)) + " = mul i32 " + v1 + "," + v2, file=_file)

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
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

    def _reduce(self, symboltable):
        symboltable.insert_param(self.name, self.type)


class ASTNodeLeftValue(ASTNode):
    def __init__(self):
        super().__init__("Left Value")
        self.name = ""
        self.pointer = False
        self.type = None

    def _reduce(self, symboltable):
        entry = symboltable.lookup_variable(self.name)
        if not entry:
            raise ParserException("Non declared variable '%s' at line %s" % (self.name, self.line_num))
        self.pointer = entry.pointer
        self.type = entry.type

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

    def print_llvm_ir_pre(self, _type_table, _file=None, _indent=0, _string_list=None):
        if isinstance(self.parent, ASTNodeFunction):
            return
        _type_table.enter_scope()
        print('  ' * _indent + "{", file=_file)

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
        _type_table.leave_scope()
        _indent -= 1
        print('    ' * _indent + "}", file=_file)


# Definition statement node
class ASTNodeDefinition(ASTNodeStatement):
    def __init__(self):
        self.init__ = super().__init__("Definition")
        self.canReplace = False
        self.type = None
        self.name = None
        self.const = False
        self.pointer = False

    # Print dot format name and label
    def print_dot(self, _file=None):
        print('"', self, '"', '[label = "', self.value, ":", self.name, self.type, '"]', file=_file)

    def _reduce(self, symboltable):
        value = None
        if len(self.children) == 0:
            pass
        elif isinstance(self.children[0], ASTNodeLiteral) and self.children[0].isConst:
            value = self.children[0].value
        elif isinstance(self.children[0], ASTNodeEqualityExpr):
            entry = symboltable.lookup_variable(self.children[0].get_name())
            value = entry.value
        elif self.pointer != isinstance(self.children[0], ASTNodeReference):
            raise ParserException("Trying to assign incompatible types at line %s" % self.line_num)
        else:
            value = "Unknown"
            if string_to_type(self.type) < self.children[0].type:
                print("Warning: implicit conversion from '%s' to '%s' at line %s" % (
                string_to_type(self.type), self.children[0].type, self.line_num))

        if not symboltable.insert_variable(self.name, self.type, value=value, pointer=self.pointer, const=self.const,
                                           line_num=self.line_num):
            raise ParserException("Trying to redeclare variable '%s' at line %s" % (self.name, self.line_num))

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):

        if not _type_table.insert_variable(self.name, self.type, pointer=self.pointer, const=self.const):
            raise ParserException("Trying to redeclare variable %s at line %s" % (self.name, self.line_num))

        llvm_type = self.get_llvm_type(_type_table, self.name)[0]
        allign = '4'
        if self.pointer:
            llvm_type += '*'
            allign = '8'

        print('    ' * _indent + "%" + self.name + " =  alloca " + llvm_type + " , align " + allign, file=_file)
        if len(self.children) > 0:
            v1 = self.children[0].load_if_necessary(_type_table, _file, _indent)
            t1 = self.children[0].get_llvm_type(_type_table)[0]
            v1 = convert_type(t1, llvm_type, v1, _file, _indent)
            print('    ' * _indent + "store " + llvm_type + " " + v1 + ", " + llvm_type + "* %" + self.name + ", align 4",
                  file=_file)


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

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
        rval = self.children[0].load_if_necessary(_type_table, _file, _indent)
        new_val = convert_type(self.children[0].get_llvm_type(_type_table)[0], 'i32', rval, _file, _indent)
        print('    ' * _indent + "ret i32 " + new_val, file=_file)


'''Expressions'''


# Base expression node
class ASTNodeExpression(ASTNode):
    def __init__(self, val="Expression"):
        super().__init__(val)
        # To support typechecking when const propagation is disabled
        self.pointer = False
        self.type = None


# Unary expression node
class ASTNodeUnaryExpr(ASTNodeExpression):
    def __init__(self, _val="Unary expression"):
        super().__init__(_val)


# Ternary expression node
class ASTNodeTernaryExpr(ASTNodeExpression):
    def __init__(self):
        super().__init__("Ternary expression")


# Node literal
class ASTNodeLiteral(ASTNodeExpression):
    def __init__(self, value="Value"):
        super().__init__(value)
        self.isConst = False
        self.canReplace = False

    def _const_propagation(self, symboltable):
        if not self.isConst:
            # Lookup variable in type table
            entry = symboltable.lookup_variable(str(self.value))
            if not entry.pointer and not entry.value == "Unknown":
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
    def _reduce(self, symboltable):
        # Check if literal is variable
        if not self.isConst:
            # Lookup variable in type table
            entry = symboltable.lookup_variable(str(self.value))
            if not entry:
                raise ParserException("Non declared variable '%s' at line %s" % (self.value, self.line_num))
            if entry.value is None:
                raise ParserException("Non defined variable '%s' at line %s" % (self.value, self.line_num))
            self.pointer = entry.pointer
            self.type = entry.type


# Postcrement expression node (In/Decrement behind var)
class ASTNodePostcrement(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Post in/decrement")
        self.canReplace = False
        self.operator = None

    def _reduce(self, symboltable):
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

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
        v0 = self.children[0].load_if_necessary(_type_table, _file, _indent)
        t0 = self.children[0].get_llvm_type(_type_table)[0]

        new_var = convert_types(t0, 'i8', v0, '1', _file, _indent)
        v0 = new_var[0]
        v1 = new_var[1]
        llvm_type = new_var[2]

        opp = "add"
        if llvm_type == 'float':
            opp = 'fadd'
        if self.operator == '--':
            opp = 'sub'
            if llvm_type == 'float':
                opp = 'fsub'

        new_addr = self.get_llvm_addr()
        if not _type_table.insert_variable(new_addr, llvm_type):
            raise ParserException("Trying to redeclare variable '%s' at line %s" % (new_addr, llvm_type))

        print('    ' * _indent + new_addr + " = " + opp + " " + llvm_type + " " + v0 + "," + v1, file=_file)
        print('    ' * _indent + "store " + llvm_type + " " + new_addr + ", " + llvm_type + "* %" + self.children[0].name
              + ", align 4 ", file=_file)


# Precrement expression node (In/Decrement in front of var)
class ASTNodePrecrement(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Pre in/decrement")
        self.canReplace = False
        self.operator = None

    def _reduce(self, symboltable):
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

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
        pass


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

    def _reduce(self, symboltable):
        entry = symboltable.lookup_variable(self.get_name())
        if not entry:
            raise ParserException("Non declared variable '%s' at line %s" % (self.get_name(), self.line_num))
        if entry.const:
            raise ParserException(
                "Trying to redefine const variable '%s' at line %s" % (self.get_name(), self.line_num))
        child = self.children[1]
        if len(self.children) == 2 and isinstance(child, ASTNodeLiteral) and child.isConst and entry.value != "Unknown":
            value = child.value
            value_type = get_dominant_type(entry.type, child.type)
            if self.equality == "=":
                pass
            elif self.equality == "+=":
                value = entry.value + value
            elif self.equality == "-=":
                value = entry.value - value
            elif self.equality == "/=":
                if value == 0:
                    raise ParserException("Division by zero at line %s" % self.line_num)
                value = entry.value / value
                if value_type != FLOAT:
                    value = int(value)
            elif self.equality == "*=":
                value = entry.value * value
            elif self.equality == "%=":
                if value_type == FLOAT:
                    raise ParserException("Invalid operation '%=' with float argument(s) at line " + str(self.line_num))
                value = entry.value % value
            else:
                raise ParserException("Not implemented yet")
        else:
            if isinstance(self.children[1], ASTNodeLiteral) and entry.pointer != self.children[1].pointer \
                    or isinstance(self.children[1], ASTNodeReference) != entry.pointer:
                raise ParserException("Trying to assign incompatible types at line %s" % self.line_num)
            value = "Unknown"
            if entry.type < child.type:
                print("Warning: implicit conversion from '%s' to '%s' at line %s" % (
                entry.type, child.type, self.line_num))
        entry.update_value(value, self.line_num)

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
        v1 = self.children[1].load_if_necessary(_type_table, _file, _indent)
        this_var = _type_table.lookup_variable(self.get_name())
        llvm_type = this_var.type.get_llvm_type()[0]
        t1 = self.children[1].get_llvm_type(_type_table)[0]
        v1 = convert_type(t1, llvm_type, v1, _file, _indent)

        if self.equality != "=":
            opp = 'add'
            if llvm_type == 'float':
                opp = 'fadd'
            if self.equality == "-=":
                opp = "sub"
                if llvm_type == 'float':
                    opp = 'fsub'
            if self.equality == "/=":
                opp = 'sdiv'
                if llvm_type == 'float':
                    opp = 'fdiv'
            if self.equality == "*=":
                opp = 'mul'
                if llvm_type == 'float':
                    opp = 'fmul'
            if self.equality == "%=":
                opp = 'srem'
                if llvm_type == 'float':
                    raise ModuloException('Trying to use modulo on float type')

            new_v1 = self.get_llvm_addr()
            print('    ' * _indent + new_v1 + " = " + opp + " " + llvm_type + " " + self.children[0].load_if_necessary(
                _type_table, _file, _indent) + "," + v1, file=_file)
            v1 = new_v1

        print(
            '    ' * _indent + "store " + llvm_type + " " + v1 + ", " + llvm_type + "* %" + self.get_name() + ", align 4",
            file=_file)


# Function call expression node
class ASTNodeFunctionCallExpr(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Function call expression")
        self.name = None
        self.canReplace = False

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
        if self.name == 'printf':
            printed_type = self.children[0].get_llvm_type(_type_table)[0]

            if printed_type == 'i8':
                _string_list.append("%c")
            if printed_type == 'i32':
                _string_list.append("%d")
            if printed_type == 'float':
                _string_list.append("%f")
            value = self.children[0].load_if_necessary(_type_table, _file, _indent)
            value = convert_type(printed_type, printed_type, value, _file, _indent)
            if printed_type == 'float':
                printed_type = 'double'
                value = convert_type('float', printed_type, value, _file, _indent)

            string_ref = "@.str"
            if len(_string_list) > 1:
                string_ref += "." + str(len(_string_list) - 1)

            print(
                "  " * _indent + self.get_llvm_addr() + " = call i32 (i8*, ...) @" + self.name +
                "(i8* getelementptr inbounds ([3 x i8], [3 x i8]* " + string_ref + ", i32 0, i32 0)," + printed_type +
                ' ' + value + ")", file=_file)


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
    def _reduce(self, symboltable):
        self.type = self.children[0].type
        if isinstance(self.children[0], ASTNodeLiteral):
            if self.children[0].isConst:
                self.children[0].value = int(not self.children[0].value)
                self.children[0].type = INT
                self.delete()


# Negative expression node
class ASTNodeNegativeExpr(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Negative expression")
        self.canReplace = False

    # Simplify this node structure if possible
    def _reduce(self, symboltable):
        self.type = self.children[0].type
        if isinstance(self.children[0], ASTNodeLiteral):
            if self.children[0].isConst:
                self.children[0].value *= -1
                self.delete()

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
        v0 = self.children[0].load_if_necessary(_type_table, _file, _indent)
        v1 = '-1'
        t0 = self.children[0].get_llvm_type(_type_table)[0]
        t1 = 'i8'
        new_var = convert_types(t0, t1, v0, v1, _file, _indent)
        v0 = new_var[0]
        v1 = new_var[1]
        llvm_type = new_var[2]
        opp = "add"
        if llvm_type == 'float':
            opp = 'fadd'

        new_addr = self.get_llvm_addr()
        if not _type_table.insert_variable(new_addr, llvm_type):
            raise ParserException("Trying to redeclare variable '%s' at line %s" % (self.name, llvm_type))

        print('    ' * _indent + new_addr + " = " + opp + " " + llvm_type + " " + v0 + "," + v1, file=_file)


# Reference expression node
class ASTNodeReference(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Reference expression")
        self.canReplace = False
        self.pointer = True

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
        pass


# Dereference expression node
class ASTNodeDereference(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Dereference expression")
        self.canReplace = False

    def _reduce(self, symboltable):
        if not self.children[0].pointer:
            raise ParserException("Trying to dereference non pointer value at line %s" % self.line_num)

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):

        child = self.children[0]
        new_addr = self.get_llvm_addr()
        entry = child.get_llvm_type(_type_table)
        llvm_type = entry[0]
        v0 = child.load_if_necessary(_type_table, _file, _indent)

        if not _type_table.insert_variable(new_addr, llvm_type, pointer=entry[1]):
            raise ParserException("Trying to redeclare variable '%s' at line %s" % (new_addr, llvm_type))

        print('    ' * _indent + new_addr + " = load " + llvm_type + ", " + llvm_type + "* " +
              v0 + ", align 4", file=_file)


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
    def _reduce(self, symboltable):
        # Run over all operators
        for i in range(len(self.operators)):
            # Get relevant children and operator
            opp = self.operators[i]
            left = self.children[0]
            right = self.children[1]
            self.children = self.children[2:] if len(self.children) > 2 else []

            # Simplify if possible
            if isinstance(left, ASTNodeLiteral) and isinstance(right, ASTNodeLiteral) \
                    and left.isConst and right.isConst:
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
            new_child.type = get_dominant_type(left.type, right.type)
            # Insert child at front of children
            self.children.insert(0, new_child)

        self.delete()

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):

        v0 = self.children[0].load_if_necessary(_type_table, _file, _indent)
        v1 = self.children[1].load_if_necessary(_type_table, _file, _indent)
        t0 = self.children[0].get_llvm_type(_type_table)[0]
        t1 = self.children[1].get_llvm_type(_type_table)[0]

        new_var = convert_types(t0, t1, v0, v1, _file, _indent)
        v0 = new_var[0]
        v1 = new_var[1]
        llvm_type = new_var[2]

        opp = "add"
        if llvm_type == 'float':
            opp = 'fadd'
        if self.operators[0] == '-':
            opp = 'sub'
            if llvm_type == 'float':
                opp = 'fsub'

        new_addr = self.get_llvm_addr()
        if not _type_table.insert_variable(new_addr, llvm_type):
            raise ParserException("Trying to redeclare variable '%s' at line %s" % (new_addr, llvm_type))

        print('    ' * _indent + new_addr + " = " + opp + " " + llvm_type + " " + v0 + "," + v1, file=_file)


# Multiplication expression node
class ASTNodeMult(ASTNodeOp):
    def __init__(self):
        super().__init__("Multiplication")

    # Simplify this node structure if possible
    def _reduce(self, symboltable):
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
                value_type = get_dominant_type(left.type, right.type)
                if opp == "*":
                    new_val = left.value * right.value
                elif opp == "/":
                    if right.value == 0:
                        raise ParserException("Division by zero at line %s" % self.line_num)
                    print(left.value, right.value)
                    new_val = left.value / right.value
                    if value_type != FLOAT:
                        new_val = int(new_val)
                elif opp == "%":
                    if value_type == FLOAT:
                        raise ParserException(
                            "Invalid operation '%' with float argument(s) at line " + str(self.line_num))
                    new_val = left.value % right.value
                else:
                    raise ParserException("Not implemented yet")

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
            new_child.type = get_dominant_type(left.type, right.type)
            # Insert child at front of children
            self.children.insert(0, new_child)

        self.delete()

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
        v0 = self.children[0].load_if_necessary(_type_table, _file, _indent)
        v1 = self.children[1].load_if_necessary(_type_table, _file, _indent)
        t0 = self.children[0].get_llvm_type(_type_table)[0]
        t1 = self.children[1].get_llvm_type(_type_table)[0]
        new_var = convert_types(t0, t1, v0, v1, _file, _indent)
        v0 = new_var[0]
        v1 = new_var[1]
        llvm_type = new_var[2]

        opp = "mul"
        if llvm_type == 'float':
            opp = 'fmul'
        if self.operators[0] == '/':
            opp = 'sdiv'
            if llvm_type == 'float':
                opp = 'fdiv'

        elif self.operators[0] == '%':
            opp = 'srem'
            if llvm_type == 'float':
                raise ModuloException('Trying to use modulo on float type')

        new_addr = self.get_llvm_addr()
        if not _type_table.insert_variable(new_addr, llvm_type):
            raise ParserException("Trying to redeclare variable '%s' at line %s" % (self.name, llvm_type))

        print('    ' * _indent + new_addr + " = " + opp + " " + llvm_type + " " + v0 + "," + v1, file=_file)


# Conditional expression node
class ASTNodeConditional(ASTNodeOp):
    def __init__(self):
        super().__init__("Conditional expression")

    # Simplify this node structure if possible
    def _reduce(self, symboltable):
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

                new_child = ASTNodeLiteral(int(new_val))
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
            new_child.type = INT
            # Insert child at front of children
            self.children.insert(0, new_child)

        self.delete()

    def print_llvm_ir_post(self, _type_table, _file=None, _indent=0, _string_list=None):
        v0 = self.children[0].load_if_necessary(_type_table, _file, _indent)
        v1 = self.children[1].load_if_necessary(_type_table, _file, _indent)
        t0 = self.children[0].get_llvm_type(_type_table)[0]
        t1 = self.children[1].get_llvm_type(_type_table)[0]
        new_var = convert_types(t0, t1, v0, v1, _file, _indent)
        v0 = new_var[0]
        v1 = new_var[1]
        llvm_type = new_var[2]

        opp = "icmp slt"
        if self.operators[0] == "==":
            opp = "icmp eq"
        elif self.operators[0] == "<":
            opp = "icmp slt"
        elif self.operators[0] == ">":
            opp = "icmp sgt"
        elif self.operators[0] == "!=":
            opp = "icmp ne"
        elif self.operators[0] == "<=":
            opp = "icmp sle"
        elif self.operators[0] == ">=":
            opp = "icmp sge"

        new_addr = self.get_llvm_addr()
        global last_label
        if self.operators[0] == "&&":
            new_addr1 = '%b' + new_addr[2:]
            new_addr2 = '%bb' + new_addr[3:]
            new_addr3 = '%bbb' + new_addr[4:]
            print('    ' * _indent + new_addr1 + " = icmp ne " + " " + llvm_type + " " + v0 + ", 0", file=_file)
            print('    ' * _indent + "br i1 " + new_addr1 + ", label %" + str(last_label + 1) + " " + ", label %" + str(
                last_label + 2), file=_file)
            print("; <label>:" + str(last_label + 1) + ":" + ' ' * 38 + "; preds = %" + str(last_label), file=_file)

            print('    ' * _indent + new_addr2 + " = icmp ne " + " " + llvm_type + " " + v1 + ", 0", file=_file)
            print('    ' * _indent + "br " + "label %" + str(last_label + 2) + " ", file=_file)
            print(
                "; <label>:" + str(last_label + 2) + ":" + ' ' * 38 + "; preds = %" + str(last_label + 1) + ", %" + str(
                    last_label), file=_file)

            print('    ' * _indent + new_addr3 + " = phi i1 [ false, %" + str(
                last_label) + "], [" + new_addr2 + ", %" + str(last_label + 1) + " ]", file=_file)
            convert_type('i1', llvm_type, new_addr3, _file, _indent, new_addr)

            last_label += 2

            if not _type_table.insert_variable(new_addr, llvm_type):
                raise ParserException("Trying to redeclare variable '%s' at line %s" % (self.name, llvm_type))

            return
        elif self.operators[0] == "||":
            new_addr1 = '%b' + new_addr[2:]
            new_addr2 = '%bb' + new_addr[3:]
            new_addr3 = '%bbb' + new_addr[4:]

            print('    ' * _indent + new_addr1 + " = icmp ne " + " " + llvm_type + " " + v0 + ", 0", file=_file)
            print('    ' * _indent + "br i1 " + new_addr1 + ", label %" + str(last_label + 2) + " " + ", label %" + str(
                last_label + 1), file=_file)
            print("; <label>:" + str(last_label + 1) + ":" + ' ' * 38 + "; preds = %" + str(last_label), file=_file)

            print('    ' * _indent + new_addr2 + " = icmp ne " + " " + llvm_type + " " + v1 + ", 0", file=_file)
            print('    ' * _indent + "br " + "label %" + str(last_label + 2) + " ", file=_file)
            print(
                "; <label>:" + str(last_label + 2) + ":" + ' ' * 38 + "; preds = %" + str(last_label + 1) + ", %" + str(
                    last_label), file=_file)

            print(
                '    ' * _indent + new_addr3 + " = phi i1 [ true, %" + str(last_label) + "], [" + new_addr2 + ", %" + str(
                    last_label + 1) + " ]", file=_file)
            convert_type('i1', llvm_type, new_addr3, _file, _indent, new_addr)

            last_label += 2

            if not _type_table.insert_variable(new_addr, llvm_type):
                raise ParserException("Trying to redeclare variable '%s' at line %s" % (self.name, llvm_type))

            return


        if not _type_table.insert_variable(new_addr, llvm_type):
            raise ParserException("Trying to redeclare variable '%s' at line %s" % (self.name, llvm_type))

        print('    ' * _indent + new_addr + " = " + opp + " " + llvm_type + " " + v0 + "," + v1, file=_file)


def convert_types(t0, t1, v0, v1, _file=None, _indent=0):
    llvm_type = 'i8'
    if t0 == 'i32' or t1 == 'i32':
        llvm_type = 'i32'
    if t0 == 'float' or t1 == 'float':
        llvm_type = 'float'

    v0 = convert_type(t0, llvm_type, v0, _file, _indent)
    v1 = convert_type(t1, llvm_type, v1, _file, _indent)

    return v0, v1, llvm_type


def convert_type(old_type, new_type, v1, _file=None, _indent=0, _save_as=None):
    if v1[0] != '%':
        if new_type == 'float':
            return double_to_hex(float(v1))
        if new_type == 'i8':
            return str(ord(v1))
        return v1
    if old_type != new_type:
        prev = str(v1)
        v1 = str(v1) + "conv"
        if _save_as:
            v1 = _save_as
        convopp = 'sitofp'
        if new_type == 'i32':
            convopp = 'sext'
            if old_type == 'float':
                convopp = 'fptosi'
            if old_type == 'i1':
                convopp = 'zext'

        if new_type == 'double':
            if old_type == 'float':
                convopp = 'fpext'

        print('    ' * _indent + v1 + " = " + convopp + " " + old_type + " " + prev + " to " + new_type, file=_file)

    return v1
