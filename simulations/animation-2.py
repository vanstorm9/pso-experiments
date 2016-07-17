from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Arc
from math import pi, sin
 
roboWidth = float(input("width of Robot\n  : "))
driveDistance = float(input("distance from target\n  : "))
#theta = float(input("angle of turning(in terms of pi)\n  : "))
 
fig = plt.figure()
 
ax = plt.axes(xlim = (-10,10), ylim = (-10,10))
 
leftPath = Arc([0,0],0,0,0,0,0,color='green', linewidth= .5,animated = True)
rightPath = Arc([0,0],0,0,0,0,0,color='red', linewidth= .5, animated = True)
 
def animate(i):
    #--------------gets globaly defined variables--------
    global driveDistance
    global roboWidth
 
    #----------sets preliminary variables----------------
    degTheta = i + 1 #<-------prevents division by zero
    miniRadius = (driveDistance / 2)/(sin(degTheta * pi / 180))
    roboCenter =  -1 *( miniRadius)
    leftRadius =  miniRadius - roboWidth / 2
    rightRadius =  miniRadius + roboWidth / 2
 
    #---------sets attributes of arcs---------------
    leftPath.xy = [roboCenter,0]
    leftPath.width = leftRadius * 2
    leftPath.height = leftRadius * 2
    leftPath.angle = degTheta
 
    leftPath.xy = [roboCenter,0]
    leftPath.width = rightRadius * 2
    leftPath.height = rightRadius * 2
    leftPath.angle = degTheta
    
ax.add_patch(leftPath)
ax.add_patch(rightPath)
 
anim = animation.FuncAnimation(fig,animate, frames = 360, interval = 20)
plt.show()
