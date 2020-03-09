class TypeTable:
    def __init__(self):
        self.tables = list()

    def enter_scope(self):
        self.tables.append(dict())

    def leave_scope(self):
        if len(self.tables) != 0:
            self.tables.pop()

    def insert_variable(self, name, value_type, attribute):
        if name in self.tables[-1]:
            return False
        self.tables[-1][name] = Entry(value_type, attribute)
        return True

    def lookup_variable(self, name):
        for i in range(0, len(self.tables)):
            if name in self.tables[-i]:
                return self.tables[-i][name]
        return None


class Entry:
    def __init__(self, value_type, attribute):
        self.type = value_type
        self.attribute = attribute


if __name__ == "__main__":
    from Source.Types import *

    table = TypeTable()
    table.enter_scope()
    table.insert_variable("i", Int(5), None)
    print(table.lookup_variable("i"))
    print(table.lookup_variable("b"))
    table.enter_scope()
    table.insert_variable("b", Float(5.0), None)
    print(table.lookup_variable("i"))
    print(table.lookup_variable("b"))
    table.leave_scope()
