# Spiral Pattern Coordinate Generator 
# For Cultured Meat Simulation 
![Tools](doubleBranch.png "")


The folder contains:<br>
    1) genTree.py This file contians a function gen_tree() which will produce tree like branching patterns of cells.<br> 
    2) Examples of coordinate files produced by this generator<br>
    3) Images of the generated patterns <br>

To use this generator:<br>
    1) Place it in the main PhysiCell directory (IE the desired location of your coordinates file)<br>
    2) Adjust the parameters within genTree.py to produce the desired tree structure<br>

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
        |genTree.py <--- 
        |coords.csv   

If a file called coords.csv already exists, it will be overwritten, if not, it will be created. 
