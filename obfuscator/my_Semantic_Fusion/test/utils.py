# statistics
path="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/APermanentResult/UnitTest/result_MODE{mode}.txt"

templateLine="| {name} |  {correct} |  {found}   | {notfound} |\n"
for mode in [1,2,3]:
    template="""
MODE{mode}  
|    function name    | correct solved | constraint found | constraint not found|
| ---------- | --- | --- | --- | --- |
""".format(mode=mode)
    modePath=path.format(mode=mode)
    resultFile = open(modePath, 'r')
    correct=0
    found=0
    notfound=0
    for line in resultFile.readlines():
        if(line.find("no path condition found")!=-1):
            notfound+=1
        elif(line.find("SAT Correct")!=-1):
            correct+=1
        elif(line.find("SAT Incorrect")!=-1):
            found+=1

        if(line.find("50 in total tested")!=-1):
            funcName=line.split(",")[0]
            resultLine=templateLine.format(name=funcName,correct=correct,found=found,notfound=notfound)
            template+=resultLine
            correct=0
            found=0
            notfound=0
    print(template)