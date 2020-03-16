class Char:
    def __init__(self):
        self.rank = 0

    def __lt__(self, other):
        return self.rank < other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __ge__(self, other):
        return self.rank >= other.rank

    def cast(self, value):
        return chr(value)

    def __str__(self):
        return "Char"

    def __repr__(self):
        return "Char"


class Int(Char):
    def __init__(self):
        super().__init__()
        self.rank = 1

    def cast(self, value):
        return int(value)

    def __str__(self):
        return "Int"

    def __repr__(self):
        return "Int"


class Float(Int):
    def __init__(self):
        super().__init__()
        self.rank = 2

    def cast(self, value):
        return float(value)

    def __str__(self):
        return "Float"

    def __repr__(self):
        return "Float"