"""
1.combine 2 formula (or 3?)
2.z function generation
3.randomly altering
"""


import random
from curses.ascii import isalpha

letters=["x","y","a","b","c"]

def fusion(formulas,fusionFunc,oracle):
    num=0
    for formula in formulas:
        formula.setvar(letters[num])
        num=num+1
    if(oracle!="SAT" and oracle != "UNSAT"):
        print("FATAL: WRONG ORACLES")
    if(any(formula.oracle!=oracle for formula in formulas)):
        print("FATAL: Inconsistent fusion oracles")
        return

    for formula in formulas:
        while(formula.body.find("#")!=-1):
            ifChange=bool(random.getrandbits(1))
            print(ifChange)
            if(ifChange):
                formula.body=formula.body.replace("#",fusionFunc[formula.var],1)
            else:
                formula.body=formula.body.replace("#",formula.var,1)
            print(formula.body)
    if(oracle=="SAT"):
        finalFormula= " & ".join(formula.body for formula in formulas)

    else:
        finalFormula= " & ".join(formula.body for formula in formulas) + " & "+ fusionFunc["z"]
    return finalFormula

class formulaTemplate():
    def __init__(self,body,oracle):
        #oracle = SAT or UNSAT
        self.oracle=oracle
        self.body=body
        self.var="#"
    
    def setvar(self,var):
        self.var=var

    def print(self):
        print(self.body)
        
def getRecipe():
    recipeFile=open("/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/formatRecipe/formulas","r")
    formulas=[]
    for line in recipeFile.readlines():
        body,SAT=line.split(",")
        formulas.append(formulaTemplate(body,SAT))
    return formulas



def test():
    formulas=getRecipe()
    formula1,formula2=random.sample(formulas,2)
    # formulaBodies=["3*#+1<3 & #>0","#+3*#>5 & #<3"]
    # Formulas=[]
    # iterNum=0
    # for item in formulaBodies:
    #     formula=formulaTemplate(item,"SAT")
    #     Formulas.append(formula)
    #     iterNum+=1
    fusionFunc={"z":"z=x+y","x":"(z-y)", "y":"(z-x)"}
    print(fusion(Formulas,fusionFunc,"SAT"))
"""
    randomly altering
"""
    