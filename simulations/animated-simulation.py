import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(5, 4.5)

ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
enemy = plt.Circle((10, -10), 0.75, fc='r')
agent = plt.Circle((10, -10), 0.75, fc='b')

food_test = plt.Circle((10, -10), 0.75, fc='y')

def init():
    enemy.center = (5, 5)
    agent.center = (5, 5)
    
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
    animateLine(i,agent)
    #goToFood(i,agent,enemy)
    
    return []

def goToFood(i, patch, enemy_patch):
    # v(t+1) = wv(t) + rand_1()c_1(p(t)  - x(t)) + rand_2()c_2(g(t) - x(t))
    # x(t+1) = x(t) + v(t + 1)
    
    x, y = patch.center
    x_e, y_e = enemy_patch.center
    
    print y

    # To update the position

    #x += 0.25
    #x += x_e - x
    y += y_e - y
    
    #x += x_e - x
    #y += y_e - y
    
    patch.center = (x, y)
    return patch,


def velocity_calc(pos_vect):

    velo_vect = np.array([0.0,0.0], dtype='f')

    velo_vect[0] = 0.25
    velo_vect[1] = 0.25
    
    return velo_vect[0], velo_vect[1]
    


def animateLine(i, patch):
    x, y = patch.center
    pos_vect = np.array([x,y], dtype='f')

    vel_vect = np.array([1,1])
    

    v_x, v_y = velocity_calc(pos_vect)

    # x position
    x += v_x

    # y position
    y += v_y

    patch.center = (x, y)
    return patch,

'''
def animateLine(i, patch):
    x, y = patch.center

    x += 0.25
    y += 0.25
    patch.center = (x, y)
    return patch,
'''

def animateCos(i, patch):
    x, y = patch.center
    x += 0.1
    y = 50 + 10 * np.cos(np.radians(i))
    y = 50 
    patch.center = (x, y)
    return patch,






anim = animation.FuncAnimation(fig, animationManage,
                               init_func=init,
                               frames=360,
                               fargs=(agent,enemy,),
                               interval=1,
                               blit=True,
                               repeat=True)


plt.show()
