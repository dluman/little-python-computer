class Agent:

    def __init__(self, inputs, storage) -> None:
        self._inputs = inputs
        self._storage = storage
        self._program = tuple(storage._program)

    def step(self):
        cmd = self._program[self._storage._counter]
        self._storage._counter += 1
