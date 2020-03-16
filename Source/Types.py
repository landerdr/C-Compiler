class Char:
    def __init__(self, pointer=False, const=False):
        self.pointer = pointer
        self.const = const


class Int(Char):
    pass


class Float(Int):
    pass
