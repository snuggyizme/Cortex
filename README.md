# Cortex
An assembly-ish wrapper for BrainFuck

# Syntax
| Instruction | Description |
| ----------- | ----------- |
| lft | Move pointer left by <arg1: int> cells |
| rgt | Move pointer right by <arg1: int> cells |
| inc | Increment current cell value by <arg1: int> |
| dec | Decrement current cell value by <arg1: int> |
| fly | Move pointr to <arg1: cell> |
| prt | Print ASCII |
| prn | Print numeral |
| dmp | Dump the contents of the tape |
| clr | Clear the contents of the current cell |
| inp | Input a character's ASCII value in the current cell |
| let | Assigns the nickname <arg1: str> to <arg2: cell> |
| set | Sets the value of the current cell to <arg1: int> |
| lop | Starts a loop that lasts until the current cell is not zero |
| end | End constraint of a loop |
| cpy | Copy value to destination cell <arg1: cell> from source cell <arg2: cell>
| add | Combine the values of <arg1: cell> and <arg2: cell> into <arg1: cell>