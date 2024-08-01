import sys

from .parts import *
from .cmd import *
from arglite import parser as cliarg
from itertools import islice
from rich.console import Console
from rich.table import Table

def debug_log(acc, storage) -> None:
    console = Console()
    table = Table(title = "Memory Table", row_styles = ["dim",""])
    for _ in range(0, 100, 10):
        table.add_column(f"{_} - {_ + 9}")
    for _ in range(0, 10):
        row = list(storage._spaces)[_::10]
        row = [str(val).zfill(3) if val else "---" for val in row]
        table.add_row(*row)
    console.print(table)
    console.print(f"ACC VALUE: {acc._value}")

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

    # Trigger debug output if debug flag set
    if cliarg.optional.debug:
        debug_log(acc, storage)

    # Prepare the ISA
    commands = Commands()

    # Get inputs from command line API, should
    # convert to a tuple if supplied with
    # comma-separated list
    inputs = Inputs(cliarg.optional.inputs)

    # Step through instruction list, translate to
    # functions
    while True:

        cmd = commands.parse(
            arg = storage.retrieve(storage._counter)
        )

        arg_types = get_signature(Commands)[cmd.__name__]

        if 'inputs' in arg_types:
            cmd(acc, storage, inputs._values.pop(0))
        else:
            status = cmd(acc, storage)
            if status == False:
                break

    if cliarg.optional.debug:
        debug_log(acc, storage)

if __name__ == "__main__":
    main()
