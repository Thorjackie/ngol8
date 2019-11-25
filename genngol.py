regs = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']
cmds = [
        ('nop', 0x00),
        ('data', 0x10),
        ('load', 0x20),
        ('stor', 0x30),
        ('jmp', 0x40),
        ('jmpc', 0x41),
        ('jmpg', 0x42),
        ('jmpe', 0x44),
        ('jmpz', 0x48),
        ('busdi', 0x50),
        ('busdo', 0x51),
        ('busai', 0x52),
        ('busao', 0x53),
        ('inc', 0x60),
        ('add', 0x80),
        ('sub', 0x81),
        ('sll', 0x82),
        ('slr', 0x83),
        ('and', 0x84),
        ('not', 0x85),
        ('xor', 0x86),
        ('cmp', 0x87)
        ]

infile = input("input file name:\n> ")
with open(infile, 'r') as f:
    data = f.read()

ofile = infile + '.o'
inst = [x[0] for x in cmds]
print(inst)
eInst = [(i, x) for i,x in enumerate(inst)]
instHex = [x[1] for x in cmds]
def instLookup(instr):
    print("inside lookup\n", "Instr: ", instr)
    for i,x in enumerate(inst):
        if x == instr:
            return instHex[i]
def regHex(reg, a):
    if not a:
        return int(reg[1])
    if a:
        return int(reg[1]) << 4

def hexCatch(inp):
    try:
        int(inp, 16)
        return True
    except ValueError:
        print("ERR:: invalid value presented")
        return False

def output(indat):
    out = []
    print(indat)
    for x in range(0, len(indat), 8):
        out.append(indat[x:x+8])
    print(out)
    for i,x in enumerate(out):
        out[i] = ' '.join(x)
    print(out)
    out = '\n'.join(out)
    out = 'v2.0 raw\n' + out
    print(out)
    with open(ofile, 'w') as f:
        f.write(out)

lines = data.split('\n')
lineStack = []
for lineNum, line in enumerate(lines):
    lineSplit = line.split(' ')
    print(line)
    ## parse lineSplit into instruction, arg1, and arg2's
    ## options:
    ## nop
    ## inst reg:
    ##   [inst reg]
    ## inst hex:
    ##   [inst] [hex]
    ## inst reg hex:
    ##   [inst reg] [hex]
    ## inst reg reg:
    ##   [inst] [reg reg]
    treeSize = len(lineSplit)

    if lineSplit[0] in inst:
        if treeSize == 1:
            ## just nop 
            lineStack.append(f'{0:02x}')

        elif treeSize == 2:
            ## bus op, inc, jmp
            if lineSplit[1] in regs:
                #bus op, inc
                cInst = instLookup(lineSplit[0])
                cBReg = regHex(lineSplit[1], False)
                cInst = cInst + cBReg
                lineStack.append(f'{cInst:02x}')
            elif hexCatch(lineSplit[1]):
                #jmp, cjmp
                cInst = f'{instLookup(lineSplit[0]):02x}'
                cHex = f'{int(lineSplit[1], 16):02x}'
                lineStack.append(cInst)
                lineStack.append(cHex)
            elif lineSplit[1] not in regs and not hexCatch(lineSplit[1]):
                print("ERR: invalid arg presented at line", lineNum)
                break

        elif treeSize == 3:
            ## data, load, stor, alu
            if lineSplit[1] in regs:
                ## data, load, stor, alu
                if lineSplit[2] in regs:
                    ## alu
                    cInst = f'{instLookup(lineSplit[0]):02x}'
                    cAReg = regHex(lineSplit[1], True)
                    cBReg = regHex(lineSplit[2], False)
                    cRegs = f'{(cAReg + cBReg):02x}'
                    lineStack.append(cInst)
                    lineStack.append(cRegs)
                elif hexCatch(lineSplit[2]):
                    ## data, load, stor
                    print(lineSplit[0])
                    cInst = instLookup(lineSplit[0])
                    print(cInst)
                    cBReg = regHex(lineSplit[1], False)
                    cHex = f'{int(lineSplit[2], 16):02x}'
                    cInst = f'{(cInst + cBReg):02x}'
                    lineStack.append(cInst)
                    lineStack.append(cHex)
                else:
                    print("ERR:: invalid argument at line", lineNum)
                    break
            elif lineSplit[1] not in regs:
                print("ERR:: invalid argument at line", lineNum)
                break
        else:
            print("ERR:: invalid parse tree size on line", lineNum)
            break
    elif lineSplit[0] == '':
        output(lineStack)
    elif lineSplit[0] not in inst and lineSplit[0] != '':
        print("ERR:: invalid instruction on line", lineNum)

