
******Readme for cgRNAfrag******  by Tan-group at Wuhan University

cgRNAfrag is a tool for separating a global RNA 3D structure at the 3-bead CG representation into its different types of fragments based on its secondary structure.

Please run cgRNAfrag as follows:

```
# The prerequisite files and path to place them
- (a) two files with suffix of “.pdb” and ".dbn" for the 3D coarse-grained coordinates in standard PDB format and secondary structure in dot-bracket form for a RNA respectively (e.g. 4jf2.pdb and 4jf2.dbn)
- (b) create a new folder named by the corresponding PDB id under the “pdb” folder (e.g. "pdb/4jf2")
- (c) place the above two files to the new folder

# Run cgRNAfrag program
- python ./cgRNAfrag.py (or python3 ./cgRNAfrag.py)
  (It depends on the installed Python version) .

# The output files
- The separated fragments will be finally in the "database" folder in different types
```

If you have any questions about cgRNAfrag, please contact us by the email: zjtan@whu.edu.cn .

Reference:                                      
[1] Zhou L, Wang X, Yu S, Tan YL, &  Tan ZJ. 2022. FebRNA: an automated fragment-ensemble-based 
model for building RNA 3D structures.


