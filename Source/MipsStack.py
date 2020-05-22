class Stack:
    def __init__(self):
        pass

    def store_and_update_fp(self):
        """
        Call when entering a function
        :return:
        """
        print("addiu $sp, $sp, -4")
        print("sw $fp, ($sp)")
        print("move $fp, $sp")

    def unload_and_update_fp(self):
        """
        Call when exiting a function
        :return:
        """
        print("move $sp, $fp")
        print("lw $fp, ($sp)")
        print("addiu $sp, $sp, 4")

    def store_to_stack(self, register: str):
        """
        Stores value in register to stack
        :param register: location of value to be stored
        :return:
        """
        print("addiu $sp, $sp, -4")
        print(f"lw ${register}, ($sp)")

    def unload_from_stack(self, register: str, offset: int):
        """
        Retrieves value from stack
        :param register: location to write value to
        :param offset: location of value on the stack
        :return:
        """
        print(f"lw ${register} {offset}($fp)")

    def break_scope(self, amount: int):
        """
        Breaks down scope
        :param amount: amount of values in the scope
        :return:
        """
        print(f"addiu $sp, $sp, {amount * 4}")
