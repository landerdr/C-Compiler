class BaseType:
    def __init__(self):
        self.pointertype = None

    def __lt__(self, other):
        return self <= other and not self == other

    def __le__(self, other):
        return issubclass(type(other), type(self))

    def __eq__(self, other):
        return type(self) == type(other)

    def __gt__(self, other):
        return self >= other and not self == other

    def __ge__(self, other):
        return issubclass(type(self), type(other))

    def cast(self, value):
        return None

    def __str__(self):
        return "NoneType"

    def __repr__(self):
        return "NoneType"

    def __bool__(self):
        return False

    def get_llvm_type(self):
        return 'NoneType'

    def get_llvm_type_ptr(self):
        return "NoneType"


class VoidType(BaseType):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Void"

    def __repr__(self):
        return "Void"

    def get_llvm_type(self):
        return 'void'

    def get_llvm_type_ptr(self):
        return "void"


class Bool(BaseType):
    def __init__(self):
        super().__init__()
        self.pointertype = BaseType()

    def cast(self, value):
        return bool(value)

    def __str__(self):
        return "Bool"

    def __repr__(self):
        return "Bool"

    def get_llvm_type(self):
        return 'i1'

    def get_llvm_type_ptr(self):
        return 'i1'

    def __bool__(self):
        return True


class Char(Bool):
    def __init__(self):
        super().__init__()
        self.pointertype = BaseType()

    # TODO: fix char to not be int
    def cast(self, value):
        if isinstance(value, int):
            return value
        return ord(value)

    def __str__(self):
        return "Char"

    def __repr__(self):
        return "Char"

    def get_llvm_type(self):
        return 'i8'

    def get_llvm_type_ptr(self):
        return 'i8'

    def __bool__(self):
        return True


class Int(Char):
    def __init__(self):
        super().__init__()

    def cast(self, value):
        return int(value)

    def __str__(self):
        return "Int"

    def __repr__(self):
        return "Int"

    def get_llvm_type(self):
        return 'i32'

    def get_llvm_type_ptr(self):
        return 'i32'


class Float(Int):
    def __init__(self):
        super().__init__()

    def cast(self, value):
        return float(value)

    def __str__(self):
        return "Float"

    def __repr__(self):
        return "Float"

    def get_llvm_type(self):
        return 'float'

    def get_llvm_type_ptr(self):
        return 'float'


class Pointer(Int):
    def __init__(self, pointertype):
        super().__init__()
        self.pointertype = pointertype

    def cast(self, value):
        return value

    def __eq__(self, other):
        return type(self) == type(other) and self.pointertype == other.pointertype

    def __lt__(self, other):
        return self <= other and not self == other

    def __le__(self, other):
        return issubclass(type(other), type(self)) and self.pointertype <= other.pointertype

    def __gt__(self, other):
        return self >= other and not self == other

    def __ge__(self, other):
        return issubclass(type(self), type(other)) and self.pointertype >= other.pointertype

    def __str__(self):
        return "%s*" % self.pointertype

    def __repr__(self):
        return "%s*" % self.pointertype

    def get_llvm_type(self):
        return self.pointertype.get_llvm_type()

    def get_llvm_type_ptr(self):
        return self.pointertype.get_llvm_type_ptr() + '*'

