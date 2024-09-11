import re
import sys
from collections import deque

class Storage:

    def __init__(self, instructions):
        # Split into line numbers and instructions using the 2+ spaces
        # rule to define separation between lines, instructions, comments
        self._counter = 1
        self._program = (
            re.split(
                r"\s{2,}|\t{1,}",
                instruction
            ) for instruction in instructions)
        self._expected_inputs = 0
        self.__initialize_storage()

    def __initialize_storage(self):
        # This implementation follows the accepted solution from SO:
        # https://stackoverflow.com/questions/5944708/how-can-i-automatically-limit-the-length-of-a-list-as-new-elements-are-added
        line = 1
        self._spaces = deque(maxlen=100)
        for _ in range(100):
            self._spaces.append(None)
        for instruction in self._program:
            self._spaces[int(instruction[0])] = instruction[1]
            #if instruction[1] == "901":
            #    self._expected_inputs += 1
            try:
                comment = str(instruction[2])
                if not comment.startswith("@"):
                    raise
            except IndexError:
                # Comment isn't there, so ignore
                pass
            except:
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
        if type(inputs) == int:
            inputs = [inputs]
        self._values = list(inputs)
