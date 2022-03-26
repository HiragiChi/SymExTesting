'''
Coding procedure
1. run math function in java
2. collect result
read command line result
3. fuzzer run
JPF test program. change a value.
jpf file not changed. 
4. collect result
'''

'''
MODE EXPLAINATION:
    TEST:generate testing java and jpf files
    CLEAN:clean all the file generated
'''

'''
origin   --stands for original implementation
'''
import os
import random
import time
from subprocess import PIPE, Popen

def mathInputGenerator(num):
    inputList=random.sample(range(1, 1000), num)
    return inputList

def deleteAllFiles():
    SEDeleteCommand="cd "+SEPath+" && rm SETest* "
    protoDeleteCommand="cd "+protoPath+" && rm math*.java && rm math_*.jpf"
    os.system(SEDeleteCommand)
    os.system(protoDeleteCommand)
    print("All generated test files have been deleted")
    if(MODE=="CLEAN"):
        exit(0)

def SEProtoReading(protoSEPath,testFilePath,FUNC,variables,constraints,otherVariables):
    protoSE=open(protoSEPath, 'r')
    protoSEList=[]
    for line in protoSE.readlines():
        protoSEList.append(line)
    protoSE.close()

    testList=[]
    for item in protoSEList:
        item=item.replace("FUNC",FUNC)
        item=item.replace("variables",variables)
        item=item.replace("constraints",constraints)
        item=item.replace("otherVariables",otherVariables)
        testList.append(item)
    
    testFile=open(testFilePath,"w+")
    testFile.seek(0)
    testFile.truncate()
    testFile.writelines(testList)
    testFile.close()

def scriptProtoReading(scriptProtoPath,scriptPath,FUNC,variables):
    scriptProtoFile=open(scriptProtoPath,"r")
    scriptProtoList=scriptProtoFile.readlines()
    scriptProtoFile.close()

    scriptList=[]
    for item in scriptProtoList:
        item=item.replace("FUNC",FUNC)
        item=item.replace("variables",variables)
        scriptList.append(item)
    
    scriptFile=open(scriptPath,"w+")
    scriptFile.seek(0)
    scriptFile.truncate()
    scriptFile.writelines(scriptList)
    scriptFile.close()


def ExecuteCommand(compileCommand,runCommand):
    p1 = Popen(compileCommand, shell=True, stdout=PIPE, stderr=PIPE)
    compileResult, stderr=p1.communicate()
    if(stderr):
        print("FATAL: error with compilation")
        exit(0)
    p2 = Popen(runCommand, shell=True, stdout=PIPE, stderr=PIPE)
    SEResult,stderr=p2.communicate()
    if(stderr):
        print("FATAL: error with SE run")
        exit(0)
    compileResult = compileResult.decode("utf-8")
    SEResult = SEResult.decode("utf-8")
    return compileResult,SEResult

def findSolution(result):
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

def CheckResult(result,resultFile,SATStatus,solution,FUNC,constraints,counter):
    if(~ result.find("Correct Find Path") ^ SATStatus):
        # check SAT status
        print("INFO: SAT status Correct with FUNC= %s, constraints %s" % (FUNC, constraints))
        checkResult="%s: SAT Correct "%(constraints)
        
        #check solution
        solutionList=findSolution(result)
        for item in solutionList:
            error=abs(solution-item)
            if(error < 0.001):
                checkResult+=" , Solution Correct \n"
                resultFile.write(checkResult)
                counter+=1
                return
        checkResult+=" Solution InCorrect with solution %s \n" %(" ".join(str(elem) for elem in solutionList))
        resultFile.write(checkResult)
        return
    else:
        print("INFO: SAT status wrong with FUNC= %s, constraints %s" % (FUNC, constraints))
        checkResult="%s: SAT Incorrect\n"%(constraints)
        resultFile.write(checkResult)
        return 
    # check if result is correct
       

def test():
    protoSEPath=protoPath+"/testCase.java.prototype.new"
    testFilePath=SEPath+"/SETest_log.java"
    protoScriptPath=protoPath+'/proto.jpf'
    testScriptPath=protoPath+'/SETest_log.jpf'
    FUNC="log"
    # outputCommand=" > "+ resultPath +"/result"
    outputCommand=""
    compileCommand="javac -d /home/hiragi/Desktop/jpf/jpf-symbc/build/examples -g /home/hiragi/Desktop/jpf/jpf-symbc/src/examples/SETest_{FUNC}.java".format(FUNC=FUNC) + outputCommand
    jpfRunCommand="/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Xmx1024m -ea -Dfile.encoding=UTF-8 -classpath /home/hiragi/Desktop/jpf/jpf-core/build/main:/home/hiragi/Desktop/jpf/jpf-core/build/peers:/home/hiragi/Desktop/jpf/jpf-core/build/classes:/home/hiragi/Desktop/jpf/jpf-core/build/annotations:/home/hiragi/Desktop/jpf/jpf-core/build/examples:/home/hiragi/Desktop/jpf/jpf-core/build/tests:/home/hiragi/Desktop/jpf/jpf-core/build:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/main:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/peers:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/lib/*:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/tests:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/examples gov.nasa.jpf.tool.RunJPF /home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf".format(FUNC=FUNC) + outputCommand

    SEProtoReading(protoSEPath, testFilePath,"log","double x","x>1","12")
    scriptProtoReading(protoScriptPath,testScriptPath,"log","sym")
    resultFile=open(resultPath,"w+")
    _,result=ExecuteCommand(compileCommand,jpfRunCommand)
    counter=0
    CheckResult(result,resultFile,True,1,"log","x>1",counter)

MODE= "RETEST"
RUNJPF=True
# MODE= "CLEAN"

funcList=['sqrt','abs','log','tan','sin','cos']
funcList1=['log']
funcList=funcList1

# protoOriginPath=protoPath+"/mathOrigin.java.prototype"
protoPath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/inputGeneration/prototypes"
resultPath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/result/result"
SEPath="/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/"


# if (MODE!="TEST"):
#     deleteAllFiles()
test()
exit(0)

recordFileName="correctRecord.txt"
recordFilePath=protoPath+"/subFolder/"+recordFileName
recordFile=open(recordFilePath,"w+")
# delete generated file



### File Reading Part

# origin file read
# protoOrigin=open(protoOriginPath,'r')
# protoOriginList=[]
# for line in protoOrigin.readlines():
#     protoOriginList.append(line)
# protoOrigin.close()


#generate testCase and jpf file
protoSEPath=protoPath+"/testCase.java.prototype"
protoSE=open(protoSEPath, 'r')
protoSEList=[]
for line in protoSE.readlines():
    protoSEList.append(line)
protoSE.close()


protoJPFPath=protoPath+"/proto.jpf"
protoJPF=open(protoJPFPath,'r')
protoJPFList=[]
for line in protoJPF.readlines():
    protoJPFList.append(line)


# for each function change file 

# original
lineOfInput=[]
for FUNC in funcList:
    SEFileName="SETest_"+FUNC+".java"
    recordFile.write("\n"+FUNC+'\n\n')

    # originList=[]
    # for i in range(len(protoOriginList)):
    #     originList.append( protoOriginList[i].replace("FUNC",FUNC))


    # originFilePath=protoPath+"/math"+"_"+FUNC+".java"
    # originFile=open(originFilePath,'w+')


    # SE test file
    SEList=[]
    # SEFilePath=SEPath+"/SETest_{}.java".format(FUNC)
    SEFilePath=SEPath+"/"+SEFileName
    SEFile=open(SEFilePath, 'w+')
    for i in range(len(protoSEList)):
        SEList.append(protoSEList[i].replace("FUNC",FUNC))
        inputPlace=protoSEList[i].find("input")
        if(inputPlace!=-1):
            lineOfInput.append(i)
            



    #  jpf file
    JPFFilePath=protoPath+"/math_"+FUNC+".jpf"
    JPFList=[]
    for item in protoJPFList:
        item=item.replace("FUNC",("SETest_"+FUNC))
        JPFList.append(item)
    JPFFile=open(JPFFilePath, "w+")
    JPFFile.writelines(JPFList)
    JPFFile.close()

    # set run config
    outputCommandNoUse=" >> /home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/subFolder/junk"
    outputCommand="> /home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/subFolder/result"
    jpfRunCommand="/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Xmx1024m -ea -Dfile.encoding=UTF-8 -classpath /home/hiragi/Desktop/jpf/jpf-core/build/main:/home/hiragi/Desktop/jpf/jpf-core/build/peers:/home/hiragi/Desktop/jpf/jpf-core/build/classes:/home/hiragi/Desktop/jpf/jpf-core/build/annotations:/home/hiragi/Desktop/jpf/jpf-core/build/examples:/home/hiragi/Desktop/jpf/jpf-core/build/tests:/home/hiragi/Desktop/jpf/jpf-core/build:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/main:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/peers:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/lib/*:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/tests:/home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf/build/examples gov.nasa.jpf.tool.RunJPF /home/hiragi/Desktop/jpf/jpf-symbc/src/examples/mytest_SE/math_{FUNC}.jpf".format(FUNC=FUNC)+ outputCommand
    runCommand="/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Dfile.encoding=UTF-8 -classpath /home/hiragi/Desktop/jpf/jpf-symbc/build/main:/home/hiragi/Desktop/jpf/jpf-symbc/build/annotations:/home/hiragi/Desktop/jpf/jpf-symbc/build/examples:/home/hiragi/Desktop/jpf/jpf-symbc/build/peers:/home/hiragi/Desktop/jpf/jpf-symbc/build/tests:/home/hiragi/Desktop/jpf/jpf-symbc/build/classes:/home/hiragi/Desktop/jpf/jpf-core/build/main:/home/hiragi/Desktop/jpf/jpf-core/build/peers:/home/hiragi/Desktop/jpf/jpf-core/build/classes:/home/hiragi/Desktop/jpf/jpf-core/build/annotations:/home/hiragi/Desktop/jpf/jpf-core/build/examples:/home/hiragi/Desktop/jpf/jpf-core/build/tests:/home/hiragi/Desktop/jpf/jpf-symbc/lib/grappa.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/aima-core.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/automaton.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/bcel.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/choco-1_2_04.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/choco-solver-2.1.1-20100709.142532-2.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/com.microsoft.z3.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/commons-lang-2.4.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/commons-math-1.2.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/coral.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/green.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/hampi.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/iasolver.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/jaxen.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/jedis-2.0.0.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/JSAP-2.1.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/libcvc3.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/opt4j-2.4.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/org.sat4j.core.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/org.sat4j.pb.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/scale.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/solver.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/Statemachines.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/STPJNI.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/string.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/yicesapijava.jar:/snap/eclipse/48/plugins/org.junit_4.12.0.v201504281640/junit.jar:/snap/eclipse/48/plugins/org.hamcrest.core_1.3.0.v20180420-1519.jar:/home/hiragi/Desktop/jpf/jpf-symbc/lib/proteus.jar mytest_SE.math_"+FUNC
    buildCommand="ant -f /home/hiragi/Desktop/jpf/jpf-symbc/build.xml"+outputCommandNoUse
    buildCommand2="ant -f /home/hiragi/Desktop/jpf/jpf-core/build.xml"+outputCommandNoUse
    deleteCommand="rm -f /home/hiragi/Desktop/jpf/jpf-symbc/build/examples/SE*.class"+outputCommandNoUse
    compileCommand="javac -d /home/hiragi/Desktop/jpf/jpf-symbc/build/examples -g /home/hiragi/Desktop/jpf/jpf-symbc/src/examples/SETest_{FUNC}.java".format(FUNC=FUNC)
    # testCommand="java /home/hiragi/Desktop/jpf/jpf-symbc/build/examples/SETest_{FUNC}".format(FUNC=FUNC)
    # testCommandWithCd="cd ~/Desktop/jpf/jpf-symbc/build/examples && java SETest_log"
    ifPathFind=False
    correctNum=0
    errorNum=0

    # # generate random inputs (how can I change the value)?

    """
    to do: change the inputNum to list
    run realistic command
    """
    randomList = mathInputGenerator(1)
    # for i in range(len(randomList)):
    #     randomList[i] = randomList[i]/100


    for inputNum in randomList:
        SEFile=open(SEFilePath, 'w+')
        # originFile=open(originFilePath,'w+')
        testOriginList=[]
        testSEList=[]
        # generate test list to avoid polluting the original list
        # for i in range(len(originList)):
        #     testOriginList.append(originList[i])
        for i in range(len(SEList)):
            testSEList.append(SEList[i])
        testOriginList[5]=testOriginList[5].replace("input",str(inputNum))
        for i in lineOfInput:
            testSEList[i]=testSEList[i].replace("input",str(inputNum))
        # originFile.seek(0)
        SEFile.seek(0)
        # originFile.truncate()
        SEFile.truncate()

        # originFile.writelines(testOriginList)
        SEFile.writelines(testSEList)
        #  run the java file and generate result

        ## originResultFile=os.popen(runCommand)
        # buildResult=os.system(buildCommand)
        # originFile.close()
        SEFile.close()

        # os.system(testCommandWithCd)

        # # '''
        # # testing cause:print build
        # # '''
        # # for line in buildResult.readlines():
        # #     print(line,end="")
        
        os.system(jpfRunCommand)
        
        if (RUNJPF):
            jpfResultFile=open(protoPath+"/subFolder/result")
            # judge
            ifPathFind=False
            print("test\n\n\n")
            os.system(testCommandWithCd)
            print("test\n\n\n")
            for line in jpfResultFile.readlines():
                print(line,end="")
                if(line.find("Correct Find Path"))!=-1:
                    correctNum+=1
                    ifPathFind=True
                    record=" "+FUNC+"   "+str(inputNum)+"\n"
                    recordFile.write(record)
                    print("I Found it!")
                    # break
            if(not ifPathFind):
                record=" "+FUNC+"   "+str(inputNum)+" Not successfully tested\n"
                recordFile.write(record)
                print("not Found!")
                errorNum+=1


    recordFile.write(FUNC+" correctly find: {}, fail to find {}\n".format(correctNum,errorNum))
    print(FUNC+" correctly find: {}, fail to find {}\n".format(correctNum,errorNum))






