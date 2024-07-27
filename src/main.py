import sys
import parts

from agent import Agent
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
    # Set up storage for individual instructions
    storage = parts.Storage(data)
    for inst in storage._program:
        print(inst)
    # Get inputs from command line API, should
    # convert to a tuple if supplied with
    # comma-separated list
    inputs = parts.Inputs(cliarg.optional.inputs)
    agent = Agent(inputs, storage)
    # Step through instruction list
    for addr, val in enumerate(storage._program):
        print(addr)

if __name__ == "__main__":
    main()
