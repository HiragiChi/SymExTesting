import os
import random
import time
from subprocess import PIPE, Popen
from easyFusion import fusion,fusionFunc2,formulaTemplate
RUNJPF=True

STORE_RESULT=True
letters=["X","Y","Z","A","B","C"]

def mathInputGenerator(num):
    inputList=random.sample(range(1, 1000), num)
    return inputList
class SymSEtest():

    def __init__(self,func,argNum):
        """
        func
        """
        self.func=func
        self.argNum=argNum
        self.totalCounter=0
        self.correctCounter=0

        protoPath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/inputGeneration/prototypes"
        self.jpfPath="/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE"
        self.resultFilePath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/result/result{text}.txt"
        self.procedurePath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/result/procedure{text}.txt"
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
    

    def findGroundTruth(self,input):

        """
        used in fusion -> to get solution
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


    def checkConstraint0(self,constraints):
        """
           
        """
        # this is a comment
        formulas=constraints.split("&")
        template="abs({left}-{right})"
        testFormulas=[]
        for formula in formulas:
            bothSide=formula.split("==")
            testFormula=template.format(left=bothSide[0],right=bothSide[1])
            testFormulas.append(testFormula)
        testFinal="+".join(testFormulas)
        testFinal=testFinal+"< 0.01"

    def checkSolution(self,constraint,solutions):
        """

        """

        originalProtoFile=open("/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/inputGeneration/prototypes/mathOrigin.java.proto2","r")
        originalTestLines=[]
        # solutions are str
        iterNum=0
        resultList=[]
        for solution in solutions:
            iterNum=0
            for item in solution:
                solutionNum=float(item)
                # solutionNum=round(solutionNum,2)
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
            resultList.append(result[:-1])
        return resultList #remove \n

    def findSESolution(self,result):
        """
        used in checkResult
        extract solution from SE results
        """
        solutionList=[]
        result=result.split("\n")
        for line in result:
            if(line.find("Method Summaries (HTML)")!=-1):
                break
            if(line.find("Return Value: 1")!=-1):
                """
                """
                line=line.replace("-9223372036854775808(don't care)","1")
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
        check if the result from SE is correct
        """
        if(not ((result.find("Correct Find Path")!=-1) ^ SATStatus)):
            self.correctCounter+=1 # had not solved the little inaccuracy problem of solution
            # check SAT status
            print("INFO: SAT status Correct with FUNC= %s, constraints %s\n" % (self.func, constraints))
            checkResult="%s: SAT Correct "%(constraints)
            #check solution
            solutionList=self.findSESolution(result)
            ifCorrect=self.checkSolution(constraints,solutionList)
            if("True" in ifCorrect):
                checkResult+=" , Solution Correct with solution %s.\n"%(" ".join(str(elem) for elem in solutionList))
                
            else:
                checkResult+=" Solution InCorrect with solution %s.\n" %(" ".join(str(elem) for elem in solutionList))
            self.resultFile.write(checkResult)
            return
        else:
            if(result.find("No path conditions for SETest")!=-1):
                print("INFO: No path conditions found with FUNC= %s, constraints %s \n" % (self.func, constraints))
                checkResult="%s: no path condition found\n"%(constraints)
            else:
                print("INFO: SAT status wrong with FUNC= %s, constraints %s \n" % (self.func, constraints))
                checkResult="%s: SAT Incorrect\n"%(constraints)
            self.resultFile.write(checkResult)
            return
    
    def getTestArgs(self,num):
        variables="double X"
        otherVariables="1"
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
                formula=formula.replace("#","X")
            boundary=boundary[:-1] # remove \n
            self.SATFormulaSolutionPairList.append((formula,boundary))
        
        for line in UNSATInputFile.readlines():
            formula,solution,boundary = line.split(",")
            if(ifFusion=="NOFusion"):
                formula=formula.replace("#","X")
            # remove \n
            print(solution)
            self.UNSATFormulaSolutionPairList.append((formula,solution))
        
        SATInputFile.close()
        UNSATInputFile.close()
    
    def normalFormulaTest(self):
        ##cannot 
        self.readFormula()
        # only test SAT
        (variables, otherVariables,jpfVariables)=self.getTestArgs(self.argNum)
        self.scriptProtoReading(jpfVariables)
        # test SAT File
        self.resultFilePath=self.resultFilePath.format(text="")
        self.procedurePath=self.procedurePath.format(text="")
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

    def unitConstraintGeneration(self,func,mode,input,argNum):
        args="("
        for i in range(argNum):
            args+=letters[i]+","
        args=args[:-1]
        args+=")"
        if (mode == 1 or mode == 2):
            constraint="Math.{func}{args}==({x})".format(func=func,x=input,args=args)
        elif(mode == 3):
            constraint="X==Math.{func}({x})".format(func=func,x=input,args=args)
        elif(mode == 4):
            constraint="Math.{func}{args}==Math.{func}({x})".format(func=func,x=input,args=args)
        return constraint

    def inputGeneration(self,mode,func,inputNum,inputRange):
        """
        Generate input for constraint
        mode=1,2,3
        func="log"
        inputNum: number of parameters of function
        inputRange:[1,100]
        """
        onlyIntList=["round","ceil","floor","rint"]
        input=[]
        start=inputRange[0]
        end=inputRange[1]
        for i in range(inputNum):
            if(mode ==1 or func in onlyIntList):
                start=round(start)
                end=round(end)
                input.append(str(random.randint(start,end)))
            else:
                input.append(str(round(random.uniform(start,end),2)))
        input=",".join(input)
        return input

    def unitTest0(self,input):
        """
        input=string 1.1,52.3
        args= x,y 
        """
        mode=self.mode
        constraint=self.unitConstraintGeneration(self.func,mode,input,self.argNum)

        (variables, otherVariables,jpfVariables)=self.getTestArgs(self.argNum)
        self.SEProtoReading(variables,constraint,otherVariables)
        _,result=self.ExecuteCommand()
        SATStatus=True
        self.CheckResult(result,SATStatus,constraint)

    def unitTest(self,mode,testRound,inputRange=[1,100],other=None):
        """
        mode=1 -> math.atan2(x,y)==integer
        mode=2 -> math.atan2(x,y)==float
        mode=3 -> x==math.atan2(a,b)

        generate input value and do unit test
        """
        self.mode=mode
        self.round=testRound
        if (mode ==1 or mode==2):
            inputNum=1
        elif(mode ==3):
            inputNum=self.argNum
            self.argNum=1
        
        (variables, otherVariables,jpfVariables)=self.getTestArgs(self.argNum)
        self.scriptProtoReading(jpfVariables)
        self.resultFilePath=self.resultFilePath.format(text="_MODE%d"%mode)
        self.procedurePath=self.procedurePath.format(text="_MODE%d"%mode)
        self.resultFile = open(self.resultFilePath,"a")
        if(STORE_RESULT):
            self.procedureFile=open(self.procedurePath,"a")

        #specialDef:
        onlyIntList=["round","ceil","floor","rint"]

        ## constraint generation
        for i in range(self.round):
            input=self.inputGeneration(mode,self.func,inputNum,inputRange)
            self.unitTest0(input)
            self.totalCounter=self.totalCounter+1
        
        funcResult="\n{func}, {total} in total tested, {correct} correct\n\n\n".format(func=self.func,total=self.totalCounter,correct=self.correctCounter)
        self.resultFile.write(funcResult)
        self.resultFile.close()
        if(STORE_RESULT):
            self.procedureFile.close()

    def unitFusionTest(self,mode,testRound,funcList):
        """
        a function fuse with other functions
        """ 
        self.round=testRound
        (variables, otherVariables,jpfVariables)=self.getTestArgs(3)
        self.scriptProtoReading(jpfVariables)
        self.resultFilePath=self.resultFilePath.format(text="Fusion")
        self.procedurePath=self.procedurePath.format(text="Fusion")
        self.resultFile = open(self.resultFilePath,"a")
        if(STORE_RESULT):
            self.procedureFile=open(self.procedurePath,"a")


        # unit constraint generation
        onlyIntList=["round","ceil","floor","rint"]
        listLength=len(funcList)
        for i in range(listLength):
            for j in range(i+1,listLength):
                func1=funcList[i]
                func2=funcList[j]
                args1=int(func1[-1])
                func1=func1[:-1]

                args2=int(func2[-1])
                func2=func2[:-1]
                
                input1=self.inputGeneration(mode=mode,func=func1,inputNum=1,inputRange=getRange(func1))
                input2=self.inputGeneration(mode=mode,func=func2,inputNum=1,inputRange=getRange(func2))
                constraint1=self.unitConstraintGeneration(func1,mode,input1,args1)
                constraint2=self.unitConstraintGeneration(func2,mode,input2,args2)    
                constraint1=constraint1.replace("X","#")
                constraint2=constraint2.replace("X","#")
                formula1=formulaTemplate(constraint1,"SAT")
                formula2=formulaTemplate(constraint2,"SAT")
                constraintList=[formula1,formula2]
                #fusion
                constraint=fusion(constraintList,fusionFunc2,"SAT")
                print("current Constraint is %s"%constraint)
                
                # test
                (variables, otherVariables,jpfVariables)=self.getTestArgs(3)
                self.SEProtoReading(variables,constraint,otherVariables)
                _,result=self.ExecuteCommand()
                SATStatus=True
                self.CheckResult(result,SATStatus,constraint)

        
        pass



SEDeleteCommand="cd ~/Desktop/jpf/obfuscator/my_Semantic_Fusion/result" +"&& rm -rf * "

def getRange(functionName):
    "get range of a function(值域)"
    if(functionName=="sin" or functionName=="cos"):
        range=[-1,1]
    elif(functionName in ["atan2","atan","asin","acos"] ):
        range=[-3.14,3.14]
    else:
        range=[0,100]
    return range

def getDomain(functionName):
    if(functionName=="asin" or functionName=="acos"):
        range=[-1,1]
    else:
        range=[0,100]
    return range

def getBoundary(functionName):
    "not implemented yet"
    pass


def unitTestAll():
    os.system(SEDeleteCommand)
    fullFuncList=["sqrt1","exp1","asin1","acos1","atan1","atan22","log1","tan1","sin1","cos1","pow2","abs1","max2","min2","round1","ceil1","floor1","rint1"]
    compensateList=["abs1","max2","min2","round1","ceil1","floor1","rint1"]
    
    for mode in [1,2,3]:
        for item in compensateList:
            # argNum represents how many arguments the "run" function needs.
            # in unit test 2, random input numbers are not in correspondence to argNum
            argNum=int(item[-1])
            funcName=item[:-1]
            test=SymSEtest(funcName,argNum)
            if (mode in [1,2]):
                funcRange=getRange(funcName)
            elif(mode ==3):
                funcRange=getDomain(funcName)    
            test.unitTest(mode=mode,testRound=50,inputRange=funcRange)
def TestSingleFunc():
    os.system(SEDeleteCommand)
    fullFuncList=["sqrt1","exp1","asin1","acos1","atan1","atan22","log1","tan1","sin1","cos1","pow2","abs1","max2","min2","round1","ceil1","floor1","rint1"]
    no2FuncList=["sqrt1","exp1","asin1","acos1","atan1","log1","tan1","sin1","cos1","abs1","round1","ceil1","floor1","rint1"]
    test=SymSEtest("fusion",1)
    a=test.checkSolution("Math.atan((Z-Y))==(0) & Math.abs((Z-X))==(15)",[['627.4131822732661', '642.4131822732661', '642.4131822732661']])
    print(a)

TestSingleFunc()