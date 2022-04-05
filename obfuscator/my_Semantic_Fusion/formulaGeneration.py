import random
import math

"""
has not support generate formula by adding two quadratic formula
"""
SATResultPath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/formatRecipe/SAT"
SATResultFile=open(SATResultPath,"w+")
UNSATResultPath="/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/formatRecipe/UNSAT"
UNSATResultFile=open(UNSATResultPath,"w+")

def solveQuadratic(a,b,c):
    delta=b*b-4*a*c
    if(delta<0):
        return ("quad0",a,b,c)
    elif(delta>0):
        solution1=(-b-math.sqrt(delta))/(2*a)
        solution2=(-b+math.sqrt(delta))/(2*a)
        return("quad1",a,b,c,solution1,solution2)

def generateFormula(formula1,formula2):
    SATFormulas=[]
    UNSATFormulas=[]
    if(formula1[0]=="linear" and formula2[0]=="linear"):
        template="{a1}*#+{b1}{sym1}{c1} & {a2}*#+{b2}{sym2}{c2},{SAT},{solution}\n"
        solution1=formula1[4]
        solution2=formula2[4]
        if(solution1>solution2):
            UNSATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2="<",SAT="UNSAT",solution=None))
            SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2=">",SAT=(solution1+solution2)/2,solution=solution1))
        elif(solution1<solution2):
            SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2="<",SAT=(solution1+solution2)/2,solution=solution1))
            UNSATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2=">",SAT="UNSAT",solution=None))
    
    if(formula1[0]=="linear" and formula2[0][0]=="q"):
        template="{a1}*#+({b1}){sym1}{c1} & {a2}*#*#+({b2})*#+({c2}){sym2}0,{SAT},{solution}\n"
        solution=formula1[-1]
        if(formula2[0]=="quad0"):
            UNSATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2="<",SAT="UNSAT",solution=None))
            SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2=">",SAT=solution-1,solution=solution))
        if(formula2[0]=="quad1"):
            solution1=formula2[-2]
            solution2=formula2[-1]
            if(solution<solution1):
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2=">",SAT=solution2+1,solution=solution))
                UNSATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2="<",SAT="UNSAT",solution=None))
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2="<",SAT=(solution1+solution2)/2,solution=solution1))
            elif(solution>solution2):
                UNSATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2="<",SAT="UNSAT",solution=None))
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2=">",SAT=solution+1,solution=solution))
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2="<",SAT=(solution1+solution2)/2,solution=solution1))
            else:
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1=">",sym2="<",SAT=(solution+solution2)/2,solution=solution))
                SATFormulas.append(template.format(a1=formula1[1],b1=formula1[2],c1=formula1[3],a2=formula2[1],b2=formula2[2],c2=formula2[3],sym1="<",sym2=">",SAT=solution1-1,solution=solution1))
    if(formula1[0][0]=="q" and formula2[0]=="linear"):
        SATFormulas,UNSATFormulas=generateFormula(formula2,formula1)
    return SATFormulas,UNSATFormulas

def main():
    linearFormulas=[]
    for i in range(20):
        a=abs(round(random.uniform(-1,1),2))
        if(a==0):
            continue
        b=round(random.uniform(-1,1),2)
        c=round(random.uniform(-1,1),2)
        solution=(c-b)/a
        linearFormulas.append(("linear",a,b,c,solution))
    
    quadFormulas=[]
    for i in range(20):
        a=abs(round(random.uniform(-1,1),2))
        if(a==0):
            continue
        b=round(random.uniform(-1,1),2)
        c=round(random.uniform(-1,1),2)
        formula=solveQuadratic(a,b,c)
        quadFormulas.append(formula)
    for i in range(2):
        form1,form2=random.sample(linearFormulas,2)
        SATResult,UNSATResult=generateFormula(form1,form2)
        for item in SATResult:
            SATResultFile.writelines(item)
        for item in UNSATResult:
            UNSATResultFile.writelines(item)
    for i in range(2):
        form1=random.choice(linearFormulas)
        form2=random.choice(quadFormulas)
        SATResult,UNSATResult=generateFormula(form1,form2)
        for item in SATResult:
            SATResultFile.writelines(item)
        for item in UNSATResult:
            UNSATResultFile.writelines(item)
    SATResultFile.close()
    UNSATResultFile.close()
main()

