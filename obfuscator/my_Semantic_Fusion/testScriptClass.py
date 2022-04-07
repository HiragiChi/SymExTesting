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
    def __init__(self,func,argNum,round):
        self.func=func
        self.round=round
        self.argNum=argNum
        self.totalCounter=0
        self.correctCounter=0

        protoPath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/inputGeneration/prototypes"
        self.jpfPath="/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE"
        self.resultFilePath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/result/result"
        self.procedurePath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/result/procedure"
        SEPath="/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/"

        compileCommand0="javac -d /home/hiragi/Desktop/jpf/jpf-symbc/build/examples -g /home/hiragi/Desktop/jpf/jpf-symbc/src/examples/SETest_{FUNC}.java"
        jpfRunCommand0="/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Xmx1024m -ea -Dfile.encoding=UTF-8 -classpath /home/hiragi/Desktop/jpf/jpf-core/build/main:/home/hiragi/Desktop/jpf/jpf-core/build/peers:/home/hiragi/Desktop/jpf/jpf-core/build/classes:/home/hiragi/Desktop/jpf/jpf-core/build/annotations:/home/hiragi/Desktop/jpf/jpf-core/build/examples:/home/hiragi/Desktop/jpf/jpf-core/build/tests:/home/hiragi/Desktop/jpf/jpf-core/build:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/main:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/peers:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/lib/*:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/tests:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/examples gov.nasa.jpf.tool.RunJPF /home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf"

        self.protoSEPath=protoPath+"/testCase.java.prototype.new"
        testFilePath0=SEPath+"/SETest_{FUNC}.java"
        self.protoScriptPath=protoPath+'/proto.jpf'
        testScriptPath0=self.jpfPath+'/math_{FUNC}.jpf'

        
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


    def scriptProtoReading(self,jpfVariables):
        func=self.func
        scriptProtoFile=open(self.protoScriptPath,"r")
        scriptProtoList=scriptProtoFile.readlines()
        scriptProtoFile.close()

        scriptList=[]
        for item in scriptProtoList:
            item=item.replace("FUNC",func)
            item=item.replace("variables",jpfVariables)
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

    def findGroundTruth(self,input):

        """
        no use
        """
        originalProtoFile=open("/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/inputGeneration/prototypes/mathOrigin.java.prototype","r")
        originalTestLines=[]
        for line in originalProtoFile.readlines():
            line=line.replace("FUNC",self.func)
            line=line.replace("input",input)
            originalTestLines.append(line)

        originalTestPath=self.jpfPath+"/math_{func}.java".format(func=self.func)
        originalTestFile=open(originalTestPath,"w+")
        originalTestFile.writelines(originalTestLines)
        originalTestFile.close()
        runCommand="/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Dfile.encoding=UTF-8 -classpath /home/hiragi/Desktop/jpf/jpf-symbc/build/main:/home/hiragi/Desktop/jpf/jpf-symbc/build/annotations:/home/hiragi/Desktop/jpf/jpf-symbc/build/examples:/home/hiragi/Desktop/jpf/jpf-symbc/build/peers:/home/hiragi/Desktop/jpf/jpf-symbc/build/tests:/home/hiragi/Desktop/jpf/jpf-symbc/build/classes:/home/hiragi/Desktop/jpf/jpf-core/build/main:/home/hiragi/Desktop/jpf/jpf-core/build/peers:/home/hiragi/Desktop/jpf/jpf-core/build/classes:/home/hiragi/Desktop/jpf/jpf-core/build/annotations:/home/hiragi/Desktop/jpf/jpf-core/build/examples:/home/hiragi/Desktop/jpf/jpf-core/build/tests:/home/hiragi/Desktop/jpf/jpf-symbc/lib/grappa.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/aima-core.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/automaton.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/bcel.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/choco-1_2_04.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/choco-solver-2.1.1-20100709.142532-2.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/com.microsoft.z3.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/commons-lang-2.4.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/commons-math-1.2.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/coral.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/green.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/hampi.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/iasolver.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/jaxen.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/jedis-2.0.0.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/JSAP-2.1.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/libcvc3.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/opt4j-2.4.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/org.sat4j.core.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/org.sat4j.pb.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/scale.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/solver.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/Statemachines.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/STPJNI.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/string.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/yicesapijava.jar:/snap/eclipse/48/plugins/org.junit_4.12.0.v201504281640/junit.jar:/snap/eclipse/48/plugins/org.hamcrest.core_1.3.0.v20180420-1519.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/proteus.jar mytest_SE.math_{func}".format(func=self.func)
        p1 = Popen(runCommand, shell=True, stdout=PIPE, stderr=PIPE)
        result, stderr=p1.communicate()
        result=result.decode("utf-8")
        return float(result)

    def checkSolution(self,constraint,solutions):
        originalProtoFile=open("/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/inputGeneration/prototypes/mathOrigin.java.proto2","r")
        originalTestLines=[]
        # solutions are str
        iterNum=0

        for solution in solutions:
            for item in solution:
                solutionNum=float(item)
                solutionNum=round(solutionNum,2)
                item=str(solutionNum)
                letter=letters[iterNum]
                if(constraint.find(letter)):
                    constraint=constraint.replace(letter,item)
                    iterNum+=1
        for line in originalProtoFile.readlines():
            line=line.replace("FUNC",self.func)
            line=line.replace("constraints",constraint)
            originalTestLines.append(line)

        originalTestPath=self.jpfPath+"/math_{func}.java".format(func=self.func)
        originalTestFile=open(originalTestPath,"w+")
        originalTestFile.writelines(originalTestLines)
        originalTestFile.close()
        runCommand="/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Dfile.encoding=UTF-8 -classpath /home/hiragi/Desktop/jpf/jpf-symbc/build/main:/home/hiragi/Desktop/jpf/jpf-symbc/build/annotations:/home/hiragi/Desktop/jpf/jpf-symbc/build/examples:/home/hiragi/Desktop/jpf/jpf-symbc/build/peers:/home/hiragi/Desktop/jpf/jpf-symbc/build/tests:/home/hiragi/Desktop/jpf/jpf-symbc/build/classes:/home/hiragi/Desktop/jpf/jpf-core/build/main:/home/hiragi/Desktop/jpf/jpf-core/build/peers:/home/hiragi/Desktop/jpf/jpf-core/build/classes:/home/hiragi/Desktop/jpf/jpf-core/build/annotations:/home/hiragi/Desktop/jpf/jpf-core/build/examples:/home/hiragi/Desktop/jpf/jpf-core/build/tests:/home/hiragi/Desktop/jpf/jpf-symbc/lib/grappa.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/aima-core.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/automaton.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/bcel.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/choco-1_2_04.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/choco-solver-2.1.1-20100709.142532-2.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/com.microsoft.z3.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/commons-lang-2.4.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/commons-math-1.2.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/coral.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/green.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/hampi.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/iasolver.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/jaxen.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/jedis-2.0.0.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/JSAP-2.1.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/libcvc3.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/opt4j-2.4.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/org.sat4j.core.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/org.sat4j.pb.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/scale.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/solver.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/Statemachines.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/STPJNI.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/string.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/yicesapijava.jar:/snap/eclipse/48/plugins/org.junit_4.12.0.v201504281640/junit.jar:/snap/eclipse/48/plugins/org.hamcrest.core_1.3.0.v20180420-1519.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/proteus.jar mytest_SE.math_{func}".format(func=self.func)
        p1 = Popen(runCommand, shell=True, stdout=PIPE, stderr=PIPE)
        result, stderr=p1.communicate()
        result=result.decode("utf-8")
        return result[:-1] #remove \n

    def findSESolution(self,result):
        """
        used in checkResult
        """
        solutionList=[]
        result=result.split("\n")
        for line in result:
            if(line.find("Method Summaries (HTML)")!=-1):
                break
            if(line.find("Return Value: 1")!=-1):
                start=line.find("(")
                end=line.find(")")
                solution=line[start+1:end]
                
                solution=solution.split(",")
                print("solution: ", solution)
                solutionList.append(solution)
        return solutionList

    def CheckResult(self,result,SATStatus,constraints):
        """
        using check solution
        """
        if(not ((result.find("Correct Find Path")!=-1) ^ SATStatus)):
            # check SAT status
            print("INFO: SAT status Correct with FUNC= %s, constraints %s\n" % (self.func, constraints))
            checkResult="%s: SAT Correct "%(constraints)
            #check solution
            solutionList=self.findSESolution(result)
            ifCorrect=self.checkSolution(constraints,solutionList)
            if(ifCorrect=="True"):
                checkResult+=" , Solution Correct \n"
                self.correctCounter+=1
            else:
                checkResult+=" Solution InCorrect with solution %s.\n" %(" ".join(str(elem) for elem in solutionList))
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
        (variables, otherVariables,jpfVariables)=self.getTestArgs(self.argNum)
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
            formula,solution, boundary = line.split(",")
            if(ifFusion=="NOFusion"):
                formula=formula.replace("#","x")
            boundary=boundary[:-1] # remove \n
            self.SATFormulaSolutionPairList.append((formula,boundary))
        
        for line in UNSATInputFile.readlines():
            formula,solution,boundary = line.split(",")
            if(ifFusion=="NOFusion"):
                formula=formula.replace("#","x")
            # remove \n
            print(solution)
            self.UNSATFormulaSolutionPairList.append((formula,solution))
        
        SATInputFile.close()
        UNSATInputFile.close()
    
    def normalFormulaTest(self):
        self.readFormula()
        # only test SAT
        (variables, otherVariables,jpfVariables)=self.getTestArgs(self.argNum)
        self.scriptProtoReading(jpfVariables)
        # test SAT File
        self.resultFile = open(self.resultFilePath,"a")
        if(STORE_RESULT):
            self.procedureFile=open(self.procedurePath,"a")
        for formulaSolutionPair in self.SATFormulaSolutionPairList:
            self.test0(formulaSolutionPair)
            self.totalCounter=self.totalCounter+1
        
        funcResult="{func}, {total} in total tested, {correct} correct\n".format(func=self.func,total=self.totalCounter,correct=self.correctCounter)
        self.resultFile.write(funcResult)
        self.resultFile.close()
        if(STORE_RESULT):
            self.procedureFile.close()


    def unitTest0(self,input,mode):
        """
        input=numbers 1.1,52.3
        args= x,y 
        """
        args="("
        for i in range(self.argNum):
            args+=letters[i]+","
        args=args[:-1]
        args+=")"
        if (mode == 1):
            constraint="Math.{func}{args}==Math.{func}({x})".format(func=self.func,x=input,args=args)
        elif(mode == 2):
            constraint="x==Math.{func}({x})".format(func=self.func,x=input,args=args)
        (variables, otherVariables,jpfVariables)=self.getTestArgs(self.argNum)
        self.SEProtoReading(variables,constraint,otherVariables)
        _,result=self.ExecuteCommand()
        SATStatus=True
        self.CheckResult(result,SATStatus,constraint)

    def unitTest(self,mode):
        (variables, otherVariables,jpfVariables)=self.getTestArgs(self.argNum)
        self.scriptProtoReading(jpfVariables)
        self.resultFile = open(self.resultFilePath,"a")
        if(STORE_RESULT):
            self.procedureFile=open(self.procedurePath,"a")

        ## change for each test
        for i in range(self.round):
            input=[]
            for i in range(self.argNum):
                input.append(str(round(random.uniform(1,100),2)))
            print(input)
            input=",".join(input)
            print(input)
            self.unitTest0(input,mode)
            self.totalCounter=self.totalCounter+1
        
        funcResult="{func}, {total} in total tested, {correct} correct\n".format(func=self.func,total=self.totalCounter,correct=self.correctCounter)
        self.resultFile.write(funcResult)
        self.resultFile.close()
        if(STORE_RESULT):
            self.procedureFile.close()

SEDeleteCommand="cd ~/Desktop/jpf/obfuscator/my_Semantic_Fusion/result" +"&& rm -rf * "
def unitTestAll():
   
    os.system(SEDeleteCommand)
    funcList=["log1","atan22","tan1","cos1","sin1","pow2"]
    for item in funcList:
        argNum=int(item[-1])
        item=item[:-1]
        test=SymSEtest(item,argNum,1)    
        test.unitTest(2)
unitTestAll()