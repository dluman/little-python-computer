import sys
import ast
import inspect

from functools import wraps
# Decoration functionality taken from the SO:
# https://stackoverflow.com/questions/3232024/introspection-to-get-decorator-names-on-a-method

# Use the following to retrieve the original names
# of wrapped functions:
# https://stackoverflow.com/questions/4887081/get-the-name-of-a-decorated-function

# Template decorators to characterize
# function signatures

# Bonus: this functionality is now codified in the graffito module:
# https://github.com/dluman/graffito

def generic(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not f.__name__.startswith("__b"):
            args[2]._counter += 1
        else:
            args[2]._spaces[99] = args[2]._counter + 1
        return f(*args, **kwargs)
    return wrapper

accumulate = generic
value = generic
storage = generic
control_flow = generic
inputs = generic
halt = generic
manipulate = generic

# Create introspection to retrieve
# decorators

def get_signature(cls):
    target = cls
    decorators = {}

    def visit_def(node):
        decorators[node.name] = []
        for n in node.decorator_list:
            name = None
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id
            decorators[node.name].append(name)

    visitor = ast.NodeVisitor()
    visitor.visit_FunctionDef = visit_def
    visitor.visit(ast.parse(inspect.getsource(target)))
    return decorators

class Commands:

    def __init__(self):
        self._syntax = {
            "1": self.__add,
            "2": self.__sub,
            "3": self.__sta,
            "4": self.__sft,
            "5": self.__lda,
            "6": self.__bra,
            "7": self.__brz,
            "8": self.__brp,
            "901": self.__inp,
            "902": self.__out,
            "0": self.__hlt
        }

    def parse(self, **kwargs):
        try:
            self._line = kwargs['line']
            self._arg = kwargs['arg'][0]
            self._val = int(kwargs['arg'][1:3])
        except KeyError:
            pass
        except:
            print(f"[ERROR] Invalid instruction at line {self._line}.")
        if self._arg == "9":
            self._arg = kwargs['arg']
        try:
            return self._syntax[self._arg]
        except:
            print(f"[ERROR] Invalid instruction at line {self._line}.")
            return

    @accumulate
    def __add(self, acc, storage) -> int:
        add = int(storage._spaces[self._val])
        acc.value += add

    @accumulate
    def __sub(self, acc, storage) -> int:
        sub = int(storage._spaces[self._val])
        acc.value -= sub

    @storage
    def __sta(self, acc, storage):
        storage._spaces[self._val] = str(acc.value)[-3:]

    @storage
    def __lda(self, acc, storage):
        acc.value = storage._spaces[self._val]

    @storage
    def __bra(self, acc, storage):
        storage._counter = self._val

    @storage
    def __brz(self, acc, storage):
        if acc.value == 0:
            storage._counter = self._val
        else:
            storage._counter += 1

    @storage
    def __brp(self, acc, storage):
        if acc.value > 0:
            storage._counter = self._val
        else:
            storage._counter += 1

    @manipulate
    def __sft(self, acc, storage):
        acc.value = str(acc.value).zfill(3)
        self._val = str(self._val).zfill(2)
        # Left shift first
        if int(self._val[0]) > 0:
            shifts = int(self._val[0])
            tmp = str(acc.value)
            for _ in range(shifts):
                tmp = f"{tmp}0"
            acc.value = tmp[-3:]
        # Right shift second
        if int(self._val[1]) > 0:
            shifts = int(self._val[1])
            tmp = str(acc.value)
            for _ in range(shifts):
                tmp = f"0{tmp}"
            acc.value = tmp[0:3]
        acc.value = int(acc.value)

    @inputs
    def __inp(self, acc, storage, input: int = 0):
        try:
            int(input)
            if input > 999:
                raise
        except:
            print("Invalid input.")
            sys.exit(1)
        acc.value = input

    def __out(self, acc, storage):
        print(acc.value)
        storage._counter += 1

    @halt
    def __hlt(self, acc, storage):
        sys.exit(0)
        return False
