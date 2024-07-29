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

def generic(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if f.__name__ not in ["__inp","__bra", "__brz", "__brp"]:
            args[2]._counter += 1
        elif f.__name__.startswith("__b"):
            print("branch!")
        return f(*args, **kwargs)
    return wrapper

accumulate = generic
value = generic
storage = generic
control_flow = generic
inputs = generic

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
            if kwargs['arg'] == None:
                self._syntax[0]()
            self._arg = kwargs['arg'][0]
            self._val = int(kwargs['arg'][1:3])
        except KeyError:
            pass
        if self._arg == "9":
            self._arg = kwargs['arg']
        try:
            return self._syntax[self._arg]
        except:
            return

    @accumulate
    def __add(self, acc, storage) -> int:
        add = storage._spaces[self._val]
        acc._value += add

    @accumulate
    def __sub(self, acc, storage) -> int:
        sub = storage._spaces[self._val]
        acc._value -= sub

    @storage
    def __sta(self, acc, storage):
        storage._spaces[self._val] = acc._value

    @storage
    def __lda(self, acc, storage):
        acc._value = storage._spaces[self._val]

    @storage
    def __bra(self):
        pass

    @storage
    def __brz(self):
        pass

    @storage
    def __brp(self):
        pass

    @inputs
    def __inp(self, acc, input: int = 0):
        print(f"[CMD] Saving {input} to accumulator...")
        acc._value = input

    def __out(self):
        pass

    def __hlt(self):
        sys.exit(0)
