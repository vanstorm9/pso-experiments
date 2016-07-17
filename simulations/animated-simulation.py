import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(5, 4.5)

ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
enemy = plt.Circle((10, -10), 0.75, fc='r')
agent = plt.Circle((10, -10), 0.75, fc='b')


def init():
    enemy.center = (5, 5)
    agent.center = (5, 5)
    ax.add_patch(agent)
    ax.add_patch(enemy)

    return []


def animationManage(i,agent,enemy):
    animateCos(i,enemy)
    animateLine(i,agent)
    return []


def animateLine(i, patch):
    x, y = patch.center
    x += 0.25
    y += 0.25
    patch.center = (x, y)
    return patch,


def animateCos(i, patch):
    x, y = patch.center
    x += 0.1
    y = 50 + 30 * np.cos(np.radians(i))
    patch.center = (x, y)
    return patch,

anim = animation.FuncAnimation(fig, animationManage,
                               init_func=init,
                               frames=360,
                               fargs=(agent,enemy,),
                               interval=20,
                               blit=True,
                               repeat=True)


plt.show()
