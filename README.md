# PaperPC

[![PyPI version](https://img.shields.io/pypi/v/paperpc)](https://pypi.org/project/paperpc/)

A python implementation of the [Little Man Computer](https://en.wikipedia.org/wiki/Little_man_computer) meant for
use in CI/CD (i.e. GitHub Actions) to verify student programs using the LMC ISA. This implementation uses the 
traditional instruction set plus one additional instruction meant to emulate bit-shifting (as implemented using
another paper computer, the [CARDIAC](https://en.wikipedia.org/wiki/CARDboard_Illustrative_Aid_to_Computation)).

## Install

This project is available via `PyPI`: `python -m pip install paperpc`.

## ISA

|Numeric syntax |Mnemonic equivalent |Instruction |Description                                                   |Destructive |
|:--------------|:-------------------|:-----------|:-------------------------------------------------------------|:------------|
|`1xx`          |`ADD`               |`ADD`       |Adds a number stored in a memory location `xx` to the `Accumulator` |`Yes`  |
|`2xx`          |`SUB`               |`SUBTRACT`  |Subtracts a number stored in a memory location `xx` from the `Accmumulator` |`Yes` |
|`3xx`          |`STA`               |`STORE`     |Stores the value of the `Accumulator` in memory location `xx`  |`No`        |
|`4lr`          |`SFT`               |`SHIFT`     |Shifts `Accumulator` value `l` places to the left, `r` places to the right |`Yes`  |
|`5xx`          |`LDA`               |`LOAD`      |Loads a number stored in memory location `xx` to the `Accumulator`|`Yes`    |
|`6xx`          |`BRA`               |`UNCONDITIONAL BRANCH` | Sets the `Program Counter` to value `xx`, preparing to execute value in `xx` |`No`  |
|`7xx`          |`BRZ`               |`BRANCH IF ZERO` |Verifies `Accumulator` value is `0`; if so, set `Program Counter` to value `xx`, prepare to execute value in `xx`| `No` |
|`8xx`          |`BRP`               |`BRANCH IF POSITIVE`| Verifies `Accumulator` value is greater than `0`; if so, set `Program Counter` to value `xx`, prepare to execute value in `xx` |`No` |
|`901`          |`INP`               |`INPUT`     |Read a single value fromw waiting input, replace `Accumulator` value|`Yes` |
|`902`          |`OUT`               |`OUTPUT`    |Output the current value of the `Accumulator`|`No` |
|`903`          |`PSH`               |`PUSH`      |Push a value to the machine's dedicated stack (080) |`No` |
|`904`          |`POP`               |`POP`       |Pop a value from the machine's dedicated stack |`Yes` |
|`905`          |`PTR`               |`STACK POINTER`|Retrieves and loads the current stack pointer to the `Accumulator`|`Yes` |
|`906`          |`SHI`               |`STACK HEIGHT` |Calculates and places the current stack height in the `Accumulator`|`Yes` |
|`000`          |`HLT`               |`HALT`      |Terminates program |`No` |

### The stack

The PaperPC stack starts at storage `080`. It occupies 18 spaces (limit `098`). This memory range may be used by
general heap operations (i.e. values can be assigned to this range). However, any stack operation will overwrite
values in the range starting at the stack pointer base, `080`. The stack overflows if the value of the stack pointer
increments above `098`.

In future releases, this will be configurable (e.g. a configuration file can remap, increase, or decrease the stack
size). This is planned, but not yet implemented as a `.pcconfig` file, existing on a per-project basis.

## Using the program

Invoke the package via the CLI script: `paperpc example.ppc --inputs [2,3]`

Here, add the command flag `--inputs` after the name of the script followed by a comma-separated list of values to include as 
inputs to the machine. The program will parse the correct input when encountering the `901` instruction. Think of it like
a stack, except it's `FIFO` rather than `LIFO`. So, not really a stack.

### Implementation-specific details

General note: all programs _must_ terminate using a `000` (`HLT`) instruction.

#### Inputs

The following program adds any two numbers from input:
```
1    901    @ Read one value from input to Accumulator
2    360    @ Store in memory location 060
3    901    @ Read one value from input to Accumulator
4    648    @ Unconditional branch to data in 048
48   160    @ Add data in 060 to Accumulator
49   902    @ Output the sum stored in the Accumulator
50   000    @ Halt
```

#### Branching

The following program uses `BRP` and `BRZ` to perform a countdown from any given input:
```
001     901 @ Read starting value from input to Accumulator
002     350 @ Store value in memory space 50
003     902 @ Output value currently in Accumulator
004     251 @ Subtract a bootstrapped 1 in memory location 51
005     740 @ Branch to end if Accumulator value is 0
006     803 @ Branch to 003 if Accumulator value is positive
040     000 @ Halt
051     001 @ Bootstrap a 1
```

#### Shifting

Routine below shifts a number (such as `200`) right `2` times, `1` left to produce a value like (e.g. `2`):
```
001     901 @ Read starting value from input to Accumulator
002     402 @ Shift 2 right
003     410 @ Shift 1 left
004     902 @ Output value of Accumulator
005     000 @ Halt
```
