import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.special import ellipk

# time step
dt = 0.001

m = 0.1 # bob pass (kg)
L = 0.1 # pendulum length (m)
g = 9.8 # gravitational constant (m/s^2)

# initial angular displacement (rad), initial tangential velocity (m/s)
theta0, v0 = np.radians(60), 0

# estimate period using harmonic (small displacement) approximation
tharm = 2 * np.pi * np.sqrt(L / g)

# theta and v list
theta, v = [theta0], [v0]
theta_old = theta0

i = 0

while True:
    # forward euler method for ode
    i += 1
    t = i * dt

    # update bob position using updated angle
    theta_old, v_old = theta[-1], v[-1]
    omega = v_old / L
    theta_new = theta_old - omega * dt

    # tangential acceleration
    accel = g * np.sin(theta_old)
    v_new = v_old + accel * dt # update tangential velocity

    # at the second turning point in velocity (back where we're started)
    # completed 1 period, finish the sim
    if (t > tharm and v_new * v_old < 0):
        break

    theta.append(theta_new)
    v.append(v_new)

# calculate estimated pendulum period (T) from numerical integration
n = len(theta)
T = n * dt
k = np.sin(theta0 / 2)

print(f"Calculated period (T): {T}")
print(f"Estimated harmonic displacement (Tharm): {tharm}")
print(f"Scipy calculated period (T): {2 * tharm / np.pi * ellipk(k**2)}")

# get (x, y) coordinates of the bob at angular displacement th
def get_coords(th):
    return L * np.sin(th), -L * np.cos(th)

# animation
fig = plt.figure()
ax = fig.add_subplot(aspect='equal')
ax.set_title('Pendulum')

# pendulum rod in initial position
x0, y0 = get_coords(theta0)
line, = ax.plot([0, x0], [0, y0], lw=3, c='k')

# pendulum bob
radius = 0.005
bob = ax.add_patch(plt.Circle(get_coords(theta0), radius, fc='b', zorder=3))

# plot limits
ax.set_xlim(-L * 1.2, L * 1.2)
ax.set_ylim(-L * 1.2, L * 1.2)

def animate(frame):
    x, y = get_coords(theta[frame])
    line.set_data([0, x], [0, y])
    bob.set_center((x, y))

nframes = n
interval = dt * 1000
anim = animation.FuncAnimation(fig, animate, frames=nframes, repeat=True, interval=interval)

plt.show()
