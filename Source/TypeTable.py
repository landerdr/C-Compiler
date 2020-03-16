from Source.Types import *


def _string_to_type(value_type):
    if value_type == "char":
        return Char()
    elif value_type == "int":
        return Int()
    elif value_type == "float":
        return Float()
    else:
        return value_type


class TypeTable:
    def __init__(self):
        self.tables = list()
        self.functions = dict()
        self.current = None
        self.param = dict()

    def enter_scope(self):
        self.tables.append(self.param)
        self.param = dict()

    def leave_scope(self):
        if len(self.tables) != 0:
            self.tables.pop()

    def insert_variable(self, name, value_type, **kwargs):
        if name in self.tables[-1]:
            return False
        self.tables[-1][name] = Entry(_string_to_type(value_type), **kwargs)
        return True

    def insert_param(self, name, value_type):
        if name in self.param:
            return False
        self.param[name] = Entry(_string_to_type(value_type))
        return True

    def lookup_variable(self, name):
        for i in range(1, len(self.tables) + 1):
            if name in self.tables[-i]:
                return self.tables[-i][name]
        return None

    def insert_function(self, name, value_type):
        if name in self.functions:
            return False
        self.current = name
        self.functions[name] = Entry(_string_to_type(value_type))

    def lookup_function(self, name):
        if name in self.functions:
            return self.functions[name]
        return None

    def __str__(self):
        str = ''
        for i in self.tables:
            str += i.__str__()
        return str


class Entry:
    def __init__(self, value_type, **kwargs):
        self.type = value_type

        self.pointer = kwargs.get("pointer") or False
        self.const = kwargs.get("const") or False

        # If value is passed set value, none otherwise
        self.value = kwargs.get("value")
        # If value is assigned, typecast to proper value
        if self.value is not None:
            self.update_value(self.value)
        # Location of variable in the register
        self.register = kwargs.get("register")
        # Location of variable on the stack (if applicable)
        self.location = kwargs.get("location")

    def update_value(self, new_value, line_num=""):
        # Support Unknown values
        if new_value == "Unknown":
            self.value = new_value
            return

        value_type = get_type(new_value)
        # TODO: check refactor possibilities (issubclass)
        if self.type < value_type:
            print("Warning: implicit conversion from %s to %s at line %s" % (value_type, self.type, line_num))
        self.value = self.type.cast(new_value)

    def __str__(self):
        return "Type: %s%s%s, Value: %s" % (
            "const " if self.const else "", str(self.type), "*" if self.pointer else "", str(self.value))

    def __repr__(self):
        return "Type: %s%s%s, Value: %s" % (
            "const " if self.const else "", str(self.type), "*" if self.pointer else "", str(self.value))


def get_type(val):
    if isinstance(val, float):
        return Float()
    if isinstance(val, int):
        return Int()
    if isinstance(val, str):
        return Char()


def get_dominant_type(val1, val2):
    if isinstance(val1, float) or isinstance(val2, float):
        return Float
    if isinstance(val1, int) or isinstance(val2, int):
        return Int
    if isinstance(val1, str) or isinstance(val2, str):
        return Char


# Found at https://stackoverflow.com/questions/23624212/how-to-convert-a-float-into-hex

import struct


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

    table.leave_scope()
    table.leave_scope()
