import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(5, 4.5)

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
patch = plt.Circle((5, -5), 0.75, fc='y')

def init():
    patch.center = (5, 5)
    ax.add_patch(patch)
    return patch,

def animateCircTraj(i):
    # i seems to go all the way from 1 to 360
    # Affects the trajectory of the path
    x, y = patch.center
    x = 5 + 3 * np.sin(np.radians(i))
    y = 5 + 3 * np.cos(np.radians(i))
    patch.center = (x, y)
    return patch,

def animateCos(i):
    x, y = patch.center
    x = i
    y = np.cos(np.radians(i))
    patch.center = (x, y)
    return patch,


anim = animation.FuncAnimation(fig, animateCircTraj, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()
