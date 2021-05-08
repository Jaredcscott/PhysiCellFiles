# Use the pattern generators here to create biologically similar cell structures. 

# Example File Structure 
Place a  <generator file>.py file within the main PhysiCell directory (OR where you wuld like your coords.csv file)
    
    .
    | 
    PhysiCell
       -.
        |PhysiCell
        |System 
        |Files
        |
        |<Generator file> <--- Place generator fiile here and ensure fitness.py references the desired generator function
        |output           <--- Output location for PhysiCell simulation files
        |Parser.py        <--- Must be in the same directory as the simulation output folder 
        |fitness.py       <--- Must be together with Parser.py
        |coords.csv       <--- Create or replace with a new file
        |sample-projects

If `coords.csv` does not exists it will be created. 
