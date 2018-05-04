#gets the url for Streamango, directly translated from equivalent Javascript function

array = ['split', 'BIGNF', 'length', 'PxMzv', 'fromCharCode', 'XMJZt', 'Uknst', 'indexOf', 'charAt', 'IgrAi', 'isrQD', 'NrFxr', 'Bfusx', 'EGuje', 'RTbDl', 'skTIa', 'tPROO', 'EyCRq', 'replace', 'reverse', 'NcOIe', '4|6|5|0|7|3|2|1|8', '6|2|9|8|5|4|7|10|0|3|1', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=', 'WSNWx']
def rotate(l, n):
    return l[n:] + l[:n]

def func1(ParamA, ParamB):
    ParamC = ParamB
    while (ParamC > 0):
        array = rotate(ParamA, 1)
        ParamA = array
        ParamC = ParamC - 1
    return array
array = func1(array, ++0x1f0)

def func2(ParamA):
    ParamA = ParamA - 0
    VarB = array[ParamA]
    return VarB

def funcB(numA, numB):
    return numA < numB
def funcC(numA, numB):
    return numA + numB
def funcD(numA, numB):
    return numA != numB
def funcE(numA, numB):
    return numA != numB
def funcF(numA, numB):
    return numA + numB
def funcG(numA, numB):
    return numA | numB
def funcH(numA, numB):
    return numA << numB
def funcI(numA, numB):
    return numA & numB
def funcJ(numA, numB):
    return numA >> numB
def funcK(numA, numB):
    return numA | numB
def funcL(numA, numB):
    return numA << numB
def funcM(numA, numB):
    return numA & numB
def funcN(numA, numB):
    return numA ^ numB

def d(token, num):
    dict = {
        'WSNWx': func2(0),
        'BIGNF': funcB
        ,
        'PxMzv': func2(1),
        'Uknst': funcC
        ,
        'XMJZt': funcD
        ,
        'IgrAi': funcE
        ,
        'WrqtH': funcF
        ,
        'isrQD': funcG
        ,
        'NrFxr': funcH
        ,
        'Bfusx': funcI
        ,
        'EGuje': funcJ
        ,
        'RTbDl': funcK
        ,
        'skTIa': funcL
        ,
        'tPROO': funcM
        ,
        'EyCRq': funcN
        ,
        'NcOIe': func2(2)
    }
    #VarC = dict[func2(3)][func2(4)]('|')
    #func2(4) is 'split'
    VarC = dict[func2(3)].split('|')
    VarD = 0;

    while (True):
        VarS = VarC[VarD]
        VarD += 1
        if VarS == '0':
            continue
        elif VarS == '1':
            #func2(6) is 'length'
            while (dict[func2(5)](VarI, len(token))):
                VarJ = dict[func2(7)].split('|')
                VarK = 0
                while (VarK<11):
                    VarT = VarJ[VarK]
                    VarK += 1
                    if VarT == '0':
                        #func2(8) is 'fromCharCode', which is simply getting unicode from the number
                        VarL = dict['Uknst'](VarL, str(unichr((VarM))))
                        #this part actually build the url
                        continue
                    elif VarT == '1':
                        #func2(8) is 'fromCharCode', which is simply getting unicode from the number
                        if (dict[func2(9)](VarH, 64)):
                            VarL = dict[func2(10)](VarL, str(unichr((VarN))))
                            #this part actually build the url
                        continue
                    elif VarT == '2':
                        #func2(12) is 'charAt'
                        #func2(11) is 'indexOf'
                        VarF = k.index(token[VarI])
                        VarI += 1
                        continue
                    elif VarT == '3':
                        #func2(8) is 'fromCharCode', which is simply getting unicode from the number
                        if (dict[func2(13)](VarG, 64)):
                            VarL = dict['WrqtH'](VarL, str(unichr((VarO))))
                            #this part actually build the url
                        continue
                    elif VarT == '4':
                        VarO = dict[func2(14)](dict[func2(15)](dict[func2(16)](VarF, 15), 4), dict[func2(17)](VarG, 2))
                        continue
                    elif VarT == '5':
                        VarM = dict[func2(18)](dict[func2(15)](VarE, 2), dict[func2(17)](VarF, 4))
                        continue
                    elif VarT == '6':
                        #func2(11) is 'indexOf'
                        VarE = k.index(token[VarI])
                        VarI += 1
                        continue
                    elif VarT == '7':
                        VarN = dict[func2(19)](dict[func2(20)](VarG, 3), 6) | VarH
                        continue
                    elif VarT == '8':
                        VarH = k.index(token[VarI])
                        VarI += 1
                        continue
                    elif VarT == '9':
                        #func2(12) is 'charAt'
                        VarG = k.index(token[VarI])
                        VarI += 1
                        continue
                    elif VarT == '10':
                        VarM = dict[func2(21)](VarM, num)
                        continue
                    else:
                        break
            continue
        elif VarS == '2':
            #token = token[func2(22)](/[^A-Za-z0-9\+\/\=]/g, '')
            #this was the orignal javascript line, I hate figuring out regular expressions
            #but so far things have been working correctly evenb without this, so I think it might not be doing anything
            continue;
        elif VarS == '3':
            #k = k[func2(4)]('')[func2(23)]()['join']('');
            #func2(4) is 'split'
            #func2(23) is 'reverse'
            #Steps are:
            #k = k.split()
            #k = k.reverse()
            #k = k.join('')
            #or more simply:
            k = k[::-1]
            continue
        elif VarS == '4':
            k = dict[func2(24)];
            continue
        elif VarS == '5':
            continue
        elif VarS == '6':
            VarL = '';
            continue
        elif VarS == '7':
            VarI = 0;
            continue
        elif VarS == '8':
            return VarL
        else:
            break
