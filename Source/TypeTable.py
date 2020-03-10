class TypeTable:
    def __init__(self):
        self.tables = list()

    def enter_scope(self):
        self.tables.append(dict())

    def leave_scope(self):
        if len(self.tables) != 0:
            self.tables.pop()

    def insert_variable(self, name, value_type, value, attribute):
        if name in self.tables[-1]:
            return False
        if value_type == "char":
            self.tables[-1][name] = Entry(chr, value, attribute)
        elif value_type == "int":
            self.tables[-1][name] = Entry(int, value, attribute)
        elif value_type == "float":
            self.tables[-1][name] = Entry(float, value, attribute)
        else:
            self.tables[-1][name] = Entry(value_type, value, attribute)
        return True

    def lookup_variable(self, name):
        for i in range(0, len(self.tables)):
            if name in self.tables[-i]:
                return self.tables[-i][name]
        return None

    def insert_function(self, name, parameters, value_type):
        key = tuple(name) + tuple(parameters)
        if len(self.tables) != 1:
            return False
        if key in self.tables[-1]:
            return False
        self.tables[-1][key] = Entry(value_type, None, None)
        return True

    def lookup_function(self, name, parameters):
        key = tuple(name) + tuple(parameters)
        return self.lookup_variable(key)


class Entry:
    def __init__(self, value_type, value, attribute):
        self.type = value_type
        self.value = value
        self.attribute = attribute

    def update_value(self, new_value):
        if not isinstance(new_value, self.type):
            print("Mismatched types")
        self.value = new_value


if __name__ == "__main__":
    table = TypeTable()
    table.enter_scope()
    table.insert_variable("i", int, 5, None)
    print(table.lookup_variable("i"))
    print(table.lookup_variable("b"))
    table.enter_scope()
    table.insert_variable("b", float, 3.0, None)
    print(table.lookup_variable("i"))
    b = table.lookup_variable("b")
    print(b, b.value)
    b.update_value(5)
    print(table.lookup_variable("b").value)

    table.leave_scope()
    table.insert_function("f", [int, int, chr], int)
    print(table.lookup_function("f", [int, int, chr]))
    table.leave_scope()
