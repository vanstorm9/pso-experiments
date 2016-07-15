import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(5, 4.5)

ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
patch = plt.Circle((10, -10), 0.75, fc='r')

def init():
    patch.center = (5, 5)
    ax.add_patch(patch)
    return patch,

def animateCirc(i):
    # It seems that i represents time step
    x, y = patch.center
    # 1st constant = position and 2nd constant = trajectory
    x = 50 + 30 * np.sin(np.radians(i))
    y = 50 + 30 * np.cos(np.radians(i))
    patch.center = (x, y)
    return patch,

def animateLine(i):
    x, y = patch.center
    x = x + 1
    y = x+ 1
    patch.center = (x, y)
    return patch,


def animateCos(i):
    x, y = patch.center
    x = x + 0.2
    y = 50 + 30 * np.cos(np.radians(i))
    patch.center = (x, y)
    return patch,

def animateSin(i):
    x, y = patch.center
    x = x + 0.2
    y = 50 + 30 * np.sin(np.radians(i))
    patch.center = (x, y)
    return patch,


anim = animation.FuncAnimation(fig, animateCos, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()
