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
        return f(*args, **kwargs)
    return wrapper

accumulate = generic
value = generic
storage = generic
flow = generic

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
            arg = kwargs['arg'][0]
            val = kwargs['arg'][1:3]
        except KeyError:
            pass
        if arg == "9":
            arg = kwargs['arg']
        try:
            return self._syntax[arg]
        except:
            return

    @accumulate
    def __add(self, acc, add) -> int:
        return acc + add

    @accumulate
    def __sub(self, acc, sub) -> int:
        return self.__add(acc, -1 * sub)

    @storage
    def __sta(self, addr):
        pass

    @storage
    def __lda(self, addr):
        pass

    @storage
    def __bra(self):
        pass

    @storage
    def __brz(self):
        pass

    @storage
    def __brp(self):
        pass

    def __inp(self):
        pass

    def __out(self):
        pass

    def __hlt(self):
        sys.exit(0)
