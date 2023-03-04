
******Readme for FebRNA package******  by Tan-group at Wuhan University

FebRNA is a package for building RNA 3D structures with input their secondary structures 
based on coarse-grained fragment ensembles [1]. The program of FebRNA is run in Python,
and numpy and scipy modules are required.


Please run FebRNA as follows:

```
# Compilation and usage under linux
gcc cgRNASP-Feb.c -lm -o cgRNASP-Feb
gcc reconstruction.c -lm -o reconstruction 

# Run in the example dir 
python ./FebRNA.py (or python3 ./FebRNA.py)
(in the file directory depending on the installed Python version) .
```

## According to corresponding instructions from FebRNA, please input :
- (a) sequence information, 
- (b) secondary structure in  dot-bracket form, 
- (c) number of structures required (n), and
- (d) whether all-atom construction is required accordingly.
 
## Wait for a while (usually within several minutes) to obtain the results.
- (a) The results are placed in the './RESULT'; 
- (b) './RESULT/CG_Result' contains all the predicted coarse-grained conformations;
- (c) './RESULT/Select_Result' contains a selection of TOP-n coarse-grained conformations;
- (d) './RESULT/AA_Result' contains the rebuilt all-atom structures of selected coarse-grained structures.

An example is:
```
python FebRNA.py 
Sequence:GCGGCACCGUCCGCUCAAACAAACGG
Secondary Structure:((((..[[[.)))).........]]]
Seleted Num(0=all):5
All-atom rebuilding?(y/n):y
Finish in folder ./RESULT
Running time :37.020s
```

## Further refinement is required for the rebuilt all-atom structures.
To remove possible steric clashes and chain breaks of the rebuilt all-atom structures,  a structure 
refinement  can be performed for the rebuilt all-atom structures by FebRNA through the method 
of QRNAS (https://github.com/sunandan-mukherjee/QRNAS.git) [2].


If you have any questions about FebRNA, please contact us by the email: zjtan@whu.edu.cn .

References:                                      
[1] Zhou L, Wang X, Yu S, Tan YL, &  Tan ZJ. 2022. FebRNA: an automated fragment-ensemble-based 
model for building RNA 3D structures. Biophys J. 121(18): 3381-3392.                                                    
[2] Stasiewicz J, Mukherjee S, Nithin C, & Bujnicki, JM. 2019. QRNAS: software tool for refinement of 
nucleic acid structures. Bmc Struct Biology. 19, 5.


