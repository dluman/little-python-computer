import os
import sys

from .parts import *
from .cmd import *
from .config import *
from arglite import parser as cliarg

from io import StringIO
from itertools import islice
from rich.console import Console
from rich.table import Table

def debug_log(console, acc, storage, output = "") -> None:
    table = Table(title = "Memory Table", row_styles = ["dim",""])
    for _ in range(0, len(storage._spaces), 10):
        table.add_column(f"{_} - {_ + 9}")
    for _ in range(0, 10):
        spaces = list(storage._spaces)
        spaces[storage._counter] = f"> {spaces[storage._counter]}"
        row = [str(val).zfill(3) if val else "---" for val in spaces[_::10]]
        table.add_row(*row)
    # Set up table
    line_no = storage._counter
    instruction = storage.retrieve(storage._counter)
    os.system("clear || cls")
    console.print(table)
    console.print(f"  ACC VALUE: {acc.value}\tPC VALUE: {line_no}\tCMD: {instruction}\tOUTPUT: {output}")
    # Ask for input to advance the table
    input()

def main() -> None:
    # Load instruction set, crash out
    # if set does not exist as file
    try:
        src = sys.argv[1]
    except:
        print("Invalid source file.")
        sys.exit(1)
    with open(src, "r") as fh:
        # Allow for inconsistent lineation in program input
        data = [val.strip() for val in fh.readlines() if val.strip()]

    # Load settings
    config = Config()

    # Initialize accumulator
    acc = Accumulator()

    # Set up storage for individual instructions
    storage = Storage(data, config)

    # Trigger debug output if debug flag set
    if cliarg.optional.debug:
        console = Console()
        debug_log(console, acc, storage)

    # Prepare the ISA
    commands = Commands(cliarg.optional.speed)

    # Get inputs from command line API, should
    # convert to a tuple if supplied with
    # comma-separated list
    inputs = Inputs(cliarg.optional.inputs)
    len_inputs = len(inputs._values)

    # Step through instruction list, translate to
    # functions

    while True:
        if cliarg.optional.debug:
            stdout = sys.stdout
            output = StringIO()
            sys.stdout = output
        cmd = commands.parse(
            line = storage._counter,
            arg = storage.retrieve(storage._counter)
        )

        arg_types = get_signature(Commands)[cmd.__name__]

        if 'inputs' in arg_types:
            try:
                cmd(acc, storage, inputs._values.pop(0))
            except IndexError as e:
                # This is the last case to consider
                #print(f"[ERROR] Reached end of inputs.")
                #print(f"        Expected:\t{storage._expected_inputs}")
                #print(f"        Given:\t\t{len_inputs}")
                sys.exit(1)
        else:
            status = cmd(acc, storage)
            if status == False:
                break
        if cliarg.optional.debug:
            sys.stdout = stdout
            debug_log(console, acc, storage, output.getvalue())

if __name__ == "__main__":
    main()
