import turtle

MINIMUM_BRANCH_LENGTH = 5

def build_tree(t, branch_length, shorten_by, angle):
  if branch_length > MINIMUM_BRANCH_LENGTH:
    print(int(t.xcor())*1.5, ',',int(t.ycor())* 1.5,',0,3')
    t.forward(branch_length/2)
    print(int(t.xcor())*1.5, ',',int(t.ycor())* 1.5,',0,3')
    t.forward(branch_length/2)
    print(int(t.xcor())*1.5, ',',int(t.ycor())* 1.5,',0,3')
    new_length = branch_length - shorten_by    
    t.left(angle)
    build_tree(t, new_length, shorten_by, angle)    
    t.right(angle * 2)
    build_tree(t, new_length, shorten_by, angle)    
    t.left(angle)
    t.backward(branch_length)

tree = turtle.Turtle()
    
tree.hideturtle()
tree.setheading(90)
tree.color('green')
build_tree(tree, 50, 10, 30)
tree.penup()
tree.goto(0,0)
tree.setheading(180)
tree.pendown()
build_tree(tree, 50, 10, 30)
tree.penup()
tree.goto(0,0)
tree.setheading(270)
tree.pendown()
build_tree(tree, 50, 10, 30)
tree.penup()
tree.goto(0,0)
tree.setheading(0)
tree.pendown()
build_tree(tree, 50, 10, 30)
turtle.mainloop()