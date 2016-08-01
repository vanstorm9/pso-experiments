import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from random import randint

import random
import math

keep = False
keepX = 0
keepY = 0

### Variables that we can play with ###
interestPointVisual = False
huntEnemy = True
numOfAgents = 10

enemyTopSpeed = 0.5
topSpeed = 0.3

secondDoor = False
resultVisual = False

#obstacleAvoidance = False
chargeEnemy = True

maxFrame = 2000

agentRadius = 2
####################################

victoryCounter = 0

phaseCount = 0

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(5, 4.5)

# Declaring the enemy and ally agents
ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
enemy = plt.Circle((10, -10), 0.95, fc='r')
agent = plt.Circle((10, -10), 0.95, fc='b')


if interestPointVisual:
    interestColor = 'y'
    interestSize = 0.55
    
else:
    interestColor = 'w'
    interestSize = 0.55
    #interestSize = 0.000001



midpoint = plt.Circle((10, -10), interestSize, fc=interestColor)

eastpoint = plt.Circle((10, -10), interestSize, fc=interestColor)
northpoint = plt.Circle((10, -10), interestSize, fc=interestColor)
westpoint = plt.Circle((10, -10), interestSize, fc=interestColor)


northeastpoint = plt.Circle((10, -10), interestSize, fc=interestColor)
mideastpoint = plt.Circle((10, -10), interestSize, fc=interestColor)
midwestpoint = plt.Circle((10, -10), interestSize, fc=interestColor)
northwestpoint = plt.Circle((10, -10), interestSize, fc=interestColor)

# Adding the exits
rect_size = 5
x_se_s = 47

x_se = 50
y_se = 0
 
southExit = plt.Rectangle([x_se_s - rect_size / 2, y_se - rect_size / 2], rect_size + 3, rect_size -2 , facecolor='black', edgecolor='black')

x_ne = 50
y_ne = 101

if secondDoor:
    northExit = plt.Rectangle([x_ne - rect_size / 2, y_ne - rect_size / 2], rect_size + 3, rect_size -2 , facecolor='black', edgecolor='black')


patches_ac = []

if interestPointVisual:
    ax.add_patch(midpoint)
    ax.add_patch(northpoint)
    ax.add_patch(eastpoint)
    ax.add_patch(westpoint)

    ax.add_patch(mideastpoint)
    ax.add_patch(midwestpoint)
    ax.add_patch(northeastpoint)
    ax.add_patch(northwestpoint)


# enemy, north, east, south, west
# 0 represents unoccupied, 1 represent occupied
global occupied_ar
global victory
global agentID
global timeStep

global agentLocationAR



ax.add_patch(agent)

for x in range(0, numOfAgents - 1):
    agent_clone = plt.Circle((10, -10), 0.95, fc='b')
    agent_clone.center = (random.randint(1, 100), random.randint(1, 100))
    patches_ac.append(agent_clone)
    ax.add_patch(agent_clone)

ax.add_patch(enemy)

# Adding exit patches
ax.add_patch(southExit)

if secondDoor:
    ax.add_patch(northExit)


def victoryCheck(enemy_patch):
    global agentLocationAR
    ex, ey = enemy_patch.center

    rangeVal = 0.8
    
    for i in range(0, numOfAgents-1):
        if abs(float(ex-agentLocationAR[i][0])) < rangeVal and  abs(float(ey-agentLocationAR[i][1])) < rangeVal:
            return True

    return False

def enemyWonCheck(enemy_patch):
    x,y = enemy_patch.center

    if (x > x_se - 4 and x < x_se + 4) and y <= y_se +4:
        return True
    return False

def borderCheck(x,y):

    if x < 0:
        x = 0

    elif x > 100:
        x = 100


    if y < 0:
        y = 0

    elif y > 100:
        y = 100


    return x, y
    

def init():
    global occupied_ar
    global agentLocationAR
    global keep
    global keepX
    global keepY

    keep = False
    keepX = 0
    keepY = 0
    
    #enemy.center = (50, 50)
    enemy.center = (random.randint(1, 100), random.randint(40, 100))
    agent.center = (random.randint(1, 100), random.randint(1, 100))

    occupied_ar = np.zeros([9])
    agentLocationAR = np.zeros((numOfAgents,2))
    

    for ac in patches_ac:
        ac.center = (random.randint(1, 100), random.randint(1, 100))

    



    return []

def animationManage(i):
    global occupied_ar
    global agentLocationAR
    global victory
    global agentID
    global timeStep
    global phaseCount
    global maxFrame
    global victoryCounter
    
    timeStep = i
    
    
    agentID = 1
    followTarget(i, agent, enemy)
    
    agentLocationAR[agentID-1][0], agentLocationAR[agentID-1][1] = agent.center
    
    for ac in patches_ac:
        agentID = agentID + 1
        followTarget(i, ac, enemy)

        agentLocationAR[agentID-1][0], agentLocationAR[agentID-1][1] = ac.center

    

        
    goToExit(i, enemy, southExit)
    # printing tests

    
    if victoryCheck(enemy):
        print 'Phase ', phaseCount
        phaseCount += 1
        victoryCounter += 1
        print 'Victory! ', victoryCounter, '/100'
        init()
    elif enemyWonCheck(enemy):
        print 'Phase ', phaseCount
        print 'Failure!'
        init()
    elif i >= maxFrame - 1:
        print 'Phase ', phaseCount
        phaseCount += 1
    
    
        
    return []


def goToExit(i, patch, exit_patch):
    global agentLocationAR
    global keep
    global keepX
    global keepY
    x, y = patch.center
    v_x, v_y = velocity_calc_exit(patch, exit_patch)

    mid_x, mid_y, rad_x, rad_y = getMidDistance(patch, exit_patch)
    rad_size = math.sqrt(rad_x**2 + rad_y**2)


    v_ax, v_ay = attractionFieldExit(patch, x_se, y_se)

    v_rx, v_ry = repulsiveFieldEnemy(patch, 5)
    
    v_x = v_ax + v_rx
    v_y = v_ay + v_ry
    '''
    if abs(v_rx) > 1:
        v_x = v_x/abs(v_x/10)
    if abs(v_ry) > 1:
        v_y = v_x/abs(v_x/10)
    '''
    # Nomalize the magnitude
    v_x = v_x*enemyTopSpeed*0.03
    v_y = v_y*enemyTopSpeed*0.03
    '''
    if abs(v_x) > 1 or abs(v_y) > 1:
        print '-------------'
        print 'Att X: ', v_ax
        print 'Att Y: ', v_ay
        print 'Rep X: ', v_rx
        print 'Rep Y: ', v_ry
        print 'Total X: ', v_x
        print 'Total Y: ', v_y
    '''
  
        
    # x position
    x += v_x*enemyTopSpeed

    # y position
    y += v_y*enemyTopSpeed

    x,y = borderCheck(x,y)

    patch.center = (x, y)

    
    return patch,

def dispersalCalc(user_patch):
    global agentLocationAR # we need location of agents
    for i in range(0,numOfAgents-1):
        if(checkSemiRadius(user_patch, agentRadius)):
            return True

    return False


def attractionFieldExit(user_patch, attr_x, attr_y):
    x,y = user_patch.center

    netX = (x - attr_x)
    netY = (y - attr_y)

    # To prevent slow down when enemy is close to exit
    if x - attr_x > 20 or y - attr_y > 20:
        if x - attr_x > 20:
            netX = (x - attr_x)
        else:
            if x - attr_x == 0:
                netX = 0
            else:
                netX = 5*((x - attr_x)/abs((x - attr_x)))


        
        if y - attr_y > 30:
            netY = (y - attr_y)
        else:
            if y -attr_y == 0:
                netY = 0
            else:
                netY = 50*((y - attr_y)/abs((y - attr_y)))
                #print 'something y ', netY
    

    return -netX, -netY

def repulsiveFieldEnemy(user_patch, repulseRadius):
    # repulsive field that will be used by the enemy agent
    global agentLocationAR
    x,y = user_patch.center
    totalRepX = 0
    totalRepY = 0

    scaleConstant = 1**38
    for i in range(0, numOfAgents-1):
        repX = 0
        repY = 0
        
        avoidX = agentLocationAR[i][0]
        avoidY = agentLocationAR[i][1]

        # To check if one of the agents to avoid are in range
        #print getDistanceScalar(x, y, avoidX, avoidY)
        if getDistanceScalar(x, y, avoidX, avoidY) <= repulseRadius:
            #print 'Enemy agent detected'
            netX = int(x - avoidX)
            netY = int(y - avoidY)

            # To deal with division by zero and normaize magnitude of repX and repY
            if netX == 0:
                netX = 0.2*((x - avoidX)/abs(x - avoidX))
            if netY == 0:
                netY = 0.2*((x - avoidX)/abs(x - avoidX))

            repX = ((1/abs(netX)) - (1/repulseRadius))*(netX/(abs(netX)**3))
            repY = ((1/abs(netY)) - (1/repulseRadius))*(netY/(abs(netY)**3))

        
        totalRepX = totalRepX + repX
        totalRepY = totalRepY + repY
            
    totalRepX = totalRepX/scaleConstant
    totalRepY = totalRepY/scaleConstant


    return -totalRepX, -totalRepY

def followTarget(i, patch, enemy_patch):
    x, y = patch.center

    # Will try to follow enemy
    #v_x, v_y = velocity_calc(patch, enemy_patch)

    # Will follow midpoint of enemy & exit
    v_x, v_y = velocity_calc_mid(patch, enemy_patch)  

    #print 'Here:'
    #print interest_ar
    
    
    # x position
    x += v_x

    # y position
    y += v_y

    patch.center = (x, y)
    return patches_ac


def getInterestPoints(enemy_patch, exit_patch):
    # Calculate interest points to attract agents

    x, y = enemy_patch.center
    
    # Calculate enemy-to-exit midpoint
    mid_x, mid_y, rad_x, rad_y = getMidDistance(enemy_patch, exit_patch)

    interest_ar = np.array([[x,y],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]])

    #north
    interest_ar[1][0] = x - rad_x
    interest_ar[1][1] = y - rad_y


    #east
    interest_ar[3][0] = x - rad_y
    interest_ar[3][1] = y + rad_x


    #south (basically the midpoint)
    interest_ar[5][0] = x + rad_x
    interest_ar[5][1] = y + rad_y


    #west
    interest_ar[7][0] = x + rad_y
    interest_ar[7][1] = y - rad_x

   


    # northeast
    interest_ar[2][0] = (interest_ar[1][0] + interest_ar[3][0])/2
    interest_ar[2][1] = (interest_ar[1][1] + interest_ar[3][1])/2

    #southeast
    interest_ar[4][0] = (interest_ar[3][0] + interest_ar[5][0])/2
    interest_ar[4][1] = (interest_ar[3][1] + interest_ar[5][1])/2

    #southwest
    interest_ar[6][0] = (interest_ar[5][0] + interest_ar[7][0])/2
    interest_ar[6][1] = (interest_ar[5][1] + interest_ar[7][1])/2

    interest_ar[8][0] = (interest_ar[7][0] + interest_ar[1][0])/2
    interest_ar[8][1] = (interest_ar[7][1] + interest_ar[1][1])/2

    
    # Setting up visuals
    northpoint.center = (interest_ar[1][0], interest_ar[1][1])
    eastpoint.center = (interest_ar[3][0], interest_ar[3][1])
    midpoint.center = (interest_ar[5][0], interest_ar[5][1])
    westpoint.center = (interest_ar[7][0], interest_ar[7][1])

    mideastpoint.center = (interest_ar[2][0], interest_ar[2][1])
    midwestpoint.center = (interest_ar[4][0], interest_ar[4][1])
    northeastpoint.center = (interest_ar[6][0], interest_ar[6][1])
    northwestpoint.center = (interest_ar[8][0], interest_ar[8][1])


    return interest_ar


def findClosestInterest(agent_patch, in_ar):
    # For some reason, north never gets occupied
    
    # north east is (north/2) + (south/2)
    global occupied_ar
    global victory
    global agentID
    global timeStep
    global huntEnemy
    

    victory = False

    index = -1
    smallDis = 999999
  

    tempAr = np.zeros([9])
    
    if huntEnemy:
        minDis = 0
    else:
        minDis = 1

    # To check agent's distance of all interest points
    for i in range(minDis,9):
        dis = abs(int(getDistance(agent_patch, in_ar, i)))

    
       # Add heavy weights to charge at enemy
        if chargeEnemy:
            if i == 0:
                dis = dis*0.5

        

        if occupied_ar[i] != 0:
            # we must write a condition so that agent knows it is the
            # one that is occupying it
            dis = dis*5

        # Add heavy weights to avoid the back
        if i == 1 or i == 8 or i == 2:

            if i == 1:
                dis = dis*3
            elif i == 2 or i == 8:
                dis = dis*4
            

        tempAr[i] = dis

  

        
        # When we discover unoccupied shorter distance, replace index        
        if dis < smallDis:
            
            # index is agent_patch.center[0] < 47 and agent_patch.center[0] > 53the index of interest_array of the closest interest point 
            smallDis = dis
            index = i
    
    # If the smallest distance is less than 10, we are currently engaged


    if smallDis < 0.5:
        # We are near or at the targeted interest point,
        # now we should update array as occupied

  
        occupied_ar[index] = agentID

        if occupied_ar[0] != 0:
            victory = True
        
        #print 'engaged index ', index
    else:
        # Else we are still far away from the index
        if occupied_ar[index] == agentID:
            occupied_ar[index] = 0
            
            
            #print 'lost track of index ', index
        #else:
            #print 'far away from index ', index
            
        
    return index

def getBypassInterestPoints(user_patch,avoidX, avoidY, exit_x, exit_y):
    # Mainly used by the enemy agent
    # User agent will find a point around the blocking agent that is closest to
    # the exit.
    x,y = user_patch.center
    rad_range = 20

    tempX = x - avoidX
    tempY = y - avoidY

    diffR = math.sqrt(tempX**2 + tempY**2)

    # Calculating our target x and y length
    radX = (rad_range*tempX)/diffR
    radY = (rad_range*tempY)/diffR

    # Now we calculate the main interest points

    # Since we are calculating perpendicular points, we reverse the X and Y
    # in the pt calculation process
    pt1X = avoidX + radY
    pt1Y = avoidY - radX
    
    ###
    pt2X = avoidX - radY
    pt2Y = avoidY + radX

    # Then we must determine which interest point is closer to the exit

    pt1Dis = int(getDistanceScalar(pt1X, pt1Y,exit_x, exit_y))
    pt2Dis = int(getDistanceScalar(pt2X, pt2Y,exit_x, exit_y))

    # If point 1 is closer to the exit than point 2
    if(int(pt1Dis) <= int(pt2Dis)):
        print int(pt1X)
        return pt1X, pt1Y
    
    print int(pt2X)
    return int(pt2X), int(pt2Y)
    

def getDistanceScalar(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def getDistance(agent_patch, in_ar, index):
    x_a, y_a = agent_patch.center
    x_t = in_ar[index][0]
    y_t = in_ar[index][1]


    # get distance between two particles
    ans = math.sqrt((x_t - x_a)**2 + (y_t - y_a)**2)
    if math.isnan(ans):
        print 'x_a: ',x_a
        print 'y_a: ',y_a
        print 'x_t: ',x_t
        print 'y_t: ',y_t
        init()
    return math.sqrt((x_t - x_a)**2 + (y_t - y_a)**2)
    

def getMidDistance(enemy_patch, exit_patch):
    # Get midpoint between enemy agent and exit
    
    x, y = enemy_patch.center
    x_e = x_se
    y_e = y_se

    # Get midpoint values
    mid_x = (x + x_e)/2
    mid_y = (y + y_e)/2

    # Get radius values
    rad_x = mid_x - x
    rad_y = mid_y - y

    # Returns (midpoint x and y) values and (radius x and y) values
    return mid_x, mid_y, rad_x, rad_y

def top_speed_regulate(curr_speed, top_speed):

    if curr_speed > top_speed:
        return top_speed
    elif curr_speed < -top_speed:
        return -top_speed
    else:
        return curr_speed

def velocityCalcScalar(x1, y1, x2, y2):
    
    veloX = top_speed_regulate( (x2 - x1)      ,enemyTopSpeed)
    veloY = top_speed_regulate( (y2 - y1)      ,enemyTopSpeed)
    
    return veloX, veloY


# Calculate velocity to rush to exit
def velocity_calc_exit(agent_patch, exit_patch):

    x, y = agent_patch.center
    #x_e, y_e = exit_patch.center
    x_e = x_se
    y_e = y_se

    velo_vect = np.array([0.0, 0.0], dtype='f')

    dis_limit_thresh = 1 

    

    velo_vect[0] = top_speed_regulate( (x_e - x)* dis_limit_thresh    ,enemyTopSpeed)
    velo_vect[1] = top_speed_regulate( (y_e - y)* dis_limit_thresh    ,enemyTopSpeed)

    return velo_vect[0], velo_vect[1]


# Calculate velocity to chase down enemy
def velocity_calc(agent_patch, enemy_patch):

    x, y = agent_patch.center
    x_e, y_e = enemy_patch.center

    velo_vect = np.array([0.0, 0.0], dtype='f')

    dis_limit_thresh = 1 

    

    velo_vect[0] = top_speed_regulate( (x_e - x)* dis_limit_thresh    ,topSpeed)
    velo_vect[1] = top_speed_regulate( (y_e - y)* dis_limit_thresh    ,topSpeed)

    return velo_vect[0], velo_vect[1]

# Calculate velocity to arrive at midpoint between enemy and exit
def velocity_calc_mid(agent_patch, enemy_patch):
   
    
    x, y = agent_patch.center
    x_e, y_e, _, _ = getMidDistance(enemy_patch, southExit)

    # We get location of interest points as well as animate the interest points
    interest_ar = getInterestPoints(enemy_patch, southExit)

    interest_index = findClosestInterest(agent_patch, interest_ar)
  

    
    
    x_e = interest_ar[interest_index][0]
    y_e = interest_ar[interest_index][1]

    
    

    velo_vect = np.array([0.0, 0.0], dtype='f')

    dis_limit_thresh = 1 

    topSpeed = 0.3

    velo_vect[0] = top_speed_regulate( (x_e - x)* dis_limit_thresh    , topSpeed)
    velo_vect[1] = top_speed_regulate( (y_e - y)* dis_limit_thresh    , topSpeed)

    '''
    if dispersalCalc(agent_patch):
        velo_vect[0] = 0
        velo_vect[1] = 0
    '''
    return velo_vect[0], velo_vect[1]


def checkRadius(user_patch, r):
    global agentLocationAR
    r = 1
    for i in range(0,numOfAgents-1):
        x = int(agentLocationAR[i][0])
        y = int(agentLocationAR[i][1])

        if(inRadius(user_patch, x, y, r)):
            # if an agent is in the user's radius
            #print 'Nearby agent detected'
            return True
            

    return False

def checkSemiRadius(user_patch, r):
    global agentLocationAR
    r = 0.001
    for i in range(0,numOfAgents-1):
        x = int(agentLocationAR[i][0])
        y = int(agentLocationAR[i][1])

        if(inSemiRadius(user_patch, x, y, r)):
            # if an agent is in the user's radius
            #print 'Nearby agent detected'
            return True
            

    return False


def inRadius(self_patch, pointX, pointY, r):
    # Helps determine if there is something near the using agent
    
    x, y = self_patch.center # agent emitting the radius
    # agent we are trying to avoid

    h = pointX
    k = pointY    
    # Equation of circle
    # (x-h)^2 + (y-k)^2 <= r^2

    tempX = (x - h)**2
    tempY = (y - k)**2

    r_2 = r**2

    if tempX + tempY <= r_2:
        # It is within the radius
        return True
    else:
        return False


def inSemiRadius(self_patch, pointX, pointY, r):
    # Helps determine if there is something near the using agent
    
    h, k = self_patch.center # agent emitting the radius
    # agent we are trying to avoid
    x = pointX
    y = pointY
    # Equation of semicircle

    tempTerm = r**2 - (x-h)**2

    if tempTerm < 0:
        # if this term is negative, that means agent to avoid is out of range
        return False

    tempEq = k - math.sqrt(tempTerm)
    

    if y <= tempEq:
        # It is within the radius
        return True
    else:
        return False



def animateCos(i, patch):
    x, y = patch.center
    x += 0.1

    y = 50 + 30 * np.cos(np.radians(i))
    patch.center = (x, y)
    return patch,


anim = animation.FuncAnimation(fig, animationManage,
                               init_func=init,
                               frames=maxFrame,
                               interval=1,
                               blit=True,
                               repeat=True)


plt.show()
