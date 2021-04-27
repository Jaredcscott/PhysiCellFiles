import turtle 
import matplotlib.pyplot as plt
import math

MINIMUM_BRANCH_LENGTH = 5
xs = []                          # Stores the x values for a graphic representation
ys = []                          # Stores the y values for a graphic representation
exampleArgs = {'sixToOne':[60,10,60],'phiAndPi':[16,3.14,60]}
branchLen = 60
armLen = 10
angle = 60

def build_tree(file, t, branch_length, shorten_by, angle):
  global xs 
  global ys
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
    x = int(t.xcor()*1.5)
    y = int(t.ycor()* 1.5)
    xs.append(x)
    ys.append(y)
    file.write(str(x)+','+str(y)+',0,3\n')
    #build_tree(file, t, new_length, shorten_by, angle) # Adds a third branch 
    t.backward(branch_length)

def gen_tree(branchLen,armLen,angle):
    file = open("./coords.csv",'w')
    file.truncate(0)
    tree = UndrawnTurtle()
    tree.setheading(90)
    build_tree(file, tree, branchLen,armLen,angle)
    tree.goto(0,0)
    tree.setheading(180)
    build_tree(file, tree, branchLen,armLen,angle)
    tree.goto(0,0)
    tree.setheading(270)
    build_tree(file, tree, branchLen,armLen,angle)
    tree.goto(0,0)
    tree.setheading(0)
    build_tree(file, tree, branchLen,armLen,angle)
    #Uncomment to add second branch structure. 
    '''
    tree.goto(0,0)
    tree.setheading(90)
    build_tree(file,tree, 60, 10,15)
    tree.goto(0,0)
    tree.setheading(180)
    build_tree(file,tree, 60, 10,15)
    tree.goto(0,0)
    tree.setheading(270)
    build_tree(file,tree, 60, 10,15)
    tree.goto(0,0)
    tree.setheading(0)
    build_tree(file,tree, 60, 10,15)
    '''
    file.close()
    plt.scatter(xs,ys)
    plt.title("Pattern Generated")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

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
      
gen_tree(branchLen,armLen,angle)