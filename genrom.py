# writes nlog rom file to file 'nROM'
eacc = 2 ** 0
cin = 2 ** 1
etmp = 2 ** 2
bus1 = 2 ** 3
eram = 2 ** 4
epc = 2 ** 5
ctpc = 2 ** 6
ldpc = 2 ** 7
eR = 2 ** 8
eB = 2 ** 9
rst = 2 ** 10
varb = 2 ** 11
varc = 2 ** 12
vard = 2 ** 13
vare = 2 ** 14
varf = 2 ** 15
sflgs = 2 ** 16
srsel = 2 ** 17
sir = 2 ** 18
sacc = 2 ** 19
stmp = 2 ** 20
sR = 2 ** 21
spc = 2 ** 22
smar = 2 ** 23
sram = 2 ** 24
var19 = 2 ** 25
var1a = 2 ** 26
var1b = 2 ** 27
var1c = 2 ** 28
var1d = 2 ** 29
var1e = 2 ** 30
var1f = 2 ** 31

def hexConv(uCode):
    out = []
    for i in uCode:
        out.append(f'{i:02x}')
    return out

def fmt(byt):
    out = []
    instLen = 6
    for x in range(0, len(byt), instLen):
        out.append(byt[x:x+instLen])
    return out

def fmtuCode(mcode):
    byt = hexConv(mcode)
    bytl = fmt(byt)
    out = []
    for x in bytl:
        out.append(' '.join(fetch) + ' ' + ' '.join(x) + '\n')
    out = ''.join(out)
    return out


fetch = hexConv([epc|smar, eram|sir|ctpc|spc])
print("fetch: ", fetch)
uCode = [
        rst, 0, 0, 0, 0, 0, # nop
        epc|smar, eram|sR|ctpc|spc, rst, 0, 0, 0, # data
        epc|smar, eram|smar|ctpc|spc, eR|sram, rst, 0, 0, # load
        epc|smar, eram|smar|ctpc|spc, eram|sR, rst, 0, 0, # stor
        ctpc|spc, rst, 0, 0, 0, 0, # jmpf
        epc|smar, eram|spc|ctpc|srsel, eR|sR, rst, 0, 0, # bus
        eR|bus1|sacc, eacc|sR, rst, 0, 0, 0, # inc
        rst, 0, 0, 0, 0, 0, # 

        epc|smar, eram|srsel|ctpc|spc, eB|eR|stmp, eR|sacc|sflgs, eacc|sR, rst, # alu
        rst, 0, 0, 0, 0, 0, # 
        rst, 0, 0, 0, 0, 0, # 
        rst, 0, 0, 0, 0, 0, # 
        rst, 0, 0, 0, 0, 0, # 
        rst, 0, 0, 0, 0, 0, # 
        rst, 0, 0, 0, 0, 0, # 
        rst, 0, 0, 0, 0, 0, # 

        rst, 0, 0, 0, 0, 0, # nop
        epc|smar, eram|sR|ctpc|spc, rst, 0, 0, 0, # data
        epc|smar, eram|smar|ctpc|spc, eR|sram, rst, 0, 0, # load
        epc|smar, eram|smar|ctpc|spc, eram|sR, rst, 0, 0, # stor
        epc|smar, eram|spc|ldpc, rst, 0, 0, 0, # jmpt
        epc|smar, eram|spc|ctpc|srsel, eR|sR, rst, 0, 0, # bus
        eR|bus1|sacc, eacc|sR, rst, 0, 0, 0, # inc
        rst, 0, 0, 0, 0, 0, #

        epc|smar, eram|srsel|ctpc|spc, eB|eR|stmp, eR|sacc|sflgs, eacc|sR, rst, # alu
        0, 0, 0, 0, 0, 0, # 
        0, 0, 0, 0, 0, 0, # 
        0, 0, 0, 0, 0, 0, # 
        0, 0, 0, 0, 0, 0, # 
        0, 0, 0, 0, 0, 0, # 
        0, 0, 0, 0, 0, 0, # 
        0, 0, 0, 0, 0, 0 # 
        ]
outp = 'v2.0 raw\n' + fmtuCode(uCode)
print(outp)
with open('romn', 'w') as f:
    f.write(outp)
