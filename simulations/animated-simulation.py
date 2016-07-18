import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import random

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(5, 4.5)

ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
enemy = plt.Circle((10, -10), 0.75, fc='r')
agent = plt.Circle((10, -10), 0.75, fc='b')

food_test = plt.Circle((10, -10), 0.75, fc='y')

def init():
    enemy.center = (5, 5)
    agent.center = (random.randint(1, 100), random.randint(1, 100))
    
    food_test.center = (10,10)


    ax.add_patch(agent)
    ax.add_patch(enemy)
    
    ax.add_patch(food_test)

    return []

def initalizePosition(agent,enemy):
    x_a, y_a = agent.center
    x_e, y_e = enemy.center

    x_a += 50
    y_a += 50

    agent.center = (x_a, y_a)
    enemy.center = (x_e, y_e)
    return agent    


def animationManage(i,agent,enemy):
    animateCos(i,enemy)
    #animateCirc(i,enemy)

    #animateLine(i,agent)
    followTarget(i,agent,enemy)
    
    return []

def followTarget(i, patch, enemy_patch):
    x, y = patch.center

    
    # Calculating velocity
    # v(t+1) = wv(t) + rand_1()c_1(p(t)  - x(t)) + rand_2()c_2(g(t) - x(t))
    v_x, v_y = velocity_calc(patch, enemy_patch)

    # Implementing:
    # x(t+1) = x(t) + v(t + 1)
   
    # x position
    x += v_x

    # y position
    y += v_y

    patch.center = (x, y)
    return patch,


def inertia_calc():
    return 0



def top_speed_regulate(curr_speed):
    top_speed = 0.5
    
    if curr_speed > top_speed:
        return top_speed
    elif curr_speed < -top_speed:
        return -top_speed
    else:
        return curr_speed

def velocity_calc(agent_patch, enemy_patch):
    
    x, y = agent_patch.center
    x_e, y_e = enemy_patch.center

    
    pos_vect = np.array([x,y], dtype='f')



    

    velo_vect = np.array([0.0,0.0], dtype='f')
    '''
    velo_vect[0] = top_speed_regulate( (x_e - x)* 0.05 )* random.random() 
    velo_vect[1] = top_speed_regulate( (y_e - y)* 0.05 )* random.random()
    '''
    
    velo_vect[0] = top_speed_regulate( (x_e - x)* 0.05 )
    velo_vect[1] = top_speed_regulate( (y_e - y)* 0.05 )

        
    
    return velo_vect[0], velo_vect[1]
    

def animateLine(i, patch):
    x, y = patch.center

    x += 0.25
    y += 0.25
    patch.center = (x, y)
    return patch,


def animateCos(i, patch):
    x, y = patch.center

    x += 0.1
    #x += 0.4

    y = 50 + 30 * np.cos(np.radians(i))
    #y = 50 + 10 * np.cos(np.radians(i))
    patch.center = (x, y)
    return patch,


def animateCirc(i, patch):
    # It seems that i represents time step
    x, y = patch.center
    # 1st constant = position and 2nd constant = trajectory
    x = 50 + 30 * np.sin(np.radians(i))
    y = 50 + 30 * np.cos(np.radians(i))
    patch.center = (x, y)
    return patch,




anim = animation.FuncAnimation(fig, animationManage,
                               init_func=init,
                               frames=1000,
                               fargs=(agent,enemy,),
                               interval=1,
                               blit=True,
                               repeat=True)


plt.show()
