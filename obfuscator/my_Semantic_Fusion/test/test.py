import random,math
a=range(1,10)
x="Math.atan((Z-Y))==(0) & Math.abs((Z-X))==(15)"
formulas=x.split("&")
template="abs({left}-{right})"
testFormulas=[]
for formula in formulas:
    bothSide=formula.split("==")
    testFormula=template.format(left=bothSide[0],right=bothSide[1])
    testFormulas.append(testFormula)
testFinal="+".join(testFormulas)
testFinal=testFinal+"< 0.01"
print(testFinal)