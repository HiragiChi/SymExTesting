"""
1.combine 2 formula (or 3?)
2.z function generation
3.randomly altering
"""


import random
from curses.ascii import isalpha

letters=["X","Y","A","B","C"]
fusionFunc2={"Z":"Z=X+Y","X":"(Z-Y)", "Y":"(Z-X)"}

def fusion(formulas,fusionFunc,oracle):
    """
    formulas - list of formula, formula should have 1 variable #
    orables - "SAT" or "UNSAT" 
    """
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
            # print(ifChange)
            if(ifChange):
                formula.body=formula.body.replace("#",fusionFunc[formula.var],1)
            else:
                formula.body=formula.body.replace("#",formula.var,1)
            # print(formula.body)
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
        print(self.body+","+self.oracle)
        
def getRecipe():
    SATRecipeFile=open("/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/formatRecipe/SAT","r")
    UNSATRecipeFile=open("/home/hiragi/Desktop/jpf/obfuscator/my_Semantic_Fusion/formatRecipe/UNSAT","r")
    SATFormulas=[]
    UNSATFormulas=[]
    for line in SATRecipeFile.readlines():
        body,SAT=line.split(",")
        SATFormulas.append(formulaTemplate(body,"SAT"))
    for line in UNSATRecipeFile.readlines():
        body,UNSAT=line.split(",")
        UNSATFormulas.append(formulaTemplate(body,"UNSAT"))
    return SATFormulas,UNSATFormulas



def test():
    a="Math.log(#)==3"
    b="Math.ceil(#)==5"
    # SATFormulas,UNSATFormulas=getRecipe()
    # SATRecipes=random.sample(SATFormulas,2)
    # UNSATRecipes=random.sample(UNSATFormulas,2)
    formulaA=formulaTemplate(a,"SAT")
    formulaB=formulaTemplate(b,"SAT")
    fusionFunc={"Z":"Z=X+Y","X":"(Z-Y)", "Y":"(Z-X)"}
    formulaList=[formulaA,formulaB]
    print(fusion(formulaList,fusionFunc,"SAT"))



"""
    randomly altering
"""