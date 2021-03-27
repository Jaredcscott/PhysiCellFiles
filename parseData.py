import sys
from Parser import Parser

#'Data' is a directory within the working directory, holding the output data.
parser = Parser("Data") 


frameCount = parser.getFrameCount() #Pulling frame count
'''
    cells is a Cells object
    Use .data to retrieve an array of the data. 
    Each entry in the data array is an array holding a single data value for all cells in the simulation. 

    Use .variables to show the data values contained for each cell. 
    The index values associated with that data is given within the variables set.  
'''
cells = parser.getFrame(1).cells 
print(cells.variables)

for frameNumber in range(170,171):
    cells = parser.getFrame(frameNumber).cells
    for cellPhase in cells.data[7]: #7 is the index value for cell phase, 14 is alive and healthy
        if cellPhase == 14:
            pass
            #Cell is alive, Calulate the volume.         
    
    
