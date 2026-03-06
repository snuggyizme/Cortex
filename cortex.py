import sys

p: int = 0
cp: int = 0

tape: list[int] = [0] * 256

tapeNames: dict[str, int] = {}

programBf: list[str | tuple] = []
programCortex: list[list] = []
rawCortex: str = ""

# Main interpreter function:
def execute(brainFuck: str):
    """
    Executes the given BrainFuck code and prints any output produced by the code.
    """
    global p
    global tape

    i: int = 0

    while i < len(brainFuck):
        command = brainFuck[i]
        match command:
            # Movement
            case ">":
                p += 1
                i += 1
            case "<":
                p -= 1
                i += 1

            # Operations
            case "+":
                tape[p] = (tape[p] + 1) % 256
                i += 1
            case "-":
                tape[p] = (tape[p] - 1) % 256
                i += 1

            # I/O
            case ".":
                print(chr(tape[p]), end="")
                i += 1
            case ",":
                tape[p] = ord(input())
                i += 1
            case "P":                      # print integer
                print(tape[p])
                i += 1
            case "D":                      # dump tape
                print(tape)
                i += 1

            # Looping
            case "[":
                if tape[p] == 0:
                    loopDepth = 1
                    i += 1
                    while i < len(brainFuck) and loopDepth > 0:
                        if brainFuck[i] == "[":
                            loopDepth += 1
                        elif brainFuck[i] == "]":
                            loopDepth -= 1
                        i += 1
                else:
                    i += 1
            case "]":
                if tape[p] != 0:
                    loopDepth = 1
                    i -= 1
                    while i >= 0 and loopDepth > 0:
                        if brainFuck[i] == "]":
                            loopDepth += 1
                        elif brainFuck[i] == "[":
                            loopDepth -= 1
                        i -= 1
                    i += 1
                else:
                    i += 1

def runner():
    """
    Runs the entire process of parsing, compiling, and executing the code.
    """
    global programBf
    global programCortex
    global rawCortex
    global tape
    global cp

    programBf.clear()
    programCortex.clear()

    parse()
    compile()

    buffer = ""
    for entry in programBf:
        if isinstance(entry, tuple):
            # Flush any accumulated bf commands before handling tuple
            if buffer:
                execute(buffer)
                buffer = ""
            if entry[0] == "PRN":
                print(tape[cp])
            elif entry[0] == "DMP":
                print(tape)
        else:
            buffer += str(entry)

    # Execute any remaining BrainFuck commands in the buffer
    if buffer:
        execute(buffer)

def parse():
    """
    Parse the given code in cortex and convert it into BrainFuck code.
    The returned code is a list (lines of code) of lists (i0: instruction, i1+: args)
    """
    global rawCortex
    global programCortex

    splitLines = rawCortex.splitlines()
    for line in splitLines:
        if line.strip() == "" or line.strip().startswith("@"): # Empty line or comment
            continue
        else:
            programCortex.append(line.split())

def compile():
    """
    Compiles the program list into a single string of BrainFuck code.
    """
    global programBf
    global programCortex

    for line in programCortex:
        instruction = line[0]
        args = line[1:]

        match instruction:
            case "lft":
                programBf.append(lft(int(args[0])))
                # E.G.
                # lft 3 == <<<
            
            case "rgt":
                programBf.append(rgt(int(args[0])))
                # E.G.
                # rgt 3 == >>>
            
            case "inc":
                programBf.append(inc(int(args[0])))
                # E.G.
                # inc 3 == +++

            case "dec":
                programBf.append(dec(int(args[0])))
                # E.G.
                # dec 3 == ---
            
            case "fly":
                programBf.append(fly(args[0]))
                # E.G.
                # fly 3 (pointer at 5) == <<
            
            case "prt":
                programBf.append(".")
                # E.G.
                # prt == .

            case "prn":
                programBf.append(("PRN", None))
                # Exception: prn is easier done outside of BrainFuck.

            case "dmp":
                programBf.append(("DMP", None))
                # Exception: dmp is easier done outside of BrainFuck.

            case "clr":
                programBf.append("[-]")
                # E.G.
                # clr == [-]
            
            case "inp":
                programBf.append(",")
                # E.G.
                # inp == ,
            
            case "let":
                if len(args) != 2:
                    raise ValueError(f"let requires 2 arguments, got {len(args)} at line: {line}")
                tapeNames[args[0]] = int(args[1])
                # E.G.
                # Exception: let is easier done outside of BrainFuck.

            case "set":
                programBf.append("[-]" + inc(int(args[0])))
                # E.G.
                # set 5 == [-]+++++
            
            case "lop":
                programBf.append("[")
                # E.G.
                # lop == [
            
            case "end":
                programBf.append("]")
                # E.G.
                # end == ]
            
            case _:
                raise ValueError(f"Unknown instruction: {instruction} at line: {line}")
            

        
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def lft(count: int):
    """
    Returns a command to move the tape pointer to the left by the specified count.
    """
    global cp

    cp -= count
    return "<" * count

def rgt(count: int):
    """
    Returns a command to move the tape pointer to the right by the specified count.
    """
    global cp

    cp += count
    return ">" * count

def inc(count: int):
    """
    Returns a command to add the specified count to the current cell.
    """
    return "+" * count

def dec(count: int):
    """
    Returns a command to subtract the specified count from the current cell.
    """
    return "-" * count

def fly(cell: int | str):
    """
    Returns a command to move the tape pointer to the specified cell.
    Specified cell can be <int> or <str>, if <str> is used, it must be in tapeNames and the index of the name in tapeNames will be used as the cell number.
    """
    global cp

    if isinstance(cell, str):
        if cell in tapeNames:
            cell = int(tapeNames[cell])
        else:
            raise ValueError(f"Unknown tape name: {cell}")

    if cell > cp:
        command = rgt(cell - cp)
    else:
        command = lft(cp - cell)
    
    return command

# Instructions reference sheet:
# lft - move pointer left by (arg1: int) cells
# rgt - move pointer right by (arg1: int) cells
# inc - increment current cell by (arg1: int)
# dec - decrement current cell by (arg1: int)
# fly - move pointer to cell (arg1: int | str)
# prt - output the character represented by the current cell
# prn - output the integer value of the current cell
# dmp - dump tape
# clr - clear current cell
# inp - input a character and store its ASCII value in the current cell
# let - assign a name (arg1: str) to the cell (arg2: int) and store the name in tapeNames
# set - set current cell to the value (arg1: int)
# lop - start a loop (while current cell != 0)
# end - end a loop

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, "r") as f:
        rawCortex = f.read()

    runner()

    bfFileName = filename.replace(".cortex", ".bf")

    with open(bfFileName, "w") as f:
        for cmd in programBf:
            if not isinstance(cmd, tuple):
                f.write(str(cmd) + "\n")