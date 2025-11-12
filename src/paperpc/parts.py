import re
import sys
from collections import deque

class Storage:

    def __init__(self, instructions, config):
        # Split into line numbers and instructions using the 2+ spaces
        # rule to define separation between lines, instructions, comments
        self._counter = 1
        self.stack = []
        # Sensible defaults based on the new paper version; this hella
        # violates pylint
        self.stack_base = config.storage["stack_base"] if "stack_base" in config.storage else 80
        self.stack_size = config.storage["stack_size"] if "stack_size" in config.storage else 18
        self.storage_size = config.storage["memory_size"] if "memory_size" in config.storage else 60
        self.stack_ptr = self.stack_base
        self._program = list(
            re.split(
                r"\s{2,}|\t{1,}",
                instruction
            ) for instruction in instructions)
        # Apparently, must initialize storage here; if we wait until the
        # end of the constructor, the program is...blank?
        self._expected_inputs = len([
            instruction for instruction
            in self._program if instruction[1] == "901"
        ])
        self.__initialize_storage()

    def __initialize_storage(self):
        # This implementation follows the accepted solution from
        # SO question no. 5944708
        line = 1
        self._spaces = deque(maxlen = self.storage_size)
        for _ in range(self.storage_size):
            self._spaces.append(None)
        for instruction in self._program:
            self._spaces[int(instruction[0])] = instruction[1]
            try:
                comment = str(instruction[2])
                if not comment.startswith("@"):
                    raise
            except IndexError:
                # Comment isn't there, so ignore
                pass
            except:
                print(comment)
                print(f"[LINE {line}] Invalid comment format: not prefaced by '@'")
                sys.exit(1)
            line += 1
        self._spaces[0] = "001"

    def retrieve(self, addr):
        if self._spaces[addr] == None:
            print(f"[ERROR] Program ends abruptly at line {addr}. Did you meant to HALT?")
            sys.exit(1)
        return self._spaces[addr]

class Accumulator:

    def __init__(self):
        self._value = 0
        self._carry= 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value = int(value)
        self._value = int(self._value)
        if self._value < 0:
            self._value = 0
        if self._value > 9999:
            print("[ERROR] ACCUMULATOR OVERFLOW!")
            sys.exit(1)
        if self._value >= 1000:
            self._carry = str(self.value)[0]
        self._value = value

    @value.getter
    def value(self):
        return self._value

class Inputs:

    def __init__(self, inputs):
        try:
            if type(inputs) == int:
                inputs = [inputs]
            if type(inputs) == str:
                inputs = [
                    int(inp) for inp
                    in inputs.split(",").strip()
                ]
            self._values = list(inputs)
        except TypeError:
            print("[ERROR] Program expects inputs, but none given.")
            sys.exit(1)
