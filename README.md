# The Little Python Computer

A python implementation of the [Little Man Computer](https://en.wikipedia.org/wiki/Little_man_computer) meant for
use in CI/CD (i.e. GitHub Actions) to verify student programs using the LMC ISA. This implementation uses the 
traditional instruction set plus one additional instruction meant to emulate bit-shifting (as implemented using
another paper computer, the [CARDIAC](https://en.wikipedia.org/wiki/CARDboard_Illustrative_Aid_to_Computation)).

## ISA

|Numeric syntax |Mnemonic equivalent |Instruction |Description                                                   |Desctructive |
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

## Using the program

Invoke the package via the CLI script: `lpc example.lpc --inputs 2,3`

Here, add the command flag `--inputs` after the name of the script followed by a comma-separated list of values to include as 
inputs to the machine. The program will parse the correct input when encountering the `901` instruction. Think of it like
a stack, except it's `FIFO` rather than `LIFO`. So, not really a stack.
