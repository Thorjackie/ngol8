# generates ngol runnable code from human readable -- basically an assembler
insts = {
        'nop': 0x00,
        'data': 0x10,
        'load': 0x20,
        'stor': 0x30,
        'jmp': 0x40,
        'jmpz': 0x48,
        'jmpe': 0x44,
        'jmpg': 0x42,
        'jmpc': 0x41,
        'busdi': 0x50,
        'busdo': 0x51,
        'busai': 0x52,
        'busao': 0x53,
        'inc': 0x60,        
        'add': 0x88,
        'sub': 0x89,
        'sll': 0x8a,
        'slr': 0x8b,
        'and': 0x8c,
        'not': 0x8d,
        'xor': 0x8e,
        'cmp': 0x8f
        }

RA = {
        'r0': 0x00,
        'r1': 0x10,
        'r2': 0x20,
        'r3': 0x30,
        'r4': 0x40,
        'r5': 0x50,
        'r6': 0x60,
        'r7': 0x70
        }

RB = {
        'r0': 0x00,
        'r1': 0x01,
        'r2': 0x02,
        'r3': 0x03,
        'r4': 0x04,
        'r5': 0x05,
        'r6': 0x06,
        'r7': 0x07
        }

infile = input("name of file to be read: \n> ")

with open(infile, 'r') as f:
    indata = f.read()

lines = indata.split('\n')
lines.pop()
print(lines)
splitlines = []

for line in lines:
    splitlines.append(line.split(' '))

lineo = []
for inst in splitlines:
    cmd = inst[0]
    args = inst[1:]
    ncmd = insts[cmd]
    nline = [ncmd, args]
    print('pre: ', cmd, nline)
    if len(args) == 0:
        nline = [ncmd]
    elif len(args) == 1:
        if args[0] in RB:
            nline[1] = RB[args[0]]
        else:
            nline[1] = int(args[0],16)

    elif len(args) == 2: 
        print('debug:')
        print('> len args 2!!!')
        if args[0] in RA:
            print('> args0 in regs')
            if args[1] in RB:
                print('> args1 in regs')
                args[1] = RB[args[1]]
                args[0] = RA[args[0]]
                nline[1] = args[0] + args[1]
                print('> nline: ', nline)
            else:
                print('> args1 not in regs')
                args[0] = RB[args[0]]
                print('> args0: ', args[0])
                print('> ncmd: ', ncmd)
                ncmd += args[0]
                print('> pncmd: ', ncmd)
                nline[1] = int(args[1], 16)
    for i,x in enumerate(nline):
        nline[i] = f'{x:02x}'
    lineo.append(' '.join(nline))
    print(nline)
print(lineo)
lineo = ' '.join(lineo)
lineo = lineo.split(' ')
print(lineo)
nlineo = []
for x in range(0, len(lineo), 8):
    nlineo.append(lineo[x:x+8])
print(nlineo)
for i,x in enumerate(nlineo):
    nlineo[i] = ' '.join(x)
nlineo = '\n'.join(nlineo)
print(nlineo)
output = 'v2.0 raw\n' + nlineo
ofile = infile + '.ot'
with open(ofile, 'w') as f:
    f.write(output)

