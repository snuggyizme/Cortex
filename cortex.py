import sys
from collections import defaultdict
import re

p: int = 0
cp: int = 0

tape: defaultdict[int, int] = defaultdict(int)

tapeNames: dict[str, int] = {}
functions: dict[str, str] = {}

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
                print(dict(tape))
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

    bf_program = "".join(str(cmd) for cmd in programBf)
    execute(bf_program)

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

    i = 0

    while i < len(programCortex):
        line = programCortex[i]
        if line[0] == "def":
            if len(line) != 3:
                raise ValueError(f"def requires 2 arguments, got {len(line)-1} at line {i+1}")
            
            name = line[1]
            rawArgs = line[2]

            bodyLines = []

            depth = 1
            i += 1

            while i < len(programCortex) and depth > 0:
                currentLine = programCortex[i]
                currentInst = currentLine[0]

                if currentInst in ["def", "lop"]:
                    depth += 1
                
                elif currentInst == "end":
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
                
                if depth > 0:
                    bodyLines.append(" ".join(currentLine) + "\n")
                
                i += 1

            if depth != 0:
                raise ValueError(f"Unclosed def '{name}' starting at line {i+1}")
            
            body = "".join(bodyLines)
            DEF(name, rawArgs, body)
        else:
            processLine(line)
            i += 1
                
def processLine(line):
    """
    Compiles a single line
    """
    global programBf

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
            programBf.append("P")

        case "dmp":
            programBf.append("D")

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
        
        case "cpy":
            if len(args) != 2:
                raise ValueError(f"cpy requires 2 arguments, got {len(args)} at line: {line}")
            programBf.append(cpy(args[0], args[1]))
            # E.G.
            # no example fuck you its 3:27
        
        case "add":
            if len(args) != 2:
                raise ValueError(f"add requires 2 arguments, got {len(args)} at line: {line}")
            programBf.append(add(args[0], args[1]))                
            # E.G.
            # add 3 4 (starting at 3) == [+>-<]
        
        case "exe":
            if len(args) != 2:
                raise ValueError(f"exe requires 2 arguments, got {len(args)} at line: {line}")
            name = args[0]
            rawArgs = args[1]
            cortexBody = exe(name, rawArgs)
            tempLines = [l.split() for l in cortexBody.splitlines() if l.strip() and not l.startswith("@")]
            for tempLine in tempLines:
                processLine(tempLine)

        case _:
            raise ValueError(f"Unknown instruction: {instruction} at line: {line}")
            
def _resolve(cell: int | str):
    """
    Turn a cell field (index or name) into a cell index.
    """

    if isinstance(cell, str):
        if cell in tapeNames:
            return int(tapeNames[cell])
        raise ValueError(f"Unknown tape name: {cell}")
    return int(cell)

def _clear(cell: int | str):
    """
    Go to and clear a cell. DOES NOT RETURN THE POINTER.
    """
    cell = _resolve(cell)

    return f"{fly(cell)}[-]"

def _get_args(raw):
    tempArgs: str = raw.strip("[]")

    arguments: list = tempArgs.split()

    for i, x in enumerate(arguments):
        arguments[i] = _resolve(x)
    
    return arguments
        
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

    cell = _resolve(cell)

    if cell > cp:
        command = rgt(cell - cp)
    else:
        command = lft(cp - cell)
    
    return command

def add(dst: int | str, src: int | str):
    """
    Returns a command to add the value of the source cell to the destination cell.
    Both dst and src can be <int> or <str>, if <str> is used, it must be in tapeNames and the index of the name in tapeNames will be used as the cell number.
    """
    global cp
    start = cp

    dst = _resolve(dst)
    src = _resolve(src)
        
    # command = f"[{fly(dst)}+{fly(temp)}+][-{fly(src)}+{fly(temp)}]" # Still sad this somehow doesn't work, piece of art.

    command = ""

    command += cpy(705, src)
    command += fly(705)
    command += "[-"
    command += fly(dst) + "+"
    command += fly(705)
    command += "]"

    command += fly(start)

    return command

def cpy(dst: int | str, src: int | str):
    """
    Returns a command to copy the value of the source cell to the destination cell.
    Both dst and src can be <int> or <str>, if <str> is used, it must be in tapeNames and the index of the name in tapeNames will be used as the cell number.
    """
    global cp
    start = cp

    dst = _resolve(dst)
    src = _resolve(src)

    # command = f"{fly(dst)}[-]{add(dst, src)}"

    command = ""

    command += _clear(dst)             # Clear destination
    command += _clear(705)             # Clear temp

    command += fly(src)                # Go to source, it is our loop counter
    command += "[-"                    # Loop and start to clear source
    command += fly(dst) + "+"          # Transferring source to destination
    command += fly(704) + "+"          # & temp
    command += fly(src)                # Go back to source to check if we are done with the loop
    command += "]"                     # The done with the loop in question

    command += fly(704)                # Go to temp, it is our loop counter
    command += "[-"                    # Loop and start to clear temp
    command += fly(src) + "+"          # Transferring temp back to source
    command += fly(704)                # Go back to temp to check if we are done with the loop
    command += "]"                     # The done with the loop in question
    
    command += fly(start)              # RAAAAAGGHHHHHHH
    
    return command

def DEF(name: str, rawArgs: str, body: str):
    """
    Creates a function with a name, arguments and code body.
    The arguments are arranged in square brackets and seperated by commas (e.g. "[x,y,z]")
    Although this function is named in capitals, the instruction in Cortex is still lowercase.
    """
    global functions
    
    arguments = [arg.strip() for arg in rawArgs.strip("[]").split(",")]
    functions[name] = {
        "arguments": arguments,
        "body": body
    }

def exe(name, rawArgs):
    """
    Runs the function given by name, with arguments
    """
    global functions

    func = functions[name]
    command = func["body"]
    argNames = func["arguments"]

    tempArgs = rawArgs.strip("[]")
    inputs = [i.strip() for i in tempArgs.split(",")]

    if len(inputs) != len(argNames):
        raise ValueError(f"Function {name} expects {len(argNames)} arguments, got {len(inputs)}")

    for a, v in zip(argNames, inputs):
        command = re.sub(r'\b' + re.escape(a) + r'\b', v, command)

    return command

# ((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
# INFORMATION:

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
# cpy - copy value to destination cell (arg2: int | str) from source cell (arg1: int | str)
# add - combine (arg1: int | str) and (arg2: int | str) into (arg1: int | str)
# def - define a function of name (arg1: str) with args (arg2) in square brackets and seperated by spaces (e.g. "def myFunction [x, y, z]"")
# exe - run the function of name (arg1: str) with args (arg2) in square brackets and seperated by spaces (e.g. "exe myFunction [0, 3, name]")

# Built-in functions reference sheet:
# cmp - compare (arg1: int | str) and (arg2: int | str) and store the result (see "cmp reference sheet") in the current cell

# cmp reference sheet:
# if arg1 = arg2: 0
# if arg1 > arg2: 1
# if arg1 < arg2: 2

# temps taken:
# 700: free
# 701: free
# 702: cmp (func)
# 703: cmp (func)
# 704: cpy (inst)
# 705: add (inst)

# ((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

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