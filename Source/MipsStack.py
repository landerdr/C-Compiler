import sys
from Source.TypeTable import *


class MipsStack(TypeTable):
    def __init__(self, output=sys.stdout):
        super().__init__()
        self.output = output

    def store_and_update_fp(self):
        """
        Call when entering a function
        :return:
        """
        print("\taddiu $sp, $sp, -4", file=self.output)
        print("\tsw $fp, ($sp)", file=self.output)
        print("\tmove $fp, $sp", file=self.output)

    def unload_and_update_fp(self):
        """
        Call when exiting a function
        :return:
        """
        print("\tmove $sp, $fp", file=self.output)
        print("\tlw $fp, ($sp)", file=self.output)
        print("\taddiu $sp, $sp, 4", file=self.output)

    def store_to_stack(self, register: str):
        """
        Stores value in register to stack
        :param register: location of value to be stored
        :return:
        """
        print("\taddiu $sp, $sp, -4", file=self.output)
        print(f"\tsw ${register}, ($sp)", file=self.output)

    def update_on_stack(self, register: str, offset: int):
        """
        Updates value on the stack
        :param register: location of value to be stored
        :param offset: location of the value to be updated
        :return:
        """
        print(f"\tsw ${register}, {offset}($fp)", file=self.output)

    def unload_from_stack(self, register: str, offset: int):
        """
        Retrieves value from stack
        :param register: location to write value to
        :param offset: location of value on the stack
        :return:
        """
        print(f"\tlw ${register}, {offset}($fp)", file=self.output)

    def break_scope(self, offset: int):
        """
        Breaks down scope
        :param offset: amount of values in the scope
        :return:
        """
        print(f"\taddiu $sp, $sp, {offset}", file=self.output)

    def get_variable(self, variable_name: str, register: str):
        e = self.lookup_variable(variable_name)
        self.unload_from_stack(register, e.location)

    def set_variable(self, variable_name: str, register: str):
        e = self.lookup_variable(variable_name)
        self.update_on_stack(register, e.location)

    def mips_insert_variable(self, name: str, value_type, **kwargs):
        location = -(sum([len(x) for x in self.tables]) + 1) * 4
        self.insert_variable(name, value_type, location=location, **kwargs)
