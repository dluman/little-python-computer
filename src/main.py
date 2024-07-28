import sys
import parts

from cmd import *
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
    # Initialize accumulator
    acc = parts.Accumulator()
    # Set up storage for individual instructions
    storage = parts.Storage(data)
    # Prepare the ISA
    commands = Commands()
    # Get inputs from command line API, should
    # convert to a tuple if supplied with
    # comma-separated list
    inputs = parts.Inputs(cliarg.optional.inputs)
    agent = Agent(inputs, storage)
    # Step through instruction list, translate to
    # functions; TODO: Remove the agent?
    for inst in agent._program:
        cmd = commands.parse(arg = agent.step())
        arg_types = get_signature(Commands)[cmd.__name__]
        if 'inputs' in arg_types:
            cmd(acc, inputs._values.pop(0))
        if 'accumulate' in arg_types:
            pass
        if 'storage' in arg_types:
            cmd(acc, storage)
    print(f"ACCUMULATOR VALUE:\t{acc._value}")
    print(f"STORAGE OVERVIEW:\t{storage._spaces}")
if __name__ == "__main__":
    main()
