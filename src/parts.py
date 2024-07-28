from collections import deque

class Storage:

    def __init__(self, instructions):
        self._program = (instruction for instruction in instructions)
        self._counter = 0
        self.__initialize_storage()

    def __initialize_storage(self):
        # This implementation follows the accepted solution from SO:
        # https://stackoverflow.com/questions/5944708/how-can-i-automatically-limit-the-length-of-a-list-as-new-elements-are-added
        self._spaces = deque(maxlen=100)
        for _ in range(100):
            self._spaces.append(None)

class Accumulator:

    def __init__(self):
        self._value = 0

class Inputs:

    def __init__(self, inputs):
        self._values = list(inputs)
