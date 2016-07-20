import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from random import randint

import random
import math

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(5, 4.5)

# Declaring the enemy and ally agents
ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
enemy = plt.Circle((10, -10), 0.95, fc='r')
agent = plt.Circle((10, -10), 0.95, fc='b')

midpoint = plt.Circle((10, -10), 0.55, fc='y')
eastpoint = plt.Circle((10, -10), 0.55, fc='y')
northpoint = plt.Circle((10, -10), 0.55, fc='y')
westpoint = plt.Circle((10, -10), 0.55, fc='y')

# Adding the exits
rect_size = 5
x_se_s = 47

x_se = 50
y_se = 0
 
southExit = plt.Rectangle([x_se_s - rect_size / 2, y_se - rect_size / 2], rect_size + 3, rect_size -2 , facecolor='black', edgecolor='black')

x_ne = 50
y_ne = 101
northExit = plt.Rectangle([x_ne - rect_size / 2, y_ne - rect_size / 2], rect_size + 3, rect_size -2 , facecolor='black', edgecolor='black')


patches_ac = []


ax.add_patch(midpoint)
ax.add_patch(northpoint)
ax.add_patch(eastpoint)
ax.add_patch(westpoint)

# enemy, north, east, south, west
# 0 represents unoccupied, 1 represent occupied
global occupied_ar
occupied_ar = np.array([0,0,0,0,0])




ax.add_patch(agent)

numOfAgents = 7


for x in range(0, numOfAgents - 1):
    agent_clone = plt.Circle((10, -10), 0.95, fc='b')
    agent_clone.center = (random.randint(1, 100), random.randint(1, 100))
    patches_ac.append(agent_clone)
    ax.add_patch(agent_clone)

ax.add_patch(enemy)

# Adding exit patches
ax.add_patch(southExit)
ax.add_patch(northExit)





def init():
    global occupied_ar
    
    enemy.center = (random.randint(1, 100), random.randint(1, 100))
    agent.center = (random.randint(1, 100), random.randint(1, 100))

    occupied_ar = np.zeros([5])
 
    

    for ac in patches_ac:
        ac.center = (random.randint(1, 100), random.randint(1, 100))

     # Initalizing visual of interest points
    in_ar = getInterestPoints(enemy, southExit)
    
    
    


    return []

def animationManage(i):
    global occupied_ar
    
    #goToExit(i, enemy, southExit)

    followTarget(i, agent, enemy)

    for ac in patches_ac:
        followTarget(i, ac, enemy)


    # printing tests

    if i >= 199:
        print occupied_ar

    return []


def goToExit(i, patch, exit_patch):
    x, y = patch.center
    v_x, v_y = velocity_calc_exit(patch, exit_patch)

    
    # x position
    x += v_x

    # y position
    y += v_y

    
    patch.center = (x, y)

    
    return patch,

def followTarget(i, patch, enemy_patch):
    x, y = patch.center

    # Will try to follow enemy
    #v_x, v_y = velocity_calc(patch, enemy_patch)

    # Will follow midpoint of enemy & exit
    #interest_ar = getInterestPoints(patch, enemy_patch)
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

    interest_ar = np.array([[mid_x,mid_y],[0,0],[0,0],[0,0],[0,0]])

    #north
    interest_ar[1][0] = x - rad_x
    interest_ar[1][1] = y - rad_y

    #print 'mid_x: ', mid_x
    #print 'mid_y: ', mid_y


    #east
    interest_ar[2][0] = x - rad_y
    interest_ar[2][1] = y + rad_x


    #print interest_ar[2][0]
    #print interest_ar[2][1]
    

    #south (basically the midpoint)
    interest_ar[3][0] = x + rad_x
    interest_ar[3][1] = y + rad_y

    
    #west
    interest_ar[4][0] = x + rad_y
    interest_ar[4][1] = y - rad_x




    northpoint.center = (interest_ar[1][0], interest_ar[1][1])
    eastpoint.center = (interest_ar[2][0], interest_ar[2][1])
    midpoint.center = (interest_ar[3][0], interest_ar[3][1])
    westpoint.center = (interest_ar[4][0], interest_ar[4][1])

    return interest_ar


def findClosestInterest(agent_patch, in_ar):
    global occupied_ar

    index = -1
    smallDis = 999999

    # To check agent's distance of all interest points
    for i in range(0,4):
        dis = abs(int(getDistance(agent_patch, in_ar, i)))

        if occupied_ar[i] == 1:
            dis = dis*200
  
        # When we discover unoccupied shorter distance, replace index        
        if dis < smallDis:
            # index is the index of interest_array of the closest interest point 
            smallDis = dis
            index = i
    
    # At this point, we found a smallest distance, let's update the occupation array
    # We want to know if interest point is occupied by someone else
    # If the smallest distance is less than 10, we are currently engaged
    if smallDis < 2:
        # We are near or at the targeted interest point,
        # now we should update array as occupied
        
        occupied_ar[index] = 1
        
        #print 'engaged index ', index
    else:
        # Else we are still far away from the index
        if occupied_ar[index] == 1:
            occupied_ar[index] = 0
            
            #print 'lost track of index ', index
        #else:
            #print 'far away from index ', index
            
        
    return index

def getDistance(agent_patch, in_ar, index):
    x_a, y_a = agent_patch.center
    x_t = in_ar[index][0]
    y_t = in_ar[index][1]

    # get distance between two particles
    return math.sqrt(abs((x_t - x_a) + (y_t - y_a)))
    

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

# Calculate velocity to rush to exit
def velocity_calc_exit(agent_patch, exit_patch):

    x, y = agent_patch.center
    #x_e, y_e = exit_patch.center
    x_e = x_se
    y_e = y_se

    velo_vect = np.array([0.0, 0.0], dtype='f')

    dis_limit_thresh = 1 

    topSpeed = 0.3

    velo_vect[0] = top_speed_regulate( (x_e - x)* dis_limit_thresh    ,topSpeed)
    velo_vect[1] = top_speed_regulate( (y_e - y)* dis_limit_thresh    ,topSpeed)

    return velo_vect[0], velo_vect[1]


# Calculate velocity to chase down enemy
def velocity_calc(agent_patch, enemy_patch):

    x, y = agent_patch.center
    x_e, y_e = enemy_patch.center

    velo_vect = np.array([0.0, 0.0], dtype='f')

    dis_limit_thresh = 1 

    topSpeed = 0.3

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

    return velo_vect[0], velo_vect[1]


def animateCos(i, patch):
    x, y = patch.center
    x += 0.1

    y = 50 + 30 * np.cos(np.radians(i))
    patch.center = (x, y)
    return patch,


anim = animation.FuncAnimation(fig, animationManage,
                               init_func=init,
                               frames=200,
                               interval=1,
                               blit=True,
                               repeat=True)


plt.show()
