IFInstrSymbHelper - "***********Warning: everything false" 
with input : log ('0.11*x+-0.01<0.15 & 0.34*x+-0.13>-0.48', '0.21256684491978617')

log10 not implemented in sym mode
tan cannot solve while cannot detect path condition in atan

statisticallize No path conditions for ...

## for SAT status wrong items, spf will only search for certain values:
like for round, only 
SETest_round.run(-99.5)  --> Return Value: 0.0
SETest_round.run(0.5)  --> Return Value: 0.0
SETest_round.run(65.5)  --> Return Value: 0.0
SETest_round.run(99.5)  --> Return Value: 0.0
are tested.