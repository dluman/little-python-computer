class Storage:

    def __init__(self, instructions):
        self._program = (instruction for instruction in instructions)
        self._counter = 0

class Accumulator:

    def __init__(self):
        self._value = 0

class Inputs:

    def __init__(self, inputs):
        self._inputs = inputs
