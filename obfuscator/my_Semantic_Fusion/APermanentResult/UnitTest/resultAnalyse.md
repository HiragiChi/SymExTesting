## Intro
1.Using three method to conduct unit test to modelled function. 
different mode represents different types of constraints:
-        mode=1 -> math.atan2(x,y)==integer
-        mode=2 -> math.atan2(x,y)==float
-        mode=3 -> x==math.atan2(a,b)


**fullFuncList**=["sqrt1","exp1","asin1","acos1","atan1","atan22","log1","tan1","sin1","cos1","pow2","abs1","max2","min2","round1","ceil1","floor1","rint1"]  while the number followed by a function name indicate the number of parameters it takes.

P.S. log10 is supported, but not good for sym testing.(detailed info can be found in /jpf-symbc/src/peers/gov/nasa/jpf/symbc/JPF_java_lang_Math.java)

## Unmodelled Functions
for unmodelled function, you simply cannot use it. It seems SPF has implemented a different math library itself (in /src/classes/java/lang/Math). You cannot even run a math function that is not in the spf's math library (like Math.cosh) without a jpf file. 

## Result
There are 3 kinds of result:
1) Find a solution and the solution is correct -- correct solved
2) Find the constraint but cannot solve it -- constraint found
3) Cannot even find constraint (output: No path conditions for FILE).
-- constraint not found 
 The related code can be found in /jpf-symbc/src/main/gov/nasa/jpf/symbc/heap/HeapSymbolicListener.java where it indicates that spf cannot find a constraint

### MODE 1: math.atan2(x,y)==integer
|    function name    | correct solved | constraint found | constraint not found|
| ---------- | --- | --- | --- | --- |
| sqrt |  4 |  0   | 46 |
| exp |  10 |  40   | 0 |
| asin |  2 |  11   | 37 |
| acos |  6 |  10   | 34 |
| atan |  18 |  4   | 28 |
| atan2 |  50 |  0   | 0 |
| log |  49 |  0   | 1 |
| tan |  0 |  50   | 0 |
| sin |  50 |  0   | 0 |
| cos |  39 |  11   | 0 |
| pow |  48 |  1   | 1 |
| abs |  50 |  0   | 0 |
| max |  50 |  0   | 0 |
| min |  50 |  0   | 0 |
| round |  2 |  48   | 0 |
| ceil |  50 |  0   | 0 |
| floor |  50 |  0   | 0 |
| rint |  50 |  0   | 0 |


### MODE2  math.atan2(x,y)==float
|    function name    | correct solved | constraint found | constraint not found|
| ---------- | --- | --- | --- | --- |
| sqrt |  2 |  0   | 48 |
| exp |  12 |  38   | 0 |
| asin |  3 |  22   | 25 |
| acos |  3 |  16   | 31 |
| atan |  12 |  13   | 25 |
| atan2 |  48 |  2   | 0 |
| log |  50 |  0   | 0 |
| tan |  0 |  50   | 0 |
| sin |  6 |  44   | 0 |
| cos |  6 |  44   | 0 |
| pow |  50 |  0   | 0 |
| abs |  50 |  0   | 0 |
| max |  50 |  0   | 0 |
| min |  50 |  0   | 0 |
| round |  2 |  48   | 0 |
| ceil |  50 |  0   | 0 |
| floor |  50 |  0   | 0 |
| rint |  50 |  0   | 0 |

### MODE3 x==math.atan2(a,b)  
|    function name    | correct solved | constraint found | constraint not found|
| ---------- | --- | --- | --- | --- |
| sqrt |  50 |  0   | 0 |
| exp |  50 |  0   | 0 |
| asin |  50 |  0   | 0 |
| acos |  50 |  0   | 0 |
| atan |  50 |  0   | 0 |
| atan2 |  50 |  0   | 0 |
| log |  50 |  0   | 0 |
| tan |  50 |  0   | 0 |
| sin |  50 |  0   | 0 |
| cos |  50 |  0   | 0 |
| pow |  50 |  0   | 0 |
| abs |  50 |  0   | 0 |
| max |  50 |  0   | 0 |
| min |  50 |  0   | 0 |
| round |  50 |  0   | 0 |
| ceil |  50 |  0   | 0 |
| floor |  50 |  0   | 0 |
| rint |  50 |  0   | 0 |



#### Result analyze:for SAT status wrong items, spf will only search for certain values:
like for round, only 
SETest_round.run(-99.5)  --> Return Value: 0.0
SETest_round.run(0.5)  --> Return Value: 0.0
SETest_round.run(65.5)  --> Return Value: 0.0
SETest_round.run(99.5)  --> Return Value: 0.0
are tested.