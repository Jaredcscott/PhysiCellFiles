'''
    To use this, place the file within the main PhysiCell directory 
    (ie PhysiCell/fitness.py)
'''
import xml.etree.ElementTree as ET
import pandas as pd
import os
import turtle

from Parser import Parser

import math
CUR_SIM = 0
volumes=[]

class UndrawnTurtle():
    def __init__(self):
        self.x, self.y, self.angle = 0.0, 0.0, 0.0
        self.pointsVisited = []
        self._visit()

    def position(self):
        return self.x, self.y

    def goto(self,x,y):
        self.x = x 
        self.y = y
        self._visit()

    def xcor(self):
        return self.x

    def ycor(self):
        return self.y

    def forward(self, distance):
        angle_radians = math.radians(self.angle)

        self.x += math.cos(angle_radians) * distance
        self.y += math.sin(angle_radians) * distance

        self._visit()

    def backward(self, distance):
        self.forward(-distance)

    def right(self, angle):
        self.angle -= angle

    def left(self, angle):
        self.angle += angle

    def setpos(self, x, y = None):
        """Can be passed either a tuple or two numbers."""
        if y == None:
            self.x = x[0]
            self.y = y[1]
        else:
            self.x = x
            self.y = y
        self._visit()

    def _visit(self):
        """Add point to the list of points gone to by the turtle."""
        self.pointsVisited.append(self.position())
        
    def setheading(self,angle):
      """Add point to the list of points gone to by the turtle."""
      self.angle = angle

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
 
MINIMUM_BRANCH_LENGTH = 5

def build_tree(file, t, branch_length, shorten_by, angle):
  if branch_length > MINIMUM_BRANCH_LENGTH:
    t.forward(branch_length/4)
    file.write(str(int(t.xcor())*1.5)+','+str(int(t.ycor())* 1.5) + ',0,3\n')
    t.forward(branch_length/2)
    file.write(str(int(t.xcor())*1.5)+','+str(int(t.ycor())* 1.5) + ',0,3\n')
    t.forward(branch_length/4)
    new_length = branch_length - shorten_by    
    t.left(angle)
    build_tree(file, t, new_length, shorten_by, angle)  
    t.right(angle * 2)
    build_tree(file, t, new_length, shorten_by, angle)    
    t.left(angle)
    file.write(str(int(t.xcor())*1.5)+','+str(int(t.ycor())* 1.5) + ',0,3\n')
    #build_tree(file, t, new_length, shorten_by, angle) # Adds a third branch 
    t.backward(branch_length)

def gen_tree(branchLen,armLen,angle):
    file = open("./coords.csv",'w')
    file.truncate(0)
    tree = UndrawnTurtle()
    tree.setheading(90)
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    build_tree(file, tree, branchLen,armLen,angle)
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    tree.goto(0,0)
    tree.setheading(180)
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    build_tree(file, tree, branchLen,armLen,angle)
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    tree.goto(0,0)
    tree.setheading(270)
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    build_tree(file, tree, branchLen,armLen,angle)
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    tree.goto(0,0)
    tree.setheading(0)
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    build_tree(file, tree, branchLen,armLen,angle)
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    file.write(str(int(tree.xcor())*1.5)+','+str(int(tree.ycor())* 1.5) + ',0,3\n')
    file.close()

def gen_tree_visible(branchLen,armLen,angle):

  tree = turtle.Turtle()
  file = open("./coords.csv",'w')
  file.truncate(0)
  tree.hideturtle()
  tree.speed(0)
  tree.setheading(90)
  tree.color('green')
  build_tree(file,tree, branchLen, armLen,angle)
  tree.penup()
  tree.goto(0,0)
  tree.setheading(180)
  tree.pendown()
  build_tree(file,tree, branchLen, armLen,angle)
  tree.penup()
  tree.goto(0,0)
  tree.setheading(270)
  tree.pendown()
  build_tree(file,tree, branchLen, armLen,angle)
  tree.penup()
  tree.goto(0,0)
  tree.setheading(0)
  tree.pendown()
  build_tree(file,tree, branchLen, armLen,angle)
  '''
  #Ucomment to add second branch structure. 
  tree.penup()
  tree.goto(0,0)
  tree.setheading(90)
  tree.pendown()
  build_tree(file,tree, 60, 10,15)
  tree.penup()
  tree.goto(0,0)
  tree.setheading(180)
  tree.pendown()
  build_tree(file,tree, 60, 10,15)
  tree.penup()
  tree.goto(0,0)
  tree.setheading(270)
  tree.pendown()
  build_tree(file,tree, 60, 10,15)
  tree.penup()
  tree.goto(0,0)
  tree.setheading(0)
  tree.pendown()
  build_tree(file,tree, 60, 10,15)
  '''
  turtle.mainloop()
