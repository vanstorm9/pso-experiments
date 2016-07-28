from pylab import *
from scipy.integrate import odeint
from matplotlib import animation
from matplotlib import cm
import numpy as np

#rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
#rc('text', usetex=True)

## Set up charges

class charge:
    def __init__(self, q, pos):
        self.q=q
        self.pos=pos


chargesPlus=[]
chargesMinus=[]

#for i in arange(0,1,1):
chargesPlus.append(charge(1,[3,0]))
chargesMinus.append(charge(-1,[-3,0]))
charges = chargesPlus + chargesMinus


def E_point_charge(q, a, x, y,r):
    return q*(x-a[0])/((x-a[0])**2+(y-a[1])**2)**(1.5), \
        q*(y-a[1])/((x-a[0])**2+(y-a[1])**2)**(1.5)


def E_total(x, y, charges):
    Ex, Ey=0, 0
    for C in charges:
        E=E_point_charge(C.q, C.pos, x, y,1)
        Ex=Ex+E[0]
        Ey=Ey+E[1]
    return [Ex, Ey]


domain =2

## Cut Quiver plot
def cut(r):
    if r < domain:
        return 0
    else:
        return 1

cutv = np.vectorize(cut)


def cut_total(charges,x): 
    c = 1
    for C in charges: 
        r = sqrt((C.pos[0] - x[0])**2 + (C.pos[1] - x[1])**2)
        c = c*cutv(r)
        print c
        print C.pos[0],C.pos[1]
    return c

fig = figure()

ax = fig.add_subplot(1,1,1)


xMin,xMax=-15,15
yMin,yMax=-10,10

#ax.plot(x,y)
ax.axis('tight')
xlim([xMin,xMax])
ylim([yMin,yMax])


# plot point charges
for C in charges:
    if C.q>0:
        plot(C.pos[0], C.pos[1], 'bo', ms=8*sqrt(C.q))
    if C.q<0:
        plot(C.pos[0], C.pos[1], 'ro', ms=8*sqrt(-C.q))


xG,yG = meshgrid(linspace(xMin,xMax,25),linspace(yMin,yMax,25))

# plot vector field
E_totalX,E_totalY = E_total(xG,yG,charges)

EAbs = (E_totalX**2 + E_totalY**2)**(0.5)
E_XX = E_totalX/EAbs
E_YY = E_totalY/EAbs
#EAbs = np.nan_to_num(EAbs) 

#ax.streamplot(xG,yG,E_XX,E_YY,color=EAbs,cmap=cm.autumn)
ax.quiver(xG,yG,E_XX,E_YY,EAbs,cmap=cm.GnBu)

xlabel('x')
ylabel('y')
ax.set_aspect(1)


plt.savefig('fig1.png')

E_totalX = E_totalX*cut_total(charges,[xG,yG])
E_totalY = E_totalY*cut_total(charges,[xG,yG])

ax.cla()

# plot point charges
for C in charges:
    if C.q>0:
        plot(C.pos[0], C.pos[1], 'bo', ms=8*sqrt(C.q))
    if C.q<0:
        plot(C.pos[0], C.pos[1], 'ro', ms=8*sqrt(-C.q))


ax.quiver(xG,yG,E_totalX,E_totalY,pivot='middle',minshaft=0.1,minlength=0.3,headlength=2,headaxislength=2,headwidth=3,scale=4,alpha=0.4,width=0.002,linestyle='solid')

xlabel('x')
ylabel('y')
ax.set_aspect(1)

plt.savefig('fig2.png')
show()
