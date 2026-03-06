# Cortex
An assembly-ish wrapper for BrainFuck

# Syntax
| Instruction | Description |
| ----------- | ----------- |
| LFT | Move pointer left by <arg1: int> cells |
| RGT | Move pointer right by <arg1: int> cells |
| INC | Increment current cell value by <arg1: int> |
| DEC | Decrement current cell value by <arg1: int> |
| FLY | Move pointr to <arg1: cell> |
| PRT | Print ASCII |
| PRN | Print numeral |
| DMP | Dump the contents of the tape |
| CLR | Clear the contents of the current cell |
| INP | Input a character's ASCII value in the current cell |
| LET | Assigns the nickname <arg1: str> to <arg2: cell> |
| SET | Sets the value of the current cell to <arg1: int> |
| LOP | Starts a loop that lasts until the current cell is not zero |
| END | End constraint of a loop |
| CPY | Copy value to destination cell <arg1: cell> from source cell <arg2: cell>
| ADD | Combine the values of <arg1: cell> and <arg2: cell> into <arg1: cell>