# Lab Meat/Cell Culture Growth Simulation Optimization 


The folder Config_Files cultured_meat should be placed within the /PhysiCell/sample-projects folder. 
The block of text within /Config_Files/makeAddition.txt should be added to /Physicell/sample-projects/Makefile-default

fitness.py should be placed (together with the class Parser.py) within the main /PhysiCell/ directory. 

Create a file called coords.csv (or use a sample one within the PhysiCellFiles/sample-coords/ folder). 

Example File Structure For Running The Sim

    .
    |
    PhysiCell
       -.
        |PhysiCell
        |System 
        |Files
        |
        |output     <--- Output location for PhysiCell simulation files
        |Parser.py  <--- Must be in the same directory as the simulation output folder 
        |fitness.py <--- Must be together with Parser.py
        |coords.csv <--- Create or replace with a new file
        |sample-projects
           -.
            |cultured_meat    <--- Copy folder 
            |Makefile-default <--- Add makeAddition.text content
      
    
