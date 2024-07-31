import sys

from .parts import *
from .cmd import *
from arglite import parser as cliarg

def main() -> None:

    # Load instruction set, crash out
    # if set does not exist as file
    try:
        src = sys.argv[1]
    except:
        print("Invalid source file.")
        sys.exit(1)
    with open(src, "r") as fh:
        data = [val.strip() for val in fh.readlines()]

    # Initialize accumulator
    acc = Accumulator()

    # Set up storage for individual instructions
    storage = Storage(data)

    # Prepare the ISA
    commands = Commands()

    # Get inputs from command line API, should
    # convert to a tuple if supplied with
    # comma-separated list
    inputs = Inputs(cliarg.optional.inputs)

    # Step through instruction list, translate to
    # functions
    for _ in list(storage._spaces):

        cmd = commands.parse(
            arg = storage.retrieve(storage._counter)
        )

        arg_types = get_signature(Commands)[cmd.__name__]

        if 'inputs' in arg_types:
            cmd(acc, storage, inputs._values.pop(0))
        else:
            cmd(acc, storage)

if __name__ == "__main__":
    main()
