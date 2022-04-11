import os
import random
import time

header ="""#include<stdio.h>
#include<klee/klee.h>
#include<assert.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

typedef char str[100];
int main() {
DECLARATION
}"""

def getVariable(varName, _type):
    if _type == "null" or _type == "point":
        # pointer type only appears in ret
        retString = "char *%s = NULL;\n" % varName
    elif _type == "str":
        val = "test_string"
        retString = "str %s = \"%s\";\n" % (varName, val)
    else:
        val = 10
        retString = "%s %s = %s;\n" % (_type, varName, val)
    return retString

def unitTest(signature):
    temp = signature.replace(' ', '').split(':')
    funcName = temp[0]
    retType = temp[2].rstrip('\n')
    argTypes = temp[1][1:-1].split(',')
    print("func:%s, ret:%s, arg:%s\n" % (funcName, retType, "|".join(argTypes)))
	
    declaration = getVariable("var0", retType)
	# declaration
    variableCount = 1
    for argType in argTypes:
        declaration += getVariable("var%d" % variableCount, argType)
        variableCount += 1
    #print(declaration)

    # make symbolic and to-solve
    # random integer from 0 to 9
    if retType == "null" or retType == "point":
        symId = random.randint(1, variableCount - 1)
    else:
        symId = random.randint(0, variableCount - 1)

    # klee_make_symbolic (addr, size, "label");
    declaration += "klee_make_symbolic(&var%d, sizeof(var%d), \"var%d\");\n" % (symId, symId, symId)

    argList = ["var%d" % i for i in range(1, variableCount)]
    call = funcName + "(" + ", ".join(argList) + ")"
    shortTypePrint = {"int":"%d", "double": "%f", "float": "%f", "str": "%s", "bool": "%d", "null": "%f"}

    if symId != 0:
        printStmt = "printf(\"%s\\n\", var%d);\n" % (shortTypePrint[argTypes[symId - 1]], symId)
    else:
        printStmt = "printf(\"%s\\n\", var%d);\n" % (shortTypePrint[retType], symId)

    if retType == "null" or retType == "point":
        declaration += "%s;\n" % call
        declaration += printStmt
    else:
        declaration += "if (%s == var0) {\n %s assert(0);\n}\n" % (call, printnStmt)
    print(header.replace("DECLARATION", declaration))


unitTest("stpncpy:(str, str, int):null")
