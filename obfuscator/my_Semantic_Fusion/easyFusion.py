"""
1.combine 2 formula (or 3?)
2.z function generation
3.randomly altering
"""

"""
only replace x , y or z
"""
import random
from curses.ascii import isalpha

letters=["x","y","a","b","c"]

def fusion(formulas,fusionFunc,oracle):
    if(oracle!="SAT" and oracle != "UNSAT"):
        print("FATAL: WRONG ORACLES")
    if(any(formula.oracle!=oracle for formula in formulas)):
        print("FATAL: Inconsistent fusion oracles")
        return
    # for num in range(len(originString)):
    #     if(isalpha(originString[num])):
    #         ifChange=bool(random.getrandbits(1))
    #         if(ifChange):
    #             replacedString
    for formula in formulas:
        while(formula.body.find("a")!=-1):
            ifChange=bool(random.getrandbits(1))
            print(ifChange)
            if(ifChange):
                formula.body=formula.body.replace("a",fusionFunc[formula.var],1)
            else:
                formula.body=formula.body.replace("a",formula.var,1)
            print(formula.body)
    if(oracle=="SAT"):
        finalFormula= " & ".join(formula.body for formula in formulas)

    else:
        finalFormula= " & ".join(formula.body for formula in formulas) + " & "+ fusionFunc["z"]
    return finalFormula

class Formula():
    def __init__(self,body,oracle):
        self.oracle=oracle
        self.body=body
        self.var="0"
    
    def setvar(self,var):
        self.var=var

def test():
    formulaBodies=["3*a+1<3 & a>0","a+3*a>5 & a<3"]
    Formulas=[]
    iterNum=0
    for item in formulaBodies:
        formula=Formula(item,"SAT")
        formula.setvar(letters[iterNum])
        Formulas.append(formula)
        iterNum+=1
    fusionFunc={"z":"z=x+y","x":"(z-y)", "y":"(z-x)"}
    print(fusion(Formulas,fusionFunc,"SAT"))
"""
    randomly altering
"""
test()
    