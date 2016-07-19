import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import random

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(5, 4.5)

# Declaring the enemy and ally agents
ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
enemy = plt.Circle((10, -10), 0.95, fc='r')
agent = plt.Circle((10, -10), 0.95, fc='b')

midpoint = plt.Circle((10, -10), 0.95, fc='y')
eastpoint = plt.Circle((10, -10), 0.95, fc='y')
northpoint = plt.Circle((10, -10), 0.95, fc='y')
westpoint = plt.Circle((10, -10), 0.95, fc='y')

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
ax.add_patch(agent)

numOfAgents = 7

for x in range(0, numOfAgents - 1):
    agent_clone = plt.Circle((10, -10), 0.95, fc='b')
    agent_clone.center = (random.randint(1, 100), random.randint(1, 100))
    patches_ac.append(agent_clone)
    ax.add_patch(agent_clone)

ax.add_patch(enemy)


ax.add_patch(midpoint)
ax.add_patch(northpoint)
ax.add_patch(eastpoint)
ax.add_patch(westpoint)





ax.add_patch(southExit)
ax.add_patch(northExit)


def init():
    enemy.center = (random.randint(1, 100), random.randint(1, 100))

    agent.center = (random.randint(1, 100), random.randint(1, 100))


    for ac in patches_ac:
        ac.center = (random.randint(1, 100), random.randint(1, 100))





     # Initalizing visual of interest points
    in_ar = getInterestPoints(enemy, southExit)
    
    
    


    return []

def animationManage(i):
    #animateCos(i, enemy)
    goToExit(i, enemy, southExit)
    
    followTarget(i, agent, enemy)
    
    for ac in patches_ac:
        followTarget(i, ac, enemy)

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


def getMidDistance(enemy_patch, exit_patch):
    # Get midpoint between enemy agent and exit
    
    x, y = enemy_patch.center
    x_e = x_se
    y_e = y_se

    #print 'x: ', x
    #print 'y: ', y

    # Get midpoint values
    mid_x = (x + x_e)/2
    mid_y = (y + y_e)/2

    #print 'mid_x: ',mid_x
    #print 'mid_y: ',mid_y

    # Get radius values
    rad_x = mid_x - x
    rad_y = mid_y - y

    #print 'rad_x: ',rad_x
    #print 'rad_y: ',rad_y
    
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

    topSpeed = 0.4

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

    ########
    interest_ar = getInterestPoints(enemy_patch, southExit)
    
    x_e = interest_ar[2][0]
    y_e = interest_ar[2][1]

    #print 'res_x: ', x_e
    #print 'res_y: ', y_e

    #print x_e , ' ' , y_e 
    #print interest_ar[4]
    ########

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
