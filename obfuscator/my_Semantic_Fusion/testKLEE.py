import os
import random
import time
from subprocess import PIPE, Popen
#pip install StringGenerator
from strgen import StringGenerator as SG
import platform
from ctypes import *
from distutils.ccompiler import new_compiler

header ="""#include<stdio.h>
#include<assert.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

typedef char str[102];
void main() {
DECLARATION
return;
}"""
def generateRandomString(length):
    return SG(r"[\w\p]{%d}&[\p]{2}" % length).render().replace("\\", "\\\\").replace("\"", "\\\"").replace("%", "\\%")

def getVariable(varName, _type):
    if _type == "null" or _type == "point":
        # pointer type only appears in ret
        retString = "char *%s = NULL;\n" % varName
    elif _type == "str":
        length = random.randint(0, 100)
        val = generateRandomString(length)
        retString = "str %s = \"%s\";\n" % (varName, val)
    else:
        val = random.randint(0, 100)
        retString = "%s %s = %s;\n" % (_type, varName, val)
    return retString

shortTypePrint = {"int":"%d", "double": "%f", "float": "%f", "str": "%s", "bool": "%d", "null": "%f"}
def variableDeclaration(signature, prefix):
    temp = signature.replace(' ', '').split(':')
    funcName = temp[0]
    retType = temp[2].rstrip('\n')
    argTypes = temp[1][1:-1].split(',')
    #print("func:%s, ret:%s, arg:%s\n" % (funcName, retType, "|".join(argTypes)))
    declaration = getVariable("%s_var0" % prefix, retType)
	# declaration
    variableCount = 1
    for argType in argTypes:
        declaration += getVariable("%s_var%d" % (prefix, variableCount), argType)
        variableCount += 1
    #print(declaration)
    argList = ["%s_var%d" % (prefix, i) for i in range(1, variableCount)]
    call = funcName + "(" + ", ".join(argList) + ")"
    printRet = "{\nfprintf(STD, \"===%s\\n\", %s_var0);\n assert(0);\n}" % (shortTypePrint[retType], prefix)
    directInvokeCall = "%s;" % call

    # ground truth
    mainCode = declaration + directInvokeCall + printRet.replace('STD', 'stderr')
    finalCode= header.replace("DECLARATION", mainCode)
    ifAssertCrash, groundRet = ConcreteRunOnCode(funcName, finalCode, retType)

    return (funcName, argTypes, retType, declaration, variableCount, call, groundRet)

def mixTwoUnits(sig1, sig2, testRet1 = False, testRet2 = False):
    """
    Three runs for each case:
    1. concrete run to obtain ground truth
    2. KLEE run to test
    3. concrete run to verify
    """
    prefix1 = "f1"
    prefix2 = "f2"
    funcName1, argTypes1, retType1, declaration1, variableCount1, call1, groundRet1 = variableDeclaration(sig1, prefix=prefix1)
    funcName2, argTypes2, retType2, declaration2, variableCount2, call2, groundRet2 = variableDeclaration(sig2, prefix=prefix2)

    if testRet1 != True or retType1 == "null" or retType1 == "point": # we set one argument to unknown and solve it.
        symId1 = random.randint(1, variableCount1 - 1)
    else: # we set ret to unknown and solve it.
        symId1 = 0

    if testRet2 != True or (retType2 == "null" or retType2 == "point"): # we set one argument to unknown and solve it.
        symId2 = random.randint(1, variableCount2 - 1)
    else: # we set ret to unknown and solve it.
        symId2 = 0

    declaration1 = '\n'.join([i if '%s_var0 = ' % (prefix1) not in i else i[0: i.find('=') + 1] + groundRet1 + ';\n' for i in declaration1.split('\n')])
    declaration2 = '\n'.join([i if '%s_var0 = ' % (prefix2) not in i else i[0: i.find('=') + 1] + groundRet2 + ';\n' for i in declaration2.split('\n')])
    kleeSymbolic = "klee_make_symbolic(&%s_var%d, sizeof(%s_var%d), \"%s_var%d\");\n" % (prefix1, symId1, prefix1, symId1, prefix1, symId1)
    kleeSymbolic += "klee_make_symbolic(&%s_var%d, sizeof(%s_var%d), \"%s_var%d\");\n" % (prefix2, symId2, prefix2, symId2, prefix2, symId2)

    if retType1 == 'null' or retType1 == 'point':
        call1 = "(%s)" % (call1)
    else:
        call1 = "(%s == %s_var0)" % (call1, prefix1)

    if retType2 == 'null' or retType2 == 'point':
        call2 = "(%s)" % (call2)
    else:
        call2 = "(%s == %s_var0)" % (call2, prefix2)

    condition = 'if (%s && %s) ' % (call1, call2)
    printStmt = "{\nfprintf(STD, \"===%s\\n\", %s_var%d);\nfprintf(STD, \"===%s\\n\", %s_var%d);\nassert(0);\n}" % \
            (shortTypePrint[retType1] if symId1 == 0 else shortTypePrint[argTypes1[symId1 - 1]], prefix1, symId1,\
            shortTypePrint[retType2] if symId2 == 0 else shortTypePrint[argTypes1[symId2 - 1]], prefix2, symId2\
            )
    mainKLEECode = "#include<klee/klee.h>\n" + declaration1 + declaration2 + kleeSymbolic + condition+ printStmt.replace('STD', 'stdout')
    finalKLEECode = header.replace("DECLARATION", mainKLEECode)
    ifAssertCrash, KLEEArgs = KLEERunOnCode(funcName1 + "-" + funcName2, finalKLEECode, \
            retType1 if symId1 == 0 else argTypes1[symId1 - 1],\
            retType2 if symId2 == 0 else argTypes1[symId2 - 1])


    declaration = '\n'.join([i if '%s_var%s = ' % (prefix1, symId1) not in i else i[0: i.find('=') + 1] + KLEEArgs[0] + ';\n' for i in declaration1.split('\n')])
    declaration = '\n'.join([i if '%s_var%s = ' % (prefix2, symId2) not in i else i[0: i.find('=') + 1] + KLEEArgs[1] + ';\n' for i in declaration2.split('\n')])
    mainCode = declaration1 + declaration2 + condition + printStmt.replace('STD', 'stderr')
    finalCode = header.replace("DECLARATION", mainCode)
    ifAssertCrash, result = ConcreteRunOnCode(funcName1 + "-" + funcName2, finalCode, \
            retType1 if symId1 == 0 else argTypes1[symId1 - 1])
    if ifAssertCrash:
        print('pass')
    else:
        print('fail')



def unitTest(signature, testRet = False):
    prefix = "f1"
    funcName, argTypes, retType, declaration, variableCount, call, groundRet = variableDeclaration(signature, prefix=prefix)

    if testRet != True or (retType == "null" or retType == "point"): # we set one argument to unknown and solve it.
        symId = random.randint(1, variableCount - 1)
    else: # we set ret to unknown and solve it.
        symId = 0

    if retType == 'null' or retType == 'point':
        call = "(%s)" % (call)
    else:
        call = "(%s == %s_var0)" % (call, prefix)

    kleeSymbolic = "klee_make_symbolic(&%s_var%d, sizeof(%s_var%d), \"%s_var%d\");\n" % (prefix, symId, prefix, symId, prefix, symId)
    condition = 'if (%s) ' % call
    printStmt = "{\nfprintf(STD, \"===%s\\n\", %s_var%d);\nassert(0);\n}" % \
            (shortTypePrint[retType] if symId == 0 else shortTypePrint[argTypes[symId - 1]], prefix, symId)
    mainKLEECode = "#include<klee/klee.h>\n" + declaration + kleeSymbolic + condition + printStmt.replace('STD', 'stdout')
    finalKLEECode = header.replace("DECLARATION", mainKLEECode)
    ifAssertCrash, KLEEArg = KLEERunOnCode(funcName, finalKLEECode, \
            retType if symId == 0 else argTypes[symId - 1])

    declaration = '\n'.join([i if '%s_var%s = ' % (prefix, symId) not in i else i[0: i.find('=') + 1] + KLEEArg + ';\n' for i in declaration.split('\n')])
    mainCode = declaration + condition + printStmt.replace('STD', 'stderr')
    finalCode = header.replace("DECLARATION", mainCode)
    ifAssertCrash, result = ConcreteRunOnCode(funcName, finalCode,\
            retType if symId == 0 else argTypes[symId - 1])
    if ifAssertCrash:
        print('pass')
    else:
        print('fail')

def KLEERunOnCode(funcName, code, _type='str', mix=False):
    name = "%s-klee" % funcName
    with open("%s.c" % name, 'w') as fp:
        fp.write(code)

    status = 0
    ## copied from testScript.py
    compileCommand = "clang -Wno-unknown-escape-sequence -Wno-main-return-type -emit-llvm -o %s.bc -c %s.c" % (name, name)

    p1 = Popen(compileCommand, shell=True, stdout=PIPE, stderr=PIPE)
    # FIXME it is sooo strange here:
    # when there is an abort, e.g., using assert(0); 
    # on Linxu stdout is not correctly redirected while stderr is!
    # therefore, I can only capture the responsne in stderr instead of stdout.
    # Mac system works as a charm.
    compileResult, stderr=p1.communicate()
    if(stderr):
        print("FATAL: error with compilation for KLEE")
        print(stderr.decode('utf-8'))
        status = -1

    invokeCProgram = "timeout 10 klee --libc=uclibc --posix-runtime --external-calls=all -link-llvm-lib=/tmp/klee-uclibc-110/lib/libm.a -link-llvm-lib=/tmp/klee-uclibc-110/lib/libcrypt.a \
    -link-llvm-lib=/tmp/klee-uclibc-110/lib/libnsl.a -link-llvm-lib=/tmp/klee-uclibc-110/lib/libresolv.a  \
    -link-llvm-lib=/tmp/klee-uclibc-110/lib/libutil.a  -link-llvm-lib=/tmp/klee-uclibc-110/lib/librt.a \
    -write-smt2s -use-constant-arrays=false  %s.bc "  % name

    p2 = Popen(invokeCProgram, shell=True, stdout=PIPE, stderr=PIPE)
    result, stderr=p2.communicate()
    stderr = stderr.decode('utf-8')
    result = result.decode('utf-8')
    if "ASSERTION" in stderr:
        status = 1
    if mix:
        print(result)
        result = [parseResult(result.split('===')[1], _type), parseResult(result.split('===')[2], mix)]
    else:
        result = parseResult(result.split('===')[1], _type)
    return status, result

def parseResult(result, _type):
    if _type == 'str':
        result = "\"" + result.replace("\\", "\\\\").replace("\"", "\\\"").replace("%", "\\%") + "\""
    elif _type == 'null':
        result = 'NULL'

    return result


def ConcreteRunOnCode(funcName, code, _type='str'):
    name = funcName
    with open('%s.c' % name, 'w') as fp:
        fp.write(code)

    status = 0
    ## copied from testScript.py
    compileCommand = "clang -Wno-unknown-escape-sequence -Wno-main-return-type -o %s %s.c" % (name, name)
    p1 = Popen(compileCommand, shell=True, stdout=PIPE, stderr=PIPE)
    compileResult, stderr=p1.communicate()
    if(stderr):
        #print("FATAL: error with compilation")
        #print(stderr.decode('utf-8'))
        status = -1

    invokeCProgram = "./%s" % name
    p2 = Popen(invokeCProgram, shell=True, stdout=PIPE, stderr=PIPE)
    result, stderr=p2.communicate()
    stderr = stderr.decode('utf-8')
    if "Assertion" in stderr:
        status = 1

    result = stderr.split('===')[1]
    return status, parseResult(result, _type)

mixTwoUnits("stpncpy:(str, str, int):null", "stpncpy:(str, str, int):null")
#t = generateRandomString(30)
#print(t)
#KLEERunOnCode('main', "#include<stdio.h> \n#include<assert.h> \n void main() {fprintf(stdout, \"===hello world===\"); assert(0);}", _type="str")
