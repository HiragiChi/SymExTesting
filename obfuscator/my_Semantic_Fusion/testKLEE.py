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

def unitTest(signature, testRet=False):
    temp = signature.replace(' ', '').split(':')
    funcName = temp[0]
    retType = temp[2].rstrip('\n')
    argTypes = temp[1][1:-1].split(',')
    #print("func:%s, ret:%s, arg:%s\n" % (funcName, retType, "|".join(argTypes)))
    declaration = getVariable("var0", retType)
	# declaration
    variableCount = 1
    for argType in argTypes:
        declaration += getVariable("var%d" % variableCount, argType)
        variableCount += 1
    #print(declaration)

    # make symbolic and to-solve
    if testRet != True or (retType == "null" or retType == "point"): # we set one argument to unknown and solve it.
        symId = random.randint(1, variableCount - 1)
    else: # we set ret to unknown and solve it.
        symId = 0

    # klee_make_symbolic (addr, size, "label");
    kleeSymbolic = "klee_make_symbolic(&var%d, sizeof(var%d), \"var%d\");\n" % (symId, symId, symId)

    argList = ["var%d" % i for i in range(1, variableCount)]
    call = funcName + "(" + ", ".join(argList) + ")"
    shortTypePrint = {"int":"%d", "double": "%f", "float": "%f", "str": "%s", "bool": "%d", "null": "%f"}

    printRet = "{\nfprintf(STD, \"===%s===\\n\", var%d);\n assert(0);\n}" % (shortTypePrint[retType], symId)
    printArg = "{\nfprintf(STD, \"===%s===\\n\", var%d);\n assert(0);\n}" % (shortTypePrint[argTypes[symId - 1]], symId)
    conditionalInvokeCall = "if (%s == var0)" % call
    unconditionalInvokeCall = "if (%s) \n" % call
    if symId == 0: # ret is unknown
        # check KLEE's result -- ret
        mainKLEECode = "#include<klee/klee.h>\n" + declaration + kleeSymbolic + conditionalInvokeCall + printRet.replace('STD', 'stdout')
        finalKLEECode = header.replace("DECLARATION", mainKLEECode)
        ifAssertCrash, result = KLEERunOnCode(funcName, finalKLEECode, retType)
        print("after", result)

        # apply KLEERet and check concrete run crashes
        declaration = '\n'.join([i if 'var0 = ' not in i else i[0: i.find('=') + 1] + result + ';\n' for i in declaration.split('\n')])
        mainCode = declaration + conditionalInvokeCall + printRet.replace('STD', 'stderr')
        finalCode= header.replace("DECLARATION", mainCode)
        ifAssertCrash, result = ConcreteRunOnCode(funcName, finalCode, retType)

    else: # one arg is unknown
        # obtain ret fron concrete run
        mainCode = declaration + unconditionalInvokeCall + printArg.replace('STD', 'stderr')
        finalCode = header.replace("DECLARATION", mainCode)
        ifAssertCrash, result = ConcreteRunOnCode(funcName, finalCode, argTypes[symId - 1]) # check if assert error is triggered
        print("after", result)

        declaration = '\n'.join([i if 'var%s = ' % symId not in i else i[0: i.find('=') + 1] + result + ';\n' for i in declaration.split('\n')])
        mainKLEECode = "#include<klee/klee.h>\n" + declaration + kleeSymbolic + unconditionalInvokeCall + printArg.replace('STD', 'stdout')
        finalKLEECode = header.replace("DECLARATION", mainKLEECode)
        ifAssertCrash, KLEEArg = KLEERunOnCode(funcName, finalKLEECode, argTypes[symId - 1])

    if ifAssertCrash > 0:
        print("pass")
    else:
        print("fail")

def KLEERunOnCode(funcName, code, _type='str'):
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

    invokeCProgram = "klee --libc=uclibc --posix-runtime --external-calls=all -link-llvm-lib=/tmp/klee-uclibc-110/lib/libm.a -link-llvm-lib=/tmp/klee-uclibc-110/lib/libcrypt.a \
    -link-llvm-lib=/tmp/klee-uclibc-110/lib/libnsl.a -link-llvm-lib=/tmp/klee-uclibc-110/lib/libresolv.a  \
    -link-llvm-lib=/tmp/klee-uclibc-110/lib/libutil.a  -link-llvm-lib=/tmp/klee-uclibc-110/lib/librt.a \
    -write-smt2s -use-constant-arrays=false  %s.bc "  % name

    p2 = Popen(invokeCProgram, shell=True, stdout=PIPE, stderr=PIPE)
    result, stderr=p2.communicate()
    stderr = stderr.decode('utf-8')
    result = result.decode('utf-8')
    if "ASSERTION" in stderr:
        status = 1
    result = result.split('===')[1]
    return status, parseResult(result, _type)

def parseResult(result, _type):
    if _type == 'str':
        result = "\"" + result.replace("\\", "\\\\").replace("\"", "\\\"").replace("%", "\\%") + "\""
    #print("-----RESULT-----")
    #print(result)
    #print("-----RESULT-----")
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
        print("FATAL: error with compilation")
        print(stderr.decode('utf-8'))
        status = -1

    invokeCProgram = "./%s" % name
    p2 = Popen(invokeCProgram, shell=True, stdout=PIPE, stderr=PIPE)
    result, stderr=p2.communicate()
    stderr = stderr.decode('utf-8')
    if "Assertion failed" in stderr:
        status = 1

    result = stderr.split('===')[1]
    return status, parseResult(result, _type)

unitTest("stpncpy:(str, str, int):null")
#t = generateRandomString(30)
#print(t)
#KLEERunOnCode('main', "#include<stdio.h> \n#include<assert.h> \n void main() {fprintf(stdout, \"===hello world===\"); assert(0);}", _type="str")

