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

# Adding the exits
rect_size = 5
x_se = 50
y_se = 0
 
southExit = plt.Rectangle([x_se - rect_size / 2, y_se - rect_size / 2], rect_size + 3, rect_size -2 , facecolor='black', edgecolor='black')

x_ne = 50
y_ne = 101
northExit = plt.Rectangle([x_ne - rect_size / 2, y_ne - rect_size / 2], rect_size + 3, rect_size -2 , facecolor='black', edgecolor='black')


patches_ac = []
ax.add_patch(agent)

numOfAgents = 10

for x in range(0, numOfAgents):
    agent_clone = plt.Circle((10, -10), 0.95, fc='b')
    agent_clone.center = (random.randint(1, 100), random.randint(1, 100))
    patches_ac.append(agent_clone)
    ax.add_patch(agent_clone)

ax.add_patch(enemy)

ax.add_patch(southExit)
ax.add_patch(northExit)


def init():
    enemy.center = (random.randint(1, 100), random.randint(1, 100))

    agent.center = (random.randint(1, 100), random.randint(1, 100))
    for ac in patches_ac:
        ac.center = (random.randint(1, 100), random.randint(1, 100))
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
    v_x, v_y = velocity_calc_mid(patch, enemy_patch)  

    # x position
    x += v_x

    # y position
    y += v_y

    patch.center = (x, y)
    return patches_ac


def getMidDistance(enemy_patch, exit_patch):
    x, y = enemy_patch.center

    x_e = x_se
    y_e = y_se

    mid_x = (x + x_e)/2
    mid_y = (y + y_e)/2

    return mid_x, mid_y

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

    topSpeed = 0.6

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
    x_e, y_e = getMidDistance(enemy_patch, southExit)


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
