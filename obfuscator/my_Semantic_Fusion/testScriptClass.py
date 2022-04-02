import os
import random
import time
from subprocess import PIPE, Popen
RUNJPF=True

STORE_RESULT=True
letters=["x","y","a","b","c"]

def mathInputGenerator(num):
    inputList=random.sample(range(1, 1000), num)
    return inputList
class SymSEtest():
    def __init__(self,func):
        self.func=func
        self.totalCounter=0
        self.correctCounter=0

        protoPath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/inputGeneration/prototypes"
        self.resultFilePath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/result/result"
        self.procedurePath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/result/procedure"
        SEPath="/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/"

        compileCommand0="javac -d /home/hiragi/Desktop/jpf/jpf-symbc/build/examples -g /home/hiragi/Desktop/jpf/jpf-symbc/src/examples/SETest_{FUNC}.java"
        jpfRunCommand0="/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Xmx1024m -ea -Dfile.encoding=UTF-8 -classpath /home/hiragi/Desktop/jpf/jpf-core/build/main:/home/hiragi/Desktop/jpf/jpf-core/build/peers:/home/hiragi/Desktop/jpf/jpf-core/build/classes:/home/hiragi/Desktop/jpf/jpf-core/build/annotations:/home/hiragi/Desktop/jpf/jpf-core/build/examples:/home/hiragi/Desktop/jpf/jpf-core/build/tests:/home/hiragi/Desktop/jpf/jpf-core/build:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/main:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/peers:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/lib/*:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/tests:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/examples gov.nasa.jpf.tool.RunJPF /home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf"

        self.protoSEPath=protoPath+"/testCase.java.prototype.new"
        testFilePath0=SEPath+"/SETest_{FUNC}.java"
        self.protoScriptPath=protoPath+'/proto.jpf'
        testScriptPath0=protoPath+'/SETest_{FUNC}.jpf'

        
        self.jpfRunCommand=jpfRunCommand0.format(FUNC=func)
        self.compileCommand=compileCommand0.format(FUNC=func)
        self.testFilePath=testFilePath0.format(FUNC=func)
        self.testScriptPath=testScriptPath0.format(FUNC=func)
    
    def SEProtoReading(self,variables,constraints,otherVariables):
        protoSE=open(self.protoSEPath, 'r')
        protoSEList=[]
        for line in protoSE.readlines():
            protoSEList.append(line)
        protoSE.close()

        testList=[]
        for item in protoSEList:
            item=item.replace("FUNC",self.func)
            item=item.replace("variables",variables)
            item=item.replace("constraints",constraints)
            item=item.replace("otherVariables",otherVariables)
            testList.append(item)
        
        testFile=open(self.testFilePath,"w+")
        testFile.seek(0)
        testFile.truncate()
        testFile.writelines(testList)
        testFile.close()


    def scriptProtoReading(self,variables):
        func=self.func
        scriptProtoFile=open(self.protoScriptPath,"r")
        scriptProtoList=scriptProtoFile.readlines()
        scriptProtoFile.close()

        scriptList=[]
        for item in scriptProtoList:
            item=item.replace("FUNC",func)
            item=item.replace("variables",variables)
            scriptList.append(item)
        
        scriptFile=open(self.testScriptPath,"w+")
        scriptFile.seek(0)
        scriptFile.truncate()
        scriptFile.writelines(scriptList)
        scriptFile.close()

    def ExecuteCommand(self):
        
        p1 = Popen(self.compileCommand, shell=True, stdout=PIPE, stderr=PIPE)
        compileResult, stderr=p1.communicate()
        if(stderr):
            print("FATAL: error with compilation")
            print(stderr.decode('utf-8'))
            exit(0)
        p2 = Popen(self.jpfRunCommand, shell=True, stdout=PIPE, stderr=PIPE)
        SEResult,stderr=p2.communicate()
        if(stderr):
            print("Warning: error with SE run")
            stderr=stderr.decode('utf-8')
            print("WARNING ERROR: %s",stderr)
            self.resultFile.write(stderr)
        compileResult = compileResult.decode("utf-8")
        SEResult = SEResult.decode("utf-8")
        if(STORE_RESULT):
            self.procedureFile.write(SEResult)
        return compileResult,SEResult

    def findSolution(self,result):
        """
        used in checkResult
        """
        solutionList=[]
        result=result.split("\n")
        for line in result:
            if(line.find("Method Summaries (HTML)")!=-1):
                break
            if(line.find("Return Value")!=-1):
                start=line.find("(")
                end=line.find(")")
                solution=line[start+1:end]
                solutionList.append(float(solution))
        return solutionList

    def CheckResult(self,result,SATStatus,solution,constraints):
        if(~ result.find("Correct Find Path") ^ SATStatus):
            # check SAT status
            print("INFO: SAT status Correct with FUNC= %s, constraints %s\n" % (self.func, constraints))
            checkResult="%s: SAT Correct "%(constraints)
            solution=float(solution)
            #check solution
            solutionList=self.findSolution(result)
            for item in solutionList:
                error=abs(solution-item)
                if(error < 0.001):
                    checkResult+=" , Solution Correct \n"
                    self.resultFile.write(checkResult)
                    self.counter+=1
                    return 
            checkResult+=" Solution InCorrect with solution %s \n" %(" ".join(str(elem) for elem in solutionList))
            self.resultFile.write(checkResult)
            return
        else:
            print("INFO: SAT status wrong with FUNC= %s, constraints %s \n" % (self.func, constraints))
            checkResult="%s: SAT Incorrect\n"%(constraints)
            self.resultFile.write(checkResult)
            return
    
    def getTestArgs(self,num):
        variables="double x"
        otherVariables="12"
        jpfVariables="sym"
        for i in range(num-1):
            variables +=",double {}".format(letters[i+1])
            otherVariables +=",12"
            jpfVariables +="#sym"
        return(variables, otherVariables,jpfVariables)
    
    def test0(self,formulaSolutionPair):
        
        constraint=formulaSolutionPair[0]
        solution=formulaSolutionPair[1]
        (variables, otherVariables,jpfVariables)=self.getTestArgs(1)
        self.SEProtoReading(variables,constraint,otherVariables)
        _,result=self.ExecuteCommand()

        if(formulaSolutionPair[1]=="UNSAT"):
            SATStatus=False
        else:
            SATStatus=True
        self.CheckResult(result,SATStatus,solution,constraint)

    
    def readFormula(self,ifFusion="NOFusion"):
        SATInputPath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/formatRecipe/SAT"
        UNSATInputPath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/formatRecipe/UNSAT"
        SATInputFile=open(SATInputPath, 'r')
        UNSATInputFile=open(UNSATInputPath, 'r')
        self.SATFormulaSolutionPairList=[]
        self.UNSATFormulaSolutionPairList=[]
        
        for line in SATInputFile.readlines():
            formula,solution = line.split(",")
            if(ifFusion=="NOFusion"):
                formula=formula.replace("#","x")
            solution=solution[:-1] # remove \n
            self.SATFormulaSolutionPairList.append((formula,solution))
        
        for line in UNSATInputFile.readlines():
            formula,solution = line.split(",")
            if(ifFusion=="NOFusion"):
                formula=formula.replace("#","x")
            solution=solution[:-1] # remove \n
            self.UNSATFormulaSolutionPairList.append((formula,solution))
        
        SATInputFile.close()
        UNSATInputFile.close()
    
    def test(self):
        self.readFormula()
        # only test SAT
        (variables, otherVariables,jpfVariables)=self.getTestArgs(1)
        self.scriptProtoReading(variables)
        # test SAT File
        self.resultFile = open(self.resultFilePath,"w+")
        if(STORE_RESULT):
            self.procedureFile=open(self.procedurePath,"w+")
        for formulaSolutionPair in self.SATFormulaSolutionPairList:
            self.test0(formulaSolutionPair)
            self.totalCounter=self.totalCounter+1
        
        funcResult="{func}, {total} in total tested, {correct} correct\n".format(func=self.func,total=self.totalCounter,correct=self.correctCounter)
        self.resultFile.write(funcResult)
        self.resultFile.close()
        if(STORE_RESULT):
            self.procedureFile.close()
a=SymSEtest("log")
a.test()