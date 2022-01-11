'''
    This is a fitness algorithm to determine how wella specific configuration of feeder cells grows the cell culture
    To use this, place the file within the main PhysiCell directory 
    (ie PhysiCell/fitness.py)
'''
import xml.etree.ElementTree as ET
import pandas as pd
import os
import turtle

from Parser import Parser
from genTree import gen_tree
from genSpiral import gen_spiral

import math
CUR_SIM = 0
volumes=[]

class Cell:
  def __init__(self, data, variables):
    self.data = data
    self.variables = variables 
  def getData(self):
    return self.data
  def getVariables(self):
    return self.variables
  def __str__(self):
    return "Cell Id: " + str(self.data[0]) + " Data index values: " + str(self.variables) 


def fitness(inputVals):
    global CUR_SIM
    '''
        This function takes as input an array where each element is an array contianing 
        input parameters for a PhysiCell .xml config file. 
        The input will then be fed, one by one, into PhysiCell for simulation. 
        Each set of simulation data will then be 
    '''
    os.system("make data-cleanup")
    gen_tree(inputVals[0],inputVals[1],inputVals[2])
    configFilePath = "./config/PhysiCell_settings.xml"   #Path to the xml config file within PhysiCell
    runSim()
    parser = Parser("./output/")                         #Parsing data into a Parser object
    frameCount = parser.getFrameCount()                  #Pulling frame count from data
    masterTable = {}                                     #Master array to store cell objects
    for frameNumber in range(*parser.getFrameRange()):   #Looping through frames
        curArray = [] 
        cells = parser.getFrame(frameNumber).cells       #Pulling cells from parser
        index = 0
        for i in range(len(cells.data[0])):              #Looping through Cell's
          curCellData = []                  
          for dataArray in cells.data:                   #Looping through master Data array aggregating the individual cell's data. 
            curCellData.append(dataArray[i])           
          newCell = Cell(curCellData, cells.variables)   #Creating Cell Object
          masterTable[newCell.getData()[0]] =  newCell

    VolumeFromInput = 0                                  #Summing healthy biomass within simulation output
    for cell in masterTable:
        curData = masterTable[cell].getData()            #Pulling individual cells data
        if curData[7] == 14:                             #Checking if cell is alive and healthy phase 14
            VolumeFromInput += curData[4]                #If cell is alive and healthy, add its volume to the current total 
    comString = "cp -r ./output ./sim" + str(CUR_SIM)
    os.system(comString) 
    print("TOTAL HEALTHY BIOMASS: ",VolumeFromInput)
    volumes.append(VolumeFromInput)
    CUR_SIM += 1
    return VolumeFromInput


def runSim():
    print("-------------Running Simulation-------------")
    os.system("./cultured_meat") 
    print("-------------Simulation Finished-------------")
 
