from Source.Types import *
import struct

NONE = BaseType()
VOID = VoidType()
BOOL = Bool()
CHAR = Char()
INT = Int()
FLOAT = Float()
STRING = Pointer(CHAR)


class ParserException(Exception):
    pass


class ModuloException(Exception):
    pass


def encap_pointers(value_type, pointer_count):
    for i in range(pointer_count):
        value_type = Pointer(value_type)
    return value_type


def string_to_type(value_type):
    pointers = 0
    if not isinstance(value_type, str):
        return value_type
    while value_type[-1] == '*':
        value_type = value_type[:-1]
        pointers += 1
    if value_type == "bool" or value_type == "i1":
        return encap_pointers(BOOL, pointers)
    elif value_type == "char" or value_type == "i8":
        return encap_pointers(CHAR, pointers)
    elif value_type == "int" or value_type == "i32":
        return encap_pointers(INT, pointers)
    elif value_type == "float":
        return encap_pointers(FLOAT, pointers)
    elif value_type == 'void':
        return encap_pointers(VOID, pointers)
    else:
        return value_type


class TypeTable:
    def __init__(self):
        self.tables = list()
        self.functions = dict()
        self.function_scope = False
        self.current = None
        self.param = dict()
        self.offset = 0

    def complete_function(self, fwd=False):
        self.function_scope = False
        if self.current is not None:
            current = self.functions[self.current]
            if current.defined and not fwd:
                raise ParserException("Trying to redefine function '%s'" % self.current)
            current.defined |= not fwd
            params = list(self.param.values())
            if current.param is None:
                current.param = params
            elif str(params) != str(current.param):
                raise ParserException("Function parameter signature doesn't match for function '%s'" % self.current)
        self.param = dict()

    def enter_scope(self):
        self.tables.append(self.param)
        if self.function_scope:
            self.complete_function()
        else:
            self.param = dict()

    def leave_scope(self):
        if len(self.tables) != 0:
            for key in self.tables[-1]:
                if key[0] == '%':
                    continue
                if self.tables[-1][key].usage_count == 0:
                    print("Warning: Unused variable '%s'" % key)
            self.tables.pop()

    def insert_variable(self, name: str, value_type, **kwargs):
        if name in self.tables[-1]:
            return False
        self.tables[-1][name] = Entry(string_to_type(value_type), **kwargs)
        return True

    def insert_param(self, name: str, value_type, **kwargs):
        if name in self.param:
            return False
        self.param[name] = Entry(string_to_type(value_type), **kwargs)
        self.param[name].update_value("Unknown")
        return True

    def lookup_variable(self, name: str):
        for i in range(1, len(self.tables) + 1):
            if name in self.tables[-i]:
                self.tables[-i][name].usage_count += 1
                return self.tables[-i][name]
        return None

    def is_global_variable(self, name: str):
        for i in range(1, len(self.tables) + 1):
            if name in self.tables[-i]:
                #self.tables[-i][name].usage_count += 1
                if i == len(self.tables):
                    return True
                return False
        return False

    def lookup_variable_register(self, register: str):
        for i in range(1, len(self.tables) + 1):
            for j in self.tables[-i]:
                if self.tables[-i][j].register == register:
                    self.tables[-i][j].usage_count += 1
                    return self.tables[-i][j]
        return None

    def insert_function(self, name: str, value_type, **kwargs):
        self.current = name
        self.function_scope = True
        self.offset = None

        function = Entry(string_to_type(value_type), **kwargs)
        if name in self.functions:
            if function.type != self.functions[name].type:
                raise ParserException("Trying to redeclare function '%s' with mismatched signature type" % name)
        else:
            self.functions[name] = function

    def lookup_function(self, name: str):
        if name in self.functions:
            return self.functions[name]
        return None

    def get_current_function(self):
        if self.current is not None:
            return self.lookup_function(self.current)
        return None

    def __str__(self):
        str = ''
        for i in self.tables:
            str += i.__str__()
        return str


class Entry:
    def __init__(self, value_type: BaseType, **kwargs):
        self.type = value_type
        if kwargs.get("pointer"):
            self.type = Pointer(self.type)

        self.const = kwargs.get("const") or False

        self.line_num = kwargs.get("line_num")
        self.usage_count = 0

        # If value is passed set value, none otherwise
        self.value = kwargs.get("value")
        # If value is assigned, typecast to proper value
        if self.value is not None:
            self.update_value(self.value, self.line_num)
        # Location of variable in the register
        self.register = kwargs.get("register")
        # Location of variable on the stack (if applicable)
        self.location = kwargs.get("location")

        self.param = None
        self.defined = False

        self.array = kwargs.get("array") or 0

    def update_value(self, new_value, line_num=""):
        # Support Unknown values
        if new_value == "Unknown":
            self.value = new_value
            return

        value_type = get_type(new_value)
        if self.type < value_type:
            print("Warning: implicit conversion from '%s' to '%s' at line %s" % (value_type, self.type, line_num))
        self.value = self.type.cast(new_value)

    def is_array(self):
        return not self.array == 0

    def __str__(self):
        return "Type: %s%s, Value: %s" % (
            "const " if self.const else "", str(self.type), str(self.value))

    def __repr__(self):
        return "Type: %s%s, Value: %s" % (
            "const " if self.const else "", str(self.type), str(self.value))


def get_type(val):
    if isinstance(val, float):
        return FLOAT
    if isinstance(val, int):
        return INT
    if isinstance(val, str):
        if len(val) == 1:
            return CHAR
        return STRING
    if isinstance(val, bool):
        return Bool


def compatible_types(type1, type2):
    return type1 <= type2 or type1 >= type2


def get_dominant_type(type1, type2):
    return max(type1, type2)


# Found at https://stackoverflow.com/questions/23624212/how-to-convert-a-float-into-hex


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


def double_to_hex(f):
    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])


if __name__ == "__main__":
    table = TypeTable()
    table.enter_scope()
    table.insert_variable("i", "int", value=5)
    print(table.lookup_variable("i"))
    print(table.lookup_variable("b"))
    table.enter_scope()
    table.insert_variable("b", "float", value=3.0)
    print(table.lookup_variable("i"))
    b = table.lookup_variable("b")
    print(b)
    b.update_value(5)
    print(table.lookup_variable("b"))

    print(get_dominant_type(INT, FLOAT))
    print(compatible_types(Pointer(INT), INT))
    print(get_dominant_type(Pointer(CHAR), Pointer(CHAR)))

    table.leave_scope()
    table.leave_scope()
