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
patches_ac = []
ax.add_patch(agent)

for x in range(0, 5):
    agent_clone = plt.Circle((10, -10), 0.75, fc='b')
    agent_clone.center = (random.randint(1, 100), random.randint(1, 100))
    patches_ac.append(agent_clone)
    ax.add_patch(agent_clone)

ax.add_patch(enemy)


def init():
    enemy.center = (5, 5)

    agent.center = (random.randint(1, 100), random.randint(1, 100))
    for ac in patches_ac:
        ac.center = (random.randint(1, 100), random.randint(1, 100))
    return []


def animationManage(i):
    animateCos(i, enemy)
    followTarget(i, agent, enemy)
    for ac in patches_ac:
        followTarget(i, ac, enemy)

    return []

def followTarget(i, patch, enemy_patch):
    x, y = patch.center
    v_x, v_y = velocity_calc(patch, enemy_patch)

    # x position
    x += v_x

    # y position
    y += v_y

    patch.center = (x, y)
    return patches_ac


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

    velo_vect = np.array([0.0, 0.0], dtype='f')

    velo_vect[0] = top_speed_regulate( (x_e - x)* 0.05 )
    velo_vect[1] = top_speed_regulate( (y_e - y)* 0.05 )

    return velo_vect[0], velo_vect[1]


def animateCos(i, patch):
    x, y = patch.center
    x += 0.1

    y = 50 + 30 * np.cos(np.radians(i))
    patch.center = (x, y)
    return patch,


anim = animation.FuncAnimation(fig, animationManage,
                               init_func=init,
                               frames=1000,
                               interval=1,
                               blit=True,
                               repeat=True)


plt.show()
