"""Abstract Syntax Tree"""
from math import floor

from Source.MipsStack import *

# ToDo: add print_llvm_ir where necessary
# ToDo: make print_llvm_ir differentiate between data types
# ToDo: make print_llvm_it differentiate between operator types

last_label = 0
last_branch_choice = 0
ctr = 0


class AST:
    def __init__(self):
        self.root = None
        self.depthStack = []
        self.typeTable = TypeTable()

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
    def print_mips(self, _file_name=None):
        _file = open(_file_name, 'w+')

        type_table = MipsStack(_file)
        type_table.enter_scope()

        string_list = {}
        float_list = []

        prestack = [self.root]
        grey = []
        visited = []

        print("j c_main", file=_file)

        while len(prestack) > 0:
            item = prestack[-1]

            if isinstance(item, ASTNodeFunction) and item.fwd:
                visited.append(item)
                prestack.pop()
                continue

            # if entering this node for the first time -> print stuff
            if not (item in grey):
                grey.append(item)
                item.print_mips_pre(type_table, _file, len(type_table.tables), string_list, float_list)

            # check if a child hasn't been visited yet
            found = False
            children = item.children
            if isinstance(item, ASTNodeEqualityExpr):
                children = list(reversed(children))
            index = 0
            for i in range(len(children)):
                if not (children[i] in visited):
                    # prestack.append(item)
                    prestack.append(children[i])
                    index = i
                    found = True
                    break

            # no new nodes were found -> all children visited -> time to exit this node -> print stuff
            if not found:
                prestack.pop()
                item.print_mips_post(type_table, _file, len(type_table.tables), string_list, float_list)
                visited.append(item)
            else:
                if index != 0:
                    item.print_mips_in(type_table, index - 1, _file, len(type_table.tables), string_list, float_list)
        print("\n.data", file=_file)
        for i in string_list:
            for j in range(len(string_list[i])):
                print("\t" + i + "_" + str(j) + ": .asciiz " + "\"" + string_list[i][j] + "\"",
                      file=_file)


        print("\tflt: .float 0", file=_file)
        for i in range(0, len(float_list)):
            float_ref = "flt"
            float_ref += '_' + str(i)
            print("\t" + float_ref + ": .float " + str(float_list[i]),
                  file=_file)

        print(".text", file=_file)


'''Core'''


# Base node class
class ASTNode:
    def __init__(self, _val='Undefined'):
        global ctr
        ctr = ctr+1
        self.id = ctr
        self.canReplace = True
        self.parent = None
        self.index = 0
        self.children = []
        self.value = _val
        self.line_num = ""
        self.unreachable = False

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
    def _reduce(self, symboltable: TypeTable):
        pass

    # Constant folds (expects reduced node)
    def _const_folding(self):
        pass

    # Constant propagation (expects reduced node)
    def _const_propagation(self, symboltable: TypeTable):
        pass

    # Optimises this node structure if possible
    def optimise(self, symboltable: TypeTable, propagation=False):
        # Simplify tree structure (remove long lines)
        if len(self.children) == 1 and self.canReplace and self.parent is not None:
            self.delete()
        # Remove unreachable code
        # elif self.unreachable:
        #     self.parent.remove_child(self)
        #     self.parent = None
        #     self.children = []
        # Further optimisations
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
    def print_mips_pre(self, _type_table, _file=None, _indent=0, _string_list=None, _float_list = None):
        pass

    def print_mips_in(self, _type_table, prev_index=0, _file=None, _indent=0, _string_list=None,_float_list = None):
        pass

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        pass

    def get_id(self):
        return str(self.id)

    def _load(self, name, _type_table, _file=None, _indent=0, _target=None):
        v1 = "$t0"
        if _target:
            v1 = _target

        e = _type_table.get_variable(str(name), v1)
        return v1
        '''
        entry = self.get_llvm_type(_type_table, str(name))
        llvm_type = entry[0]
        pointer = entry[1]

        entry2 = _type_table.lookup_variable(str(name))

        if pointer != llvm_type:
            print("\tla" + "\t" + v1 + "," + str(entry2.location) + "($fp)" , file=_file)
            return v1

        if entry2.array == 0:
            if llvm_type == 'float':
                if not _target:
                    v1 = "$f1"
                print("\tl.s" + "\t" + v1 + "," + str(entry2.location) + "($fp)" , file=_file)
            else:

                print("\tlw" + "\t" + v1 + "," + str(entry2.location) + "($fp)" , file=_file)

        return v1
        '''

    def load_if_necessary(self, _type_table, _file=None, _indent=0, _target=None):
        if not _target:
            _target = "$t0"
        _type_table.get_variable(self.get_id(), _target)
        return _target

    def get_without_load(self, _type_table):
        return self.get_id()

    def get_llvm_type(self, _type_table, _var_name=None):
        if _var_name:
            entry = _type_table.lookup_variable(_var_name)
            return entry.type.get_llvm_type(), entry.type.get_llvm_type_ptr()
        entry = _type_table.lookup_variable(self.get_id())
        if isinstance(entry.type, str):
            return entry.type, entry.type
        else:
            return entry.type.get_llvm_type(), entry.type.get_llvm_type_ptr()


# Base Library node
class ASTNodeLib(ASTNode):
    def __init__(self):
        super().__init__("Lib")


# Base function declaration node
class ASTNodeFunction(ASTNode):
    def __init__(self):
        super().__init__("Function")
        # Indicates whether node can be replaced
        self.canReplace = False
        # Name of node, used for printing in llvm
        self.name = None
        # Type of node, used for quicker checking (uses child type)
        self.type = NONE
        # Forward declaration
        self.fwd = False
        # No clue - oli's stuff
        self.param_names = []

    def _reduce(self, symboltable: TypeTable):
        if self.fwd:
            symboltable.complete_function(fwd=True)

    def print_mips_pre(self, _type_table, _file=None, _indent=0, _string_list=None, _float_list = None):
        print("c_" + self.name + ":", file=_file)
        _type_table.insert_function(self.name, self.type)
        _indent += 1
        _type_table.enter_scope()

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):

        if len(self.children) > 0:
            if not isinstance(self.children[-1], ASTNodeReturn):
                if isinstance(self.children[-1], ASTNodeCompound):
                    if len(self.children[-1].children) > 0:
                        if not isinstance(self.children[-1].children[-1], ASTNodeReturn):
                            if self.name == "main":
                                print("\tli $v0,10", file=_file)
                                print("\tsyscall", file=_file)
                                return
                            v = convert_type('i32', self.type.get_llvm_type_ptr(), '0')
                            print("\tmovz	$31,$31,$0\n" +
                                  "\tjr	$31\n" +
                                  "\tnop\n", file=_file)
                    else:
                        v = convert_type('i32', self.type.get_llvm_type_ptr(), '0')
                        if self.name == "main":
                            print("\tli $v0,10", file=_file)
                            print("\tsyscall", file=_file)
                            return
                        print("\tli $2,$0")
                        print("\tmovz	$31,$31,$0\n" +
                              "\tjr	$31\n" +
                              "\tnop\n", file=_file)

                else:
                    v = convert_type('i32', self.type.get_llvm_type_ptr(), '0')
                    if self.name == "main":
                        print("\tli $v0,10", file=_file)
                        print("\tsyscall", file=_file)
                        return
                    print("\tli $2,$0")
                    print("\tmovz	$31,$31,$0\n" +
                          "\tjr	$31\n" +
                          "\tnop\n", file=_file)
        else:
            v = convert_type('i32', self.type.get_llvm_type_ptr(), '0')
            if self.name == "main":
                print("\tli $v0,10", file=_file)
                print("\tsyscall", file=_file)
                return
            print("\tli $2,$0")
            print("\tmovz	$31,$31,$0\n" +
                  "\tjr	$31\n" +
                  "\tnop\n", file=_file)

        _type_table.leave_scope()

    def print_mips_in(self, _type_table, prev_index=0, _file=None, _indent=0, _string_list=None,_float_list = None):
        if prev_index < len(self.children) - 2:
            pass
        else:
            _type_table.enter_scope()
            _indent += 1
            print("# Parameters", file=_file)
            for i in range(len(self.param_names)):
                if i >= 4:
                    return
                name = self.param_names[i][0]
                llvm_type = self.param_names[i][1].get_llvm_type_ptr()
                if (_type_table.offset == None):
                    _type_table.offset = 8
                else:
                    _type_table.offset += 4

                print("\tsw $"+ str(4+i)+  "," + str(_type_table.offset) + "($fp)", file=_file)


# Base list of parameters node
class ASTNodeParams(ASTNode):
    def __init__(self):
        super().__init__("Params")


# Single parameter node
class ASTNodeParam(ASTNode):
    def __init__(self):
        super().__init__("Param")
        # Name from parameter
        self.name = None
        # Type of parameter
        self.type = NONE
        # If parameter is const
        self.const = False
        self.array = None

    def _reduce(self, symboltable):
        if not symboltable.insert_param(self.name, self.type, const=self.const):
            raise ParserException("Trying to redeclare variable '%s' at line %s" % (self.name, self.line_num))

    def print_dot(self, _file=None):
        print('"', self, '"', '[label = "', self.value, ": param", self.name, '"]', file=_file)

    def print_mips_pre(self, _type_table, _file=None, _indent=0, _string_list=None, _float_list = None):
        if self.array is not None:
            self.type = Pointer(self.type)
        t = self.type

        _type_table.insert_param(self.name, t, register=str("%" + self.name), const=self.const)
        if isinstance(self.parent, ASTNodeFunction):
            self.parent.param_names.append([self.name, t])
        else:
            self.parent.parent.param_names.append([self.name, t])


class ASTNodeLeftValue(ASTNode):
    def __init__(self):
        super().__init__("Left Value")
        self.name = ""
        self.type = NONE

    def _reduce(self, symboltable):
        entry = symboltable.lookup_variable(self.name)
        if not entry:
            raise ParserException("Non declared variable '%s' at line %s" % (self.name, self.line_num))
        self.type = entry.type

    def print_dot(self, _file=None):
        print('"', self, '"', '[label = "', self.value, ":", self.name, '"]', file=_file)

    def get_without_load(self, _type_table):
        entry = _type_table.lookup_variable(str(self.name))
        if entry:
            if entry.register:
                return entry.register
        return '%' + str(self.name)

    def get_llvm_type(self, _type_table, _var_name=None):
        entry = _type_table.lookup_variable(self.name)
        if isinstance(entry.type, str):
            return entry.type, entry.type
        else:
            return entry.type.get_llvm_type(), entry.type.get_llvm_type_ptr()

    def load_if_necessary(self, _type_table, _file=None, _indent=0, _target=None):
        return self._load(self.name, _type_table, _file, _indent, _target)


class ASTNodeInclude(ASTNode):

    def __init__(self):
        super().__init__("Include")
        self.name = ""

    def _reduce(self, symboltable: TypeTable):
        if self.name != 'stdio.h':
            raise ParserException("No file named %s" % self.name)

    def print_mips_pre(self, _type_table, _file=None, _indent=0, _string_list=None, _float_list = None):
        if self.name == 'stdio.h':
            #print("\ndeclare i32 @printf(i8*, ...) #1", file=_file)
            #print("declare i32 @__isoc99_scanf(i8*, ...) #1\n", file=_file)
            _type_table.insert_function('printf', 'i32')
            _type_table.insert_function('scanf', 'i32')


'''Statements'''


# Base statement node
class ASTNodeStatement(ASTNode):
    def __init__(self, _val="Statement"):
        super().__init__(_val)


# Break statement node
class ASTNodeBreak(ASTNodeStatement):
    def __init__(self):
        super().__init__("Break")

    def _reduce(self, symboltable: TypeTable):
        node = self
        while not isinstance(node, ASTNodeLoopStatement) and node is not None:
            node = node.parent

        if node is None:
            raise ParserException("Continue statement outside loop at line %s" % self.line_num)

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        node = self
        while not isinstance(node, ASTNodeLoopStatement) and node is not None:
            node = node.parent

        if node is None:
            raise ParserException("Continue statement outside loop at line %s" % self.line_num)

        print("\tj " + node.label3, file=_file)


# Continue statement node
class ASTNodeContinue(ASTNodeStatement):
    def __init__(self):
        super().__init__("Continue")

    def _reduce(self, symboltable: TypeTable):
        node = self
        while not isinstance(node, ASTNodeLoopStatement) and node is not None:
            node = node.parent

        if node is None:
            raise ParserException("Continue statement outside loop at line %s" % self.line_num)

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        node = self
        while not isinstance(node, ASTNodeLoopStatement) and node is not None:
            node = node.parent

        if node is None:
            raise ParserException("Continue statement outside loop at line %s" % self.line_num)

        print("\tj " + node.label_continue, file=_file)


# Base expression statement node
class ASTNodeExpressionStatement(ASTNodeStatement):
    def __init__(self, _val="Expression statement"):
        super().__init__(_val)


# Compound statement node
class ASTNodeCompound(ASTNodeStatement):
    def __init__(self, _val="Compound statement"):
        super().__init__(_val)

    def print_mips_pre(self, _type_table, _file=None, _indent=0, _string_list=None, _float_list = None):
        if isinstance(self.parent, ASTNodeFunction):
            return
        _type_table.enter_scope()

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        if isinstance(self.parent, ASTNodeFunction):
            return
        _type_table.leave_scope()


# Definition statement node
class ASTNodeDefinition(ASTNodeStatement):
    def __init__(self):
        self.init__ = super().__init__("Definition")
        self.canReplace = False
        self.type = None
        self.name = None
        self.const = False
        self.array = None

    # Print dot format name and label
    def print_dot(self, _file=None):
        print('"', self, '"', '[label = "', self.value, ":", self.name, self.type, '"]', file=_file)

    def _reduce(self, symboltable):
        value = None
        # If no children -> not defined
        if len(self.children) == 0:
            # If pointer, ignore
            if self.type.pointertype != NONE or self.array:
                value = "Unknown"
            elif self.const:
                raise ParserException("Non defined const variable at line %s" % self.line_num)
        # If value is known, assign value
        elif isinstance(self.children[0], ASTNodeLiteral) and self.children[0].isConst:
            value = self.children[0].value
            if self.children[0].type == CHAR:
                value = chr(value)
        elif isinstance(self.children[0], ASTNodeEqualityExpr):
            entry = symboltable.lookup_variable(self.children[0].get_name())
            value = entry.value
            if entry.type == CHAR:
                value = chr(value)
        elif not compatible_types(self.type, self.children[0].type):
            raise ParserException("Trying to assign incompatible types at line %s" % self.line_num)
        else:
            value = "Unknown"
            if self.type < self.children[0].type:
                print("Warning: implicit conversion from '%s' to '%s' at line %s" % (
                    self.children[0].type, self.type, self.line_num))

        if not symboltable.insert_variable(self.name, self.type, value=value, const=self.const,
                                           line_num=self.line_num, array=self.array):
            raise ParserException("Trying to redeclare variable '%s' at line %s" % (self.name, self.line_num))

    # TODO: Update: use of new functions
    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):

        llvm_type = self.type.get_llvm_type()
        allign = '4'
        if self.type.pointertype != NONE:
            llvm_type = self.type.get_llvm_type_ptr()
            allign = '8'
        if self.array == -1:
            self.array = len(self.children[0].children)
        print_type = llvm_type
        if self.array != None:
            print_type = '[ ' + str(self.array) + ' x ' + llvm_type + ']'
        register = "%var_" + self.name + "_" + self.get_id()[1:]
        if len(_type_table.tables) == 1:
            register = "@" + self.name
            if len(self.children) > 0:
                v1 = self.children[0].get_without_load(_type_table)
                t1 = self.children[0].get_llvm_type(_type_table)[0]
                v1 = convert_type(t1, llvm_type, v1, _file, _indent)
            else:
                print(register + "= common global " + print_type + "zeroinitializer, align 4", file=_file)
                _type_table.insert_variable(self.name, self.type, const=self.const, register=register, array=self.array)
                return
        if _type_table.offset == None:
            _type_table.offset = 8
        else:
            _type_table.offset += 4
        _type_table.mips_insert_variable(self.name, self.type)

        if len(_type_table.tables) == 1:
            print("# Global", file=_file)
            print(".data", file=_file)
            print("\t" + register[1:] + ":", file=_file, end="")
            if self.type == CHAR:
                if v1 == 0 or v1 == "$0":
                    print("\t.space	1",file=_file)
                else:
                    print("\t.byte	" + v1 + "\n",file=_file)
            else:
                if v1 == 0 or v1 == "$0":
                    print("\t.space	4",file=_file)
                else:
                    print("\t.word	" + v1,file=_file)

            print(".text\n", file=_file)
            return

        if len(self.children) > 0:
            if not isinstance(self.children[0], ASTNodeList):
                print("# Var Definition",  self.name, file=_file)
                v1 = self.children[0].load_if_necessary(_type_table, _file, _indent)
                t1 = self.children[0].get_llvm_type(_type_table)[1]
                v1 = convert_type(t1, llvm_type, v1, _file, _indent)
                _type_table.set_variable(self.name, v1)

            else:
                prev = None
                for index in range(int(self.array)):
                    if index < len(self.children[0].children):
                        k = self.children[0].children[index]
                        v1 = k.load_if_necessary(_type_table, _file, _indent)
                        t1 = k.get_llvm_type(_type_table)[1]
                        v1 = convert_type(t1, llvm_type, v1, _file, _indent)
                        new_addr = k.get_id() + '_listitem'
                    else:
                        v1 = '0'
                        t1 = "i32"
                        new_addr = self.children[0].get_id() + '_listitem_' + str(index)
                        v1 = convert_type(t1, llvm_type, v1, _file, _indent)

                    if index == 0:
                        print("    " * _indent + new_addr + " =  getelementptr inbounds [" + str(
                            self.array) + " x " + llvm_type + "], [" + str(
                            self.array) + " x " + llvm_type + "]*" + register + ", i64 0, i64 " + str(index),
                              file=_file)
                    else:
                        print(
                            "    " * _indent + new_addr + " =  getelementptr inbounds " + llvm_type + ", " + llvm_type + "* " + prev + ", i64 1",
                            file=_file)
                    if _type_table.offset == None:
                        _type_table.offset = 8
                    else:
                        _type_table.offset += 4
                    _type_table.set_variable(self.name, "$2")
                    #print("sw      $2," + str(_type_table.offset) + "($fp)", file=_file)
                    prev = new_addr


# If statement node
class ASTNodeIf(ASTNodeStatement):
    def __init__(self):
        super().__init__("If statement")
        self.Condition = None
        self.body = None
        self.label1 = None
        self.label2 = None
        self.label3 = None

    def print_mips_in(self, _type_table, prev_index=0, _file=None, _indent=0, _string_list=None,_float_list = None):
        if prev_index == 0:
            v0 = self.children[0].load_if_necessary(_type_table, _file, _indent)
            t0 = self.children[0].get_llvm_type(_type_table)[0]
            v0 = convert_type(t0, 'i1', v0, _file, _indent)
            llvm_type = 'i1'
            new_addr = self.get_id()
            new_addr1 = "$t0"
            self.label1 = "label_" + self.get_id() + "_1"
            self.label2 = "label_" + self.get_id() + "_2"
            self.label3 = self.label2
            icmp = 'icmp ne'
            if llvm_type == 'float' or llvm_type == 'double':
                icmp = 'fcmp une'

            print('\t' + "beq " + new_addr1 + ", 1" + ", " + str(self.label1), file=_file)
            print('\t' + "j " + str(self.label2) , file=_file)
            print("\n " + self.label1 + ":", file=_file)

        if prev_index == 1:
            self.label3 = "label_" + self.get_id() + "_3"
            print('\t' + "j " + str(self.label3) , file=_file)
            print("\n " + str(self.label2) + ":", file=_file)

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        print('\t' + "j " + str(self.label3) , file=_file)
        print("\n " + str(self.label3) + ":", file=_file)


# Loop statement node
class ASTNodeLoopStatement(ASTNodeStatement):
    def __init__(self):
        super().__init__("Loop statement")
        self.loop_type = None
        self.Condition = None
        self.body = None
        self.label1 = "label_" + self.get_id() + "_1"
        self.label2 = "label_" + self.get_id() + "_2"
        self.label3 = "label_" + self.get_id() + "_3"
        self.label_continue = self.label1

    def print_mips_pre(self, _type_table, _file=None, _indent=0, _string_list=None, _float_list = None):
        _type_table.enter_scope()
        if self.loop_type == 'do':
            self.label3 = self.label2
        if self.loop_type == 'while' or self.loop_type == 'do':
            print('\tj ' + str(self.label1), file=_file)
            print("\n " + self.label1 + ":", file=_file)
        if self.loop_type == 'for':
            self.label_continue = "label_" + self.get_id()[1:] + "continue"
            temp = self.children[3]
            self.replace_child(3, self.children[2])
            self.replace_child(2, temp)

    def print_mips_in(self, _type_table, prev_index=0, _file=None, _indent=0, _string_list=None,_float_list = None):
        if prev_index == 0 and self.loop_type == 'for':
            print('\tj ' + str(self.label1), file=_file)
            print("\n " + self.label1 + ":", file=_file)
        if (prev_index == 0 and self.loop_type == 'while') or (prev_index == 1 and self.loop_type == 'for'):
            v0 = self.children[prev_index].load_if_necessary(_type_table, _file, _indent)
            t0 = self.children[prev_index].get_llvm_type(_type_table)[prev_index]
            v0 = convert_type(t0, 'bool', v0, _file, _indent)

            print('\tbeq ' + v0 + ', 1, ' + self.label2, file=_file)
            print('\tj ' + self.label3, file=_file)
            print("\n " + self.label2 + ":", file=_file)

        if prev_index == 2 and self.loop_type == 'for':
            print("\tj " + str(self.label_continue), file=_file)
            print("\n " + self.label_continue + ":", file=_file)

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        if self.loop_type == 'do':
            v0 = self.children[1].load_if_necessary(_type_table, _file, _indent)
            t0 = self.children[1].get_llvm_type(_type_table)[1]
            v0 = convert_type(t0, 'bool', v0, _file, _indent)

            print('\tbeq ' + v0 + ', 1, ' + self.label1, file=_file)
            print('\tj ' + self.label2, file=_file)

            print("\n " + self.label2 + ":", file=_file)
            _type_table.leave_scope()
            return

        print('\tj ' + str(self.label1), file=_file)
        print("\n " + str(self.label3) + ":", file=_file)


# Return statement node
class ASTNodeReturn(ASTNodeStatement):
    def __init__(self):
        super().__init__("Return statement")
        self.canReplace = False

    def _reduce(self, symboltable: TypeTable):
        entry = symboltable.get_current_function()
        if entry is None:
            raise ParserException("Invalid location of 'return' at line %s" % self.line_num)
        if entry.type == VOID and len(self.children) != 0 or len(self.children) == 0 and entry.type != VOID:
            raise ParserException("Invalid return statement for type '%s' at line %s" % (entry.type, self.line_num))
        if len(self.children) != 0 and not compatible_types(entry.type, self.children[0].type):
            raise ParserException("Invalid return statement for type '%s' and type '%s' at line %s" % (
                entry.type, self.children[0].type, self.line_num))

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        new_val = ''
        entry = _type_table.lookup_function(_type_table.current)
        if _type_table.current == "main":
            print("\tli $v0,10", file=_file)
            print("\tsyscall", file=_file)
            return
        llvm_type = entry.type.get_llvm_type_ptr()
        if len(self.children):
            rval = self.children[0].load_if_necessary(_type_table, _file, _indent)
            new_val = convert_type(self.children[0].get_llvm_type(_type_table)[1], llvm_type, rval, _file, _indent)
        print("\tmovz	$31,$31,$0\n" +
              "\tmove	$sp,$fp\n" +
              "\tlw	$fp,20($sp)\n" +
              "\taddiu	$sp,$sp,24\n" +
              "\tjr	$31\n" +
              "\tnop\n" , file=_file)


'''Expressions'''


# Base expression node
class ASTNodeExpression(ASTNode):
    def __init__(self, val="Expression"):
        super().__init__(val)
        # To support typechecking when const propagation is disabled
        self.type = NONE


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
        self.prop_able = False
        self.stringRef = None
        self.floatRef = None
        self.isString = False

    def _const_propagation(self, symboltable):
        if not self.isConst:
            # Lookup variable in type table
            entry = symboltable.lookup_variable(str(self.value))
            if entry.value != "Unknown":
                # Replace with value from symboltable
                replacement = ASTNodeLiteral(entry.value)
                replacement.isConst = True
                replacement.type = entry.type
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
            if not self.prop_able:
                entry.update_value("Unknown")
            self.type = entry.type
        else:
            self.value = self.type.cast(self.value)

    def print_mips_pre(self, _type_table, _file=None, _indent=0, _string_list=None, _float_list = None):
        if self.isString:
            self.stringRef = "str_" + str(len(_string_list))
            import re
            strs = re.split('%d|%s|%f|%c',self.value)
            #strs = self.value.split("%d")
            _string_list[self.stringRef] = strs

        if self.type == FLOAT and self.isConst:
            float_ref = "flt_" + str(len(_float_list))
            self.floatRef = float_ref
            _float_list.append(self.value)

    def get_without_load(self, _type_table):
        if not self.isConst:
            return '%' + str(self.value)
        else:
            if self.stringRef:
                return self.stringRef
            return str(self.value)

    def get_llvm_type(self, _type_table, _var_name=None):
        if not self.isConst:
            entry = _type_table.lookup_variable(str(self.value))
            return entry.type.get_llvm_type(), entry.type.get_llvm_type_ptr()
        else:
            if self.isString:
                return 'i8', 'i8*'
            return self.type.get_llvm_type(), self.type.get_llvm_type_ptr()

    def load_if_necessary(self, _type_table, _file=None, _indent=0, _target=None):
        if not self.isConst:
            return self._load(self.value, _type_table, _file, _indent, _target)
        else:
            if self.type == FLOAT:
                if not _target:
                    _target = "$f1"
                print("\tl.s\t" + _target + "," + str(self.floatRef), file=_file )
                return _target
            if not _target:
                _target = "$t0"

            if self.stringRef:
                print("\tla\t" + _target + "," + str(self.stringRef) + "_0", file=_file )
                return _target
            print("\tli\t" + _target + "," + str(self.value), file=_file )
            return _target



# Postcrement expression node (In/Decrement behind var)
class ASTNodePostcrement(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Post in/decrement")
        self.canReplace = False
        self.operator = None

    def _const_propagation(self, symboltable):
        if isinstance(self.children[0], ASTNodeLeftValue):
            entry = symboltable.lookup_variable(self.children[0].name)

            if entry.value == "Unknown":
                return

            new_child = ASTNodeLiteral(entry.value)
            new_child.parent = self
            new_child.isConst = True
            new_child.type = entry.type
            self.children = [new_child]
            self.delete()

            if self.operator == "++":
                entry.value += 1
            elif self.operator == "--":
                entry.value -= 1

    def _reduce(self, symboltable):
        # ToDo: move to Left_Value??
        if isinstance(self.children[0], ASTNodeLeftValue):
            entry = symboltable.lookup_variable(self.children[0].name)
            if not entry:
                raise ParserException("Non declared variable '%s' at line %s" % (self.children[0].name, self.line_num))
            if entry.value is None:
                raise ParserException("Non defined variable '%s' at line %s" % (self.children[0].name, self.line_num))
            if entry.const:
                raise ParserException(
                    "Incompatible operation '%s' with type const type at line %s" % (self.operator, self.line_num))
            self.type = entry.type

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        v0 = self.children[0].load_if_necessary(_type_table, _file, _indent, self.get_id())
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

        self.type = string_to_type(llvm_type)

        new_addr = self.get_id()
        _type_table.insert_variable(new_addr, llvm_type)
        var_name = self.children[0].get_without_load(_type_table)

        print('    ' * _indent + new_addr + "t = " + opp + " " + llvm_type + " " + v0 + "," + v1, file=_file)
        print(
            '    ' * _indent + "store " + llvm_type + " " + new_addr + "t, " + llvm_type + "* " + var_name
            + ", align 4 ", file=_file)


# Precrement expression node (In/Decrement in front of var)
class ASTNodePrecrement(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Pre in/decrement")
        self.canReplace = False
        self.operator = None

    def _const_propagation(self, symboltable):
        if isinstance(self.children[0], ASTNodeLeftValue):
            entry = symboltable.lookup_variable(self.children[0].name)
            if entry.value == "Unknown":
                return

            if self.operator == "++":
                entry.value += 1
            elif self.operator == "--":
                entry.value -= 1

            new_child = ASTNodeLiteral(entry.value)
            new_child.parent = self
            new_child.isConst = True
            new_child.type = entry.type
            self.children = [new_child]
            self.delete()

    def _reduce(self, symboltable):
        # ToDo: move to Left_Value??
        if isinstance(self.children[0], ASTNodeLeftValue):
            entry = symboltable.lookup_variable(self.children[0].name)
            if not entry:
                raise ParserException("Non declared variable '%s' at line %s" % (self.children[0].name, self.line_num))
            if entry.value is None:
                raise ParserException("Non defined variable '%s' at line %s" % (self.children[0].name, self.line_num))
            if entry.const:
                raise ParserException(
                    "Incompatible operation '%s' with type const type at line %s" % (self.operator, self.line_num))
            self.type = entry.type

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        v0 = self.children[0].load_if_necessary(_type_table, _file, _indent)
        t0 = self.children[0].get_llvm_type(_type_table)[0]

        new_var = convert_types(t0, 'i8', v0, '1', _file, _indent)
        v0 = new_var[0]
        v1 = new_var[1]
        llvm_type = new_var[2]

        self.type = string_to_type(llvm_type)

        opp = "add"
        if llvm_type == 'float':
            opp = 'fadd'
        if self.operator == '--':
            opp = 'sub'
            if llvm_type == 'float':
                opp = 'fsub'

        new_addr = self.get_id()
        _type_table.insert_variable(new_addr, llvm_type)
        var_name = self.children[0].get_without_load(_type_table)

        '''
        entry = _type_table.lookup_variable(var_name)
        print(var_name)
        if entry.register:
            var_name = entry.register
        '''


        print('    ' * _indent + new_addr + " = " + opp + " " + llvm_type + " " + v0 + "," + v1, file=_file)
        print(
            '    ' * _indent + "store " + llvm_type + " " + new_addr + ", " + llvm_type + "* " + var_name
            + ", align 4 ", file=_file)


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
        if not isinstance(self.children[0], ASTNodeLeftValue):
            return
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
            self.type = entry.type
            if self.equality == "=":
                if child.type == CHAR:
                    value = chr(value)
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
            if not compatible_types(entry.type, child.type):
                raise ParserException("Trying to assign incompatible types at line %s" % self.line_num)
            value = "Unknown"
            if entry.type < child.type:
                print("Warning: implicit conversion from '%s' to '%s' at line %s" % (
                    entry.type, child.type, self.line_num))
        entry.update_value(value, self.line_num)

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        v1 = self.children[1].load_if_necessary(_type_table, _file, _indent)
        if not isinstance(self.children[0], ASTNodeLeftValue):
            if not isinstance(self.children[0], ASTNodeIndexingExpr):
                var_name = self.children[0].children[0].get_id()[1:]
                entry = _type_table.lookup_variable(self.children[0].get_id())
            else:
                var_name = self.children[0].get_id()[1:]
                entry = _type_table.lookup_variable(self.children[0].get_id())
        else:
            var_name = self.get_name()
            entry = _type_table.lookup_variable(var_name)
        llvm_type = entry.type.get_llvm_type_ptr()
        t1 = self.children[1].type.get_llvm_type()

        if self.equality != "=":

            if t1 == 'float' and isinstance(self.children[1], ASTNodeLiteral):
                t1 = 'double'

            new_v1 = self.get_id()
            v0 = self.children[0].load_if_necessary(_type_table, _file, _indent)
            converted = convert_types(llvm_type, t1, v0, v1, _file, _indent)

            v0 = converted[0]
            v1 = converted[1]
            t1 = converted[2]

            opp = 'add'
            if t1 == 'double' or t1 == 'float':
                opp = 'fadd'
            if self.equality == "-=":
                opp = "sub"
                if t1 == 'double' or t1 == 'float':
                    opp = 'fsub'
            if self.equality == "/=":
                opp = 'sdiv'
                if t1 == 'double' or t1 == 'float':
                    opp = 'fdiv'
            if self.equality == "*=":
                opp = 'mul'
                if t1 == 'double' or t1 == 'float':
                    opp = 'fmul'
            if self.equality == "%=":
                opp = 'srem'
                if t1 == 'double' or t1 == 'float':
                    raise ModuloException('Trying to use modulo on float type')

            print('    ' * _indent + new_v1 + " = " + opp + " " + t1 + " " + v0 + ", " + v1, file=_file)
            v1 = new_v1
        if t1 == "float":
            v1 = "$f1"
        v1 = convert_type(t1, llvm_type, v1, _file, _indent)
        _type_table.set_variable(var_name, v1)
        '''
        if llvm_type == "float":
            print("\tswc1 ", v1 + "," + str(entry.location) + "($sp)", file=_file)
        else:
            print("\tsw ", v1 + "," + str(entry.location) + "($sp)", file=_file)
        '''

    def print_mips_pre(self, _type_table, _file=None, _indent=0, _string_list=None, _float_list = None):
        print("# Equality expression (" + str(self.children[0]) + self.equality + ")", file=_file)

    def get_without_load(self, _type_table):
        entry = _type_table.lookup_variable(str(self.children[0].name))
        if entry:
            if entry.register:
                return entry.register
        return '%' + str(self.children[0].name)

    def get_llvm_type(self, _type_table, _var_name=None):
        entry = _type_table.lookup_variable(self.children[0].name)
        if isinstance(entry.type, str):
            return entry.type, entry.type
        else:
            return entry.type.get_llvm_type(), entry.type.get_llvm_type_ptr()

    def load_if_necessary(self, _type_table, _file=None, _indent=0, _target=None):
        if self.equality == '=':
            return self._load(self.children[0].name, _type_table, _file, _indent, _target)
        else:
            return self.get_id()


# Function call expression node
class ASTNodeFunctionCallExpr(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Function call expression")
        self.name = None
        self.canReplace = False

    def _reduce(self, symboltable):
        if self.name == "printf" or self.name == "scanf":
            self.type = VOID
            return
        entry = symboltable.lookup_function(self.name)
        if entry is None:
            raise ParserException("No function named '%s' at line %s" % (self.name, self.line_num))
        if len(entry.param) != len(self.children):
            raise ParserException("Invalid amount of param for function '%s' at line %s" % (self.name, self.line_num))
        self.type = entry.type

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        if self.name == 'printf':
            print("# Printf " + str(self.children[0].type), file=_file)
            if (self.children[0].stringRef):
                sl = []
                ss = "str_0"
                for i in _string_list:
                    if i == self.children[0].stringRef:
                        sl = _string_list[i]
                        ss = i
                        break
                for i in range(len(sl)):
                    print("\tli $v0, 4", file=_file)
                    print("\tla $a0," + ss + "_" + str(i), file=_file)
                    print("\tsyscall", file=_file)
                    j = i + 1
                    if j >= len(self.children):
                        continue

                    target = "$t0"
                    if self.children[j].type == FLOAT:
                        target = "$f1"
                    value = self.children[j].load_if_necessary(_type_table, _file, _indent, target)

                    if self.children[j].type.pointertype == CHAR:
                        print("\tli $v0, 4", file=_file)
                        print("\tmove $a0," + str(value), file=_file)
                    elif self.children[j].type == FLOAT:
                        print("\tli $v0, 2", file=_file)
                        print("\tmov.s $f12," + str(value), file=_file)
                    elif self.children[j].type == CHAR:
                        print("\tli $v0, 11", file=_file)
                        print("\tmove $a0," + str(value), file=_file)
                    else:
                        print("\tli $v0, 1", file=_file)
                        print("\tmove $a0," + str(value), file=_file)
                    print("\tsyscall", file=_file)
            else:
                target = "$t0"
                if self.children[0].type == FLOAT:
                    target = "$f1"
                value = self.children[0].load_if_necessary(_type_table, _file, _indent, target)

                if self.children[0].type.pointertype == CHAR:
                    print("\tli $v0, 4", file=_file)
                    print("\tmove $a0," + str(value), file=_file)
                elif self.children[0].type == FLOAT:
                    print("\tli $v0, 2", file=_file)
                    print("\tmov.s $f12," + str(value), file=_file)
                elif self.children[0].type == CHAR:
                    print("\tli $v0, 11", file=_file)
                    print("\tmove $a0," + str(value), file=_file)
                else:
                    print("\tli $v0, 1", file=_file)
                    print("\tmove $a0," + str(value), file=_file)
                print("\tsyscall", file=_file)

        elif self.name == 'scanf':
            print("# Scanf " + str(self.children[0].type), file=_file)
            if self.children[1].type == FLOAT:
                print("\tli $v0,6", file=_file)
                print("\tsyscall", file=_file)
                print("\tmov.s $f1,$f0", file=_file)
                if len(self.children) > 0:
                    entry = _type_table.lookup_variable(str(self.children[-1].value))
                    print("\tswc1 $f1," + str(entry.location) + "($sp)", file=_file)
            else:
                print("\tli $v0,5", file=_file)
                print("\tsyscall", file=_file)
                print("\tmove $t0,$v0", file=_file)
                if len(self.children) > 0:
                    entry = _type_table.lookup_variable(str(self.children[-1].value))
                    print("\tsw $t0," + str(entry.location) + "($sp)", file=_file)



        else:
            i = len(self.children) - 1
            while i >= 0:
                value = self.children[i].load_if_necessary(_type_table, _file, _indent, "$" +str(4 + i))
                i = i - 1

            print("\tjal c_" + self.name, file=_file)

            #_type_table.insert_variable(self.get_llvm_addr(), entry.type)


# Indexing expression node
class ASTNodeIndexingExpr(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Indexing expression")
        self.canReplace = False
        self.value = None

    def _reduce(self, symboltable: TypeTable):
        if self.value:
            entry = symboltable.lookup_variable(self.value)
            self.type = entry.type
            if not entry.is_array():
                raise ParserException("Invalid operation '[]' on type '%s' at line %s" % (self.type, self.line_num))
            if not self.children[-1].type < FLOAT:
                raise ParserException("Invalid operation type for indexing operation %s at line %s" % (
                    self.children[-1].type, self.line_num))

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        self.type = self.children[0].type
        if self.value:
            entry = _type_table.lookup_variable(self.value)
            register = entry.register
            l = entry.array
            llvm_type = entry.type.get_llvm_type_ptr()
            index = str(self.children[0].load_if_necessary(_type_table, _file, _indent))
            t1 = self.children[0].get_llvm_type(_type_table)[1]
        else:
            register = str(self.children[0].load_if_necessary(_type_table, _file, _indent))
            entry = _type_table.lookup_variable(register)
            if not entry:
                entry = _type_table.lookup_variable_register(register[1:])
            l = entry.array
            llvm_type = entry.type.get_llvm_type_ptr()
            index = str(self.children[1].load_if_necessary(_type_table, _file, _indent))
            t1 = self.children[1].get_llvm_type(_type_table)[1]

        v1 = convert_type(t1, 'i64', index, _file, _indent)

        new_addr = self.get_id()
        arr = str(entry.type.get_llvm_type() + ", " + llvm_type)
        ind = ''
        if int(l) > 0:
            ind = 'i64 0,'
            arr = "[" + str(l) + " x " + llvm_type + "], [" + str(l) + " x " + llvm_type + "]*"
        print(
            "    " * _indent + new_addr + " =  getelementptr inbounds " + arr + ' ' + register + ", " + ind + " i64 " + v1,
            file=_file)

        _type_table.insert_variable(new_addr, entry.type.get_llvm_type())

    def load_if_necessary(self, _type_table, _file=None, _indent=0, _target=None):
        return self._load(self.get_id(), _type_table, _file, _indent, self.get_id() + "_l")


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

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        v0 = self.children[0].load_if_necessary(_type_table, _file, _indent)
        t0 = self.children[0].get_llvm_type(_type_table)[1]
        v1 = convert_type('i32', str(t0), '0', _file, _indent)

        llvm_type = 'i1'
        opp = "xor"
        icmp = 'icmp ne '
        if str(t0) == 'float' or t0 == 'double':
            opp = 'xor'
            icmp = 'fcmp une '

        new_addr = self.get_id()
        if not _type_table.insert_variable(new_addr, llvm_type):
            raise ParserException("Trying to redeclare variable '%s'" % new_addr)
        print('    ' * _indent + v0 + 't = ' + icmp + t0 + ' ' + v0 + ', ' + v1, file=_file)
        print('    ' * _indent + new_addr + " = " + opp + " " + llvm_type + " " + v0 + "t , true", file=_file)


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

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        v0 = self.children[0].load_if_necessary(_type_table, _file, _indent)
        v1 = '0'
        t0 = self.children[0].get_llvm_type(_type_table)[1]
        t1 = 'i8'
        new_var = convert_types(t0, t1, v0, v1, _file, _indent)
        v0 = new_var[0]
        v1 = new_var[1]
        llvm_type = new_var[2]
        opp = "sub"
        if llvm_type == 'float':
            opp = 'fsub'

        new_addr = self.get_id()
        if not _type_table.insert_variable(new_addr, llvm_type):
            raise ParserException("Trying to redeclare variable '%s'" % new_addr)

        print('    ' * _indent + new_addr + " = " + opp + " " + llvm_type + " " + v1 + "," + v0, file=_file)


# Reference expression node
class ASTNodeReference(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Reference expression")
        self.canReplace = False

    def _const_propagation(self, symboltable):
        entry = symboltable.lookup_variable(self.children[0].name)
        entry.value = "Unknown"

    def _reduce(self, symboltable):
        self.type = Pointer(self.children[0].type)
        entry = symboltable.lookup_variable(self.children[0].name)
        entry.value = "Unknown"

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        child = self.children[0]
        new_addr = self.get_id()
        llvm_type = child.get_llvm_type(_type_table)[1]
        _type_table.insert_variable(new_addr, Pointer(string_to_type(llvm_type)))

    def get_id(self):
        return self.children[0].get_id()

    def load_if_necessary(self, _type_table, _file=None, _indent=0, _target=None):
        return self.children[0].get_without_load(_type_table)


# Dereference expression node
class ASTNodeDereference(ASTNodeUnaryExpr):
    def __init__(self):
        super().__init__("Dereference expression")
        self.canReplace = False

    def _reduce(self, symboltable):
        self.type = self.children[0].type.pointertype
        if self.type == NONE:
            raise ParserException("Trying to dereference non pointer value at line %s" % self.line_num)

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):

        child = self.children[0]
        new_addr = self.get_id()
        entry = child.get_llvm_type(_type_table)
        llvm_type = entry[1]
        v0 = child.load_if_necessary(_type_table, _file, _indent)

        _type_table.insert_variable(new_addr, llvm_type[:-1])

        if isinstance(self.parent, ASTNodeEqualityExpr):
            if self.parent.children[0] == self and self.parent.equality == '=':
                return

        print('    ' * _indent + new_addr + " = load " + llvm_type[:-1] + ", " + llvm_type + " " +
              v0 + ", align 4", file=_file)

    def get_without_load(self, _type_table):
        return self.children[0].get_id()


class ASTNodeList(ASTNodeUnaryExpr):
    def __init__(self, tt="list"):
        super().__init__(tt)
        self.operators = []
        self.canReplace = False


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

            if not compatible_types(left.type,
                                    right.type) or left.type.pointertype != BaseType() or right.type.pointertype != BaseType():
                raise ParserException("Invalid operation '%s' on types %s and %s at line %s" % (
                    opp, left.type, right.type, self.line_num))

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

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        v0 = self.children[0].load_if_necessary(_type_table, _file, _indent, "$t0")
        v1 = self.children[1].load_if_necessary(_type_table, _file, _indent, "$t1")
        t0 = self.children[0].get_llvm_type(_type_table)[1]
        t1 = self.children[1].get_llvm_type(_type_table)[1]
        new_var = convert_types(t0, t1, v0, v1, _file, _indent)
        v0 = new_var[0]
        v1 = new_var[1]
        llvm_type = new_var[2]

        opp = "addu"
        if llvm_type == 'float':
            opp = 'add.s'
        if self.operators[0] == '-':
            opp = 'sub'
            if llvm_type == 'float':
                opp = 'sub.s'

        new_addr = "$t0"
        self.type = string_to_type(llvm_type)
        #_type_table.insert_variable(new_addr, llvm_type)
        print('\t' + opp + " " + new_addr + "," + v0 + "," + v1, file=_file)
        _type_table.mips_insert_variable(self.get_id(), self.type)
        _type_table.set_variable(self.get_id(), new_addr)
        #print('    ' * _indent + new_addr + " = " + opp + " " + llvm_type + " " + v0 + "," + v1, file=_file)


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

            if not compatible_types(left.type,
                                    right.type) or left.type.pointertype != BaseType() or right.type.pointertype != BaseType():
                raise ParserException("Invalid operation '%s' on types %s and %s at line %s" % (
                    opp, left.type, right.type, self.line_num))

            # Simplify if possible
            if isinstance(left, ASTNodeLiteral) and isinstance(right,
                                                               ASTNodeLiteral) and left.isConst and right.isConst:
                value_type = get_dominant_type(left.type, right.type)
                if opp == "*":
                    new_val = left.value * right.value
                elif opp == "/":
                    if right.value == 0:
                        raise ParserException("Division by zero at line %s" % self.line_num)
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

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):

        t0 = self.children[0].get_llvm_type(_type_table)[1]
        t1 = self.children[1].get_llvm_type(_type_table)[1]

        if t0 == "float":
            v0 = self.children[0].load_if_necessary(_type_table, _file, _indent, "$f1")
        else:
            v0 = self.children[0].load_if_necessary(_type_table, _file, _indent, "$t0")

        if t1 == "float":
            v1 = self.children[1].load_if_necessary(_type_table, _file, _indent, "$f2")
        else:
            v1 = self.children[1].load_if_necessary(_type_table, _file, _indent, "$t1")

        new_var = convert_types(t0, t1, v0, v1, _file, _indent)
        v0 = new_var[0]
        v1 = new_var[1]
        llvm_type = new_var[2]

        new_addr = "$t0"
        opp = "mul"
        if llvm_type == 'float':
            opp = 'mul.s'
            new_addr = "$f1"
        if self.operators[0] == '/':
            opp = 'div'
            if llvm_type == 'float':
                opp = 'div.s'

        elif self.operators[0] == '%':
            if llvm_type == 'float':
                raise ModuloException('Trying to use modulo on float type')
            print('\t' + "div" + " " + new_addr + "," + v0 + "," + v1, file=_file)
            print('\t' + "mfhi " + new_addr, file=_file)
            _type_table.mips_insert_variable(self.get_id(), self.type)
            _type_table.set_variable(self.get_id(), new_addr)
            return

        print('\t' + opp + " " + new_addr + "," + v0 + "," + v1, file=_file)
        _type_table.mips_insert_variable(self.get_id(), self.type)
        _type_table.set_variable(self.get_id(), new_addr)


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

            if not compatible_types(left.type,
                                    right.type) or left.type.pointertype != BaseType() or right.type.pointertype != BaseType():
                raise ParserException("Invalid operation '%s' on types %s and %s at line %s" % (
                    opp, left.type, right.type, self.line_num))

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
                    new_val = left.value > 0 and right.value > 0
                elif opp == "||":
                    new_val = left.value > 0 or right.value > 0
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

    def print_mips_post(self, _type_table, _file=None, _indent=0, _string_list=None,_float_list = None):
        print("# Conditional", file=_file)
        t0 = self.children[0].get_llvm_type(_type_table)[1]
        r0 = "$t0"
        if t0 == "float":
            r0 = "$f1"
        t1 = self.children[1].get_llvm_type(_type_table)[1]
        r1 = "$t1"
        if t1 == "float":
            r1 = "$f2"
        v0 = self.children[0].load_if_necessary(_type_table, _file, _indent, r0)
        v1 = self.children[1].load_if_necessary(_type_table, _file, _indent, r1)

        llvm_type = "bool"

        if self.operators[0] != "&&" and self.operators[0] != "||":
            new_var = convert_types(t0, t1, v0, v1, _file, _indent)
            v0 = new_var[0]
            v1 = new_var[1]
            llvm_type = new_var[2]
        else:
            v0 = convert_type(t0, "bool", v0, _file, _indent, "$t0")
            v1 = convert_type(t1, "bool", v1, _file, _indent, "$t1")

        inverse = False

        opp = "slt"
        if self.operators[0] == "==":
            opp = "seq"
            if llvm_type == 'float' or llvm_type == 'double':
                opp = 'c.eq.s'
        elif self.operators[0] == "<":
            opp = "slt"
            if llvm_type == 'float' or llvm_type == 'double':
                opp = 'c.lt.s'
        elif self.operators[0] == ">":
            opp = "sgt"
            if llvm_type == 'float' or llvm_type == 'double':
                opp = 'c.le.s'
                inverse = True
        elif self.operators[0] == "!=":
            opp = "sne"
            if llvm_type == 'float' or llvm_type == 'double':
                opp = 'c.ne.s'
        elif self.operators[0] == "<=":
            opp = "sle"
            if llvm_type == 'float' or llvm_type == 'double':
                opp = 'c.le.s'
        elif self.operators[0] == ">=":
            opp = "sge"
            if llvm_type == 'float' or llvm_type == 'double':
                opp = 'c.lt.s'
                inverse = True
        elif self.operators[0] == "&&":
            opp = "and"
        elif self.operators[0] == "||":
            opp = "or"
        new_addr = "$t0"

        if llvm_type == 'float' or llvm_type == 'double':

            br_name = 'eq_' + self.get_id()
            print('\tli ' + new_addr + ", " + str(int(not inverse)), file=_file)
            print('\t' + opp + " " + " " + v0 + "," + v1, file=_file)
            print('\tbc1t ' + br_name, file=_file)
            print('\tli ' + new_addr + ", " + str(int(inverse)), file=_file)
            print( br_name + ":", file=_file)
        else:
            print('\t' + opp + " " + new_addr + ", " + v0 + "," + v1, file=_file)
        _type_table.mips_insert_variable(self.get_id(), self.type)
        _type_table.set_variable(self.get_id(), new_addr)


def convert_types(t0, t1, v0, v1, _file=None, _indent=0):
    llvm_type = 'bool'
    if t0 == 'i32' or t1 == 'i32' or t0 == 'int' or t1 == 'int':
        llvm_type = 'i32'
    if t0 == 'float' or t1 == 'float':
        llvm_type = 'float'
    if t0 == 'double' or t1 == 'double':
        llvm_type = 'double'
    v0_conv = v0
    v1_conv = v1
    if llvm_type == "float":
        v0_conv = "$f1"
    if llvm_type == "float":
        v1_conv = "$f2"

    v0 = convert_type(t0, llvm_type, v0, _file, _indent, v0_conv )
    v1 = convert_type(t1, llvm_type, v1, _file, _indent, v1_conv )
    return v0, v1, llvm_type


def convert_type(old_type, new_type, v1, _file=None, _indent=0, _save_as=None):
    if new_type == 'void' :
        return ''
    if old_type != new_type:
        if new_type == "float":
            if not _save_as:
                _save_as = "$f1"
            #print("# Int to float", file=_file)
            print("\tmtc1 " + v1 + "," + _save_as, file=_file)
            print("\tcvt.s.w " + _save_as + "," + _save_as, file=_file)
            return _save_as
        if new_type == "i32":
            if not _save_as:
                _save_as = "$t0"
            #print("# Float to int", file=_file)
            print("\tcvt.w.s " + v1 + "," + v1, file=_file)
            print("\tmfc1 " + _save_as + "," + v1 , file=_file)
            return _save_as
        if new_type == "bool" or new_type == "i1":
            if old_type == "float":
                global  last_label
                last_label = last_label + 1
                if not _save_as:
                    _save_as = "$f3"
                br_name = 'conv_' + str(last_label)
                print('\tli ' + _save_as + ", 0", file=_file)
                print('\tl.s $f3, flt', file=_file)
                print('\tc.le.s ' + " " + v1 + ", $f3", file=_file)
                print('\tbc1t ' + br_name, file=_file)
                print('\tli ' + _save_as + ", 1", file=_file)
                print( br_name + ":", file=_file)
            else:
                if not _save_as:
                    _save_as = "$t0"
                print("\tsgt " + _save_as + ", " + v1, ", 0", file=_file)
            return _save_as

    if old_type[-1] == '*' or new_type[-1] == '*' or v1[0] == "$":
        return v1

    return v1
