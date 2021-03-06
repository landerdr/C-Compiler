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

    def store_to_stack(self, register: str, type = None):
        """
        Stores value in register to stack
        :param register: location of value to be stored
        :return:
        """
        print("\taddiu $sp, $sp, -4", file=self.output)
        if type == FLOAT:
            print(f"\ts.s {register}, ($sp)", file=self.output)
            return
        if type == CHAR:
            print(f"\tsb {register}, ($sp)", file=self.output)
            return
        print(f"\tsw {register}, ($sp)", file=self.output)

    def update_on_stack(self, register: str, offset: int, type = None):
        """
        Updates value on the stack
        :param register: location of value to be stored
        :param offset: location of the value to be updated
        :return:
        """
        if type == FLOAT:
            print(f"\ts.s {register}, {offset}($fp)", file=self.output)
            return
        if type == CHAR:
            print(f"\tsb {register}, {offset}($fp)", file=self.output)
            return
        print(f"\tsw {register}, {offset}($fp)", file=self.output)

    def store_on_adress(self, register: str, adress: str, type = None):
            """
            Updates value on the stack
            :param register: location of value to be stored
            :param offset: location of the value to be updated
            :return:
            """
            if type == FLOAT:
                print(f"\ts.s {register}, {adress}", file=self.output)
                return
            if type == CHAR:
                print(f"\tsb {register}, {adress}", file=self.output)
                return
            print(f"\tsw {register}, {adress}", file=self.output)

    def unload_from_stack(self, register: str, offset: int, type = None):
        """
        Retrieves value from stack
        :param register: location to write value to
        :param offset: location of value on the stack
        :return:
        """
        if type == FLOAT:
            print(f"\tl.s {register}, {offset}($fp)", file=self.output)
            return
        if type == CHAR:
            print(f"\tlb {register}, {offset}($fp)", file=self.output)
            return
        print(f"\tlw {register}, {offset}($fp)", file=self.output)

    def unload_global(self, register: str, global_name: str, type = None):
        """
        Retrieves value from stack
        :param register: location to write value to
        :param offset: location of value on the stack
        :return:
        """
        if type == FLOAT:
            print(f"\tl.s {register}, {global_name}", file=self.output)
            return
        if type == CHAR:
            print(f"\tlb {register}, {global_name}", file=self.output)
            return
        print(f"\tlw {register}, {global_name}", file=self.output)

    def break_scope(self, offset: int):
        """
        Breaks down scope
        :param offset: amount of values in the scope
        :return:
        """
        print(f"\taddiu $sp, $sp, {offset}", file=self.output)

    def get_variable(self, variable_name: str, register: str):
        e = self.lookup_variable(variable_name)
        if self.is_global_variable(variable_name):
            print(e)
            if e.array:
                print("\tla " + register +  ", g_" + variable_name, file=self.output)
            else:
                self.unload_global(register, "g_" + variable_name, e.type)
        else:
            self.unload_from_stack(register, e.location, e.type)
        return e

    def set_variable(self, variable_name: str, register: str):
        e = self.lookup_variable(variable_name)
        self.update_on_stack(register, e.location, e.type)

    def mips_insert_variable(self, name: str, value_type, **kwargs):
        location = -(sum([len(x) for x in self.tables]) + 1) * 4
        #print("move $sp, $fp", file=self.output)
        if not kwargs.get("no_sp"):
            print("\taddiu $sp, $sp, -4", file=self.output)
        self.insert_variable(name, value_type, location=location, **kwargs)
