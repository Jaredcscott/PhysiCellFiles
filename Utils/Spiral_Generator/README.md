# Spiral Pattern Coordinate Generator 
# For Lab Meat Simulation 
![Tools](/doubleSpiral.png "")


The folder contains:
    1) genSpiral.py This file contians a function gen_spiral() which will produce spiral patterns of cells. 
    
    2) Examples of coordinate files produced by this generator

    3) Images of the generated patterns. 

To use this generator:
    1) Place it in the main PhysiCell directory (IE the desired location of your coordinates file)

    2) Adjust the parameters within genSpiral.py to produce the desired spiral. 

Example file structure for running generator 

    .
    |
    PhysiCell
       -.
        |PhysiCell
        |System 
        |Files
        |
        |output       
        |genSpiral.py <--- 
        |coords.csv   

If a file called coords.csv already exists, it will be overwritten, if not, it will be created. 