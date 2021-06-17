"""
参照：https://github.com/bonarl/Clohessy-Wiltshire

@author: bonar

@author: shio 2021


!apt-get update && apt-get install imagemagick
"""

import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from IPython.display import HTML

# r0 = [5, 0.0, 0]                                #initial position vector
# rdot0 = [0.1, 0.3, -0.023]                      #initial velocity
# omeg = 0.0010854                                #mean motion of principal body, (can be calculated from altitude of circular orbit)

gc = 398600.5           # Gravitational constant [km^3/s^2]
r_earth = 6378.14       # erath radius [km]
alt = 590               # altitude [km]

omeg = math.sqrt(gc/(r_earth+alt)**3)

r0 = [25, 100, 0]
rdot0 = [0, -1.5*r0[0]*omeg, 0]



def CW(r0, rdot0, omeg, t):
    x0 = r0[0]
    y0 = r0[1]
    z0 = r0[2]
    xdot0 = rdot0[0]
    ydot0 = rdot0[1]
    zdot0 = rdot0[2]
    
    xt = (4*x0 + (2*ydot0)/omeg)+(xdot0/omeg)*math.sin(omeg*t)-(3*x0+(2*ydot0)/omeg)*math.cos(omeg*t)
    yt = (y0 - (2*xdot0)/omeg)+((2*xdot0)/omeg)*math.cos(omeg*t)+(6*x0 + (4*ydot0)/omeg)*math.sin(omeg*t)-(6*omeg*x0+3*ydot0)*t
    zt = z0*math.cos(omeg*t)+(zdot0/omeg)*math.sin(omeg*t)
    return([xt, yt, zt])
    
xs = []
ys = []
zs = []
time = []

nframes = 100
dt = 120
for j in range(nframes):
    xs.append(CW(r0, rdot0, omeg, j*dt)[0])
    ys.append(CW(r0, rdot0, omeg, j*dt)[1])
    zs.append(CW(r0, rdot0, omeg, j*dt)[2])
    time.append(j*dt/60)
xmin = min(xs)
xmax = max(xs)
ymin = min(ys)
ymax = max(ys)
zmin = min(zs)
zmax = max(zs)

fig = plt.figure()

# ax0 = fig.add_subplot(111)
# ax0.plot(ys, xs)
# plt.show


ax = fig.add_subplot(111, projection='3d',xlim = (xmin, xmax), ylim = (ymin, ymax),zlim = (zmin, zmax))
ax.set_xlabel('x')
ax.invert_xaxis()
ax.set_ylabel('y')
ax.set_zlabel('z') 


def init():
    return(ax)

def animate(j):
    x = CW(r0, rdot0, omeg, j*dt)[0]
    y = CW(r0, rdot0, omeg, j*dt)[1]
    z = CW(r0, rdot0, omeg, j*dt)[2]
    ax.scatter(x, y, z, marker='.',c='r', alpha = 0.5)
    time_str = "%s [min]" %(time[j])
    # ax.text(0.5, 1.01, time_str, horizontalalignment="center", verticalalignment="bottom", transform=ax.transAxes, size=10)
    ax.text(25.0, 100.0, 0.04, time_str, bbox=dict(facecolor='white', alpha=1.0), fontsize=10)
    return(ax)
    
anim= animation.FuncAnimation(fig, animate, init_func=init, frames = nframes, interval = 50)
anim.save('/content/cw0.gif', dpi=80, writer='imagemagick')
plt.close()
HTML(anim.to_jshtml())
