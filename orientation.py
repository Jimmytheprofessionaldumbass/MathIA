import csv
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

with open("Test/Accelerometer.csv") as accelobject, open("Test/Orientation.csv") as orientationobject:
    # Preprocessing ---------------------------------------------------------------------------------
    accel = tuple(tuple(float(item) for item in row) for row in list(csv.reader(accelobject))[2:])
    # Because Accelerometer actually records before orientation sensor does
    # format: time, seconds_elapsed,z,y,x
    #         0     1               2 3 4

    orien = tuple(tuple(float(item) for item in row) for row in list(csv.reader(orientationobject))[1:])
    # format: time,seconds_elapsed,qz,qy,qx,qw,roll,pitch,yaw
    #         0    1               2  3  4  5  6    7     8(-1)
    
    # Check if the time is aligned
    if (orien[0][1] != accel[0][1]):
        print("Initial Time not aligned!")
        print(f"orientation initial time is {orien[0][1]}, but acceleration initial time is {accel[0][1]}")
        quit()
    # Orienting -------------------------------------------------------------------------------------
    oriented_accel = []
    # format: time, north_accel, east_accel
    index = 0
    for row in accel:
        try:
            oriented_accel.append((
                row[1],
                row[3]*math.cos(orien[index][-1]) - row[4]*math.sin(orien[index][-1]),
# Translation:  y     *     cos(     yaw        ) - x     *     sin(      yaw       )
                row[3]*math.sin(orien[index][-1]) + row[4]*math.cos(orien[index][-1])
# Translation:  y     *     sin(     yaw        ) + x     *     cos(      yaw       )
            ))
            index += 1
        except IndexError:
            break

    # Centering averages ----------------------------------------------------------------------------
    # avg_n_displ = sum(datum[1] for datum in oriented_accel)/len(oriented_accel)
    # avg_e_displ = sum(datum[2] for datum in oriented_accel)/len(oriented_accel)
    # oriented_accel = [(row[0], row[1] - avg_n_displ, row[2] - avg_e_displ) for row in oriented_accel]

    # Integrating to velocity -----------------------------------------------------------------------
    vel = [(oriented_accel[0][0], 0, 0)]
    index = 0
    for row in oriented_accel:
        try:
            dt = oriented_accel[index+1][0]-row[0]
            
            dn_accel = oriented_accel[index+1][1] - row[1]
            de_accel = oriented_accel[index+1][2] - row[2]

            dn_vel = (dt*row[1]+(1/2)*(dt*dn_accel))
            de_vel = (dt*row[2]+(1/2)*(dt*de_accel))

            vel.append((row[0], vel[index][1]+dn_vel, vel[index][2]+de_vel))
            
            index += 1
        except IndexError:
            break

    # Centering averages ----------------------------------------------------------------------------
    # avg_n_displ = sum(datum[1] for datum in vel)/len(vel)
    # avg_e_displ = sum(datum[2] for datum in vel)/len(vel)
    # vel = [(row[0], row[1] - avg_n_displ, row[2] - avg_e_displ) for row in vel]

    # Integrating to displacement -------------------------------------------------------------------
    displ = [(vel[0][0], 0, 0)]
    index = 0
    for row in vel:
        try:
            dt = vel[index+1][0]-row[0]
            
            dn_vel = vel[index+1][1] - row[1]
            de_vel = vel[index+1][2] - row[2]

            dn_displ = (dt*row[1]+(1/2)*(dt*dn_vel))
            de_displ = (dt*row[2]+(1/2)*(dt*de_vel))

            displ.append((row[0], displ[index][1]+dn_displ, displ[index][2]+de_displ))
            
            index += 1
        except IndexError:
            break

# Cleaning the filter -------------------------------------------------------------------------------

proc = []
index = 0

for datum in displ:
    proc.append(
        (
            datum[0],
            datum[1] - displ[-1][1] * (index/len(displ)),
            datum[2] - displ[-1][2] * (index/len(displ))
        )
    )
    index += 1

# Plotting ------------------------------------------------------------------------------------------
# Extract data from the Oriented Acceleration stage
time_accel = [row[0] for row in oriented_accel]
north_accel = [row[1] for row in oriented_accel]
east_accel = [row[2] for row in oriented_accel]

# Extract data from the Velocity stage
time_vel = [row[0] for row in vel]
north_vel = [row[1] for row in vel]
east_vel = [row[2] for row in vel]

# Extract data from the Raw Displacement stage
time_displ = [row[0] for row in displ]
north_displ = [row[1] for row in displ]
east_displ = [row[2] for row in displ]

# Extract data from the Cleaned Filter (proc) stage
time_proc = [row[0] for row in proc]
north_proc = [row[1] for row in proc]
east_proc = [row[2] for row in proc]

# --- PLOTTING ---
# Extract data from the Raw Acceleration stage
# (Slicing accel to the exact length of oriented_accel so the time arrays match)
raw_y = [accel[i][3] for i in range(len(oriented_accel))]
raw_x = [accel[i][4] for i in range(len(oriented_accel))]

# Extract data from the Oriented Acceleration stage
time_accel = [row[0] for row in oriented_accel]
north_accel = [row[1] for row in oriented_accel]
east_accel = [row[2] for row in oriented_accel]

# Extract data from the Velocity stage
time_vel = [row[0] for row in vel]
north_vel = [row[1] for row in vel]
east_vel = [row[2] for row in vel]

# Extract data from the Raw Displacement stage
time_displ = [row[0] for row in displ]
north_displ = [row[1] for row in displ]
east_displ = [row[2] for row in displ]

# Extract data from the Cleaned Filter (proc) stage
time_proc = [row[0] for row in proc]
north_proc = [row[1] for row in proc]
east_proc = [row[2] for row in proc]

# --- PLOTTING ---
# # Set up a 4x2 grid (4 rows | 2 columns)
# fig, axes = plt.subplots(4, 2, figsize=(14, 13), sharex=True)
# fig.suptitle('IMU Data Pipeline: Raw Acceleration to Displacement', fontsize=16, fontweight='bold')
#
# # ROW 1: RAW ACCELERATION (Un-oriented)
# axes[0, 0].plot(time_accel, raw_y, color='tab:orange')
# axes[0, 0].set_title('Raw Y Acceleration (Forward/Backward)')
# axes[0, 0].set_ylabel('Accel (m/s²)')
# axes[0, 0].grid(True, linestyle='--', alpha=0.6)
#
# axes[0, 1].plot(time_accel, raw_x, color='tab:green')
# axes[0, 1].set_title('Raw X Acceleration (Left/Right)')
# axes[0, 1].grid(True, linestyle='--', alpha=0.6)
#
# # ROW 2: ORIENTED ACCELERATION
# axes[1, 0].plot(time_accel, north_accel, color='tab:red')
# axes[1, 0].set_title('Oriented North Acceleration')
# axes[1, 0].set_ylabel('Accel (m/s²)')
# axes[1, 0].grid(True, linestyle='--', alpha=0.6)
#
# axes[1, 1].plot(time_accel, east_accel, color='tab:blue')
# axes[1, 1].set_title('Oriented East Acceleration')
# axes[1, 1].grid(True, linestyle='--', alpha=0.6)
#
# # ROW 3: VELOCITY
# axes[2, 0].plot(time_vel, north_vel, color='tab:red')
# axes[2, 0].set_title('North Velocity')
# axes[2, 0].set_ylabel('Velocity (m/s)')
# axes[2, 0].grid(True, linestyle='--', alpha=0.6)
#
# axes[2, 1].plot(time_vel, east_vel, color='tab:blue')
# axes[2, 1].set_title('East Velocity')
# axes[2, 1].grid(True, linestyle='--', alpha=0.6)
#
# # ROW 4: DISPLACEMENT
# # Plot raw displacement faded out in the background
# axes[3, 0].plot(time_displ, north_displ, color='tab:red', alpha=0.3, label='Raw Integration')
# # Overlay the linear drift corrected data
# axes[3, 0].plot(time_proc, north_proc, color='tab:red', label='Drift Corrected')
# axes[3, 0].set_title('North Displacement')
# axes[3, 0].set_ylabel('Displacement (m)')
# axes[3, 0].set_xlabel('Time (s)')
# axes[3, 0].legend()
# axes[3, 0].grid(True, linestyle='--', alpha=0.6)
#
# axes[3, 1].plot(time_displ, east_displ, color='tab:blue', alpha=0.3, label='Raw Integration')
# axes[3, 1].plot(time_proc, east_proc, color='tab:blue', label='Drift Corrected')
# axes[3, 1].set_title('East Displacement')
# axes[3, 1].set_xlabel('Time (s)')
# axes[3, 1].legend()
# axes[3, 1].grid(True, linestyle='--', alpha=0.6)
#
# # Adjust layout to prevent overlapping labels
# plt.tight_layout()
# plt.show()
#


# =========================================================================================
# --- ANIMATION: 2D Trajectory Path ---
# =========================================================================================

# Create a new square figure for the map view
fig_anim, ax_anim = plt.subplots(figsize=(8, 8))
fig_anim.suptitle('Phone Trajectory (Top-Down View)', fontsize=16, fontweight='bold')

ax_anim.set_xlabel('East Displacement (m)')
ax_anim.set_ylabel('North Displacement (m)')
ax_anim.grid(True, linestyle='--', alpha=0.6)

# Force equal aspect ratio so 1 meter North looks exactly as long as 1 meter East
ax_anim.set_aspect('equal')

# Set static axis boundaries based on min/max of your drift-corrected data 
# (+ a 10% buffer so the path doesn't touch the very edge of the window)
x_range = max(east_proc) - min(east_proc)
y_range = max(north_proc) - min(north_proc)
buffer_x = x_range * 0.1 if x_range != 0 else 1
buffer_y = y_range * 0.1 if y_range != 0 else 1

ax_anim.set_xlim(min(east_proc) - buffer_x, max(east_proc) + buffer_x)
ax_anim.set_ylim(min(north_proc) - buffer_y, max(north_proc) + buffer_y)

# Initialize the line for the path, and a red dot for the phone's current location
trajectory_line, = ax_anim.plot([], [], color='tab:blue', linewidth=2, label='Path Taken')
phone_point, = ax_anim.plot([], [], 'ro', markersize=8, label='Phone Position')
ax_anim.legend(loc="upper left")

# Initialization function required by FuncAnimation
def init():
    trajectory_line.set_data([], [])
    phone_point.set_data([], [])
    return trajectory_line, phone_point

# Update function that runs every frame
def update(frame):
    # Draw line from start to current frame
    trajectory_line.set_data(east_proc[:frame], north_proc[:frame])
    # Place the dot exactly at the current frame's X/Y coordinate
    phone_point.set_data([east_proc[frame]], [north_proc[frame]])
    return trajectory_line, phone_point

# Create the looping animation
# frames=len(time_proc) ensures it runs through your entire dataset
# interval=20 sets a 20 millisecond delay between frames (adjust for speed)
# repeat=True makes it loop indefinitely
ani = animation.FuncAnimation(
    fig_anim, 
    update, 
    frames=len(time_proc),
    init_func=init, 
    blit=True, 
    interval=20, 
    repeat=True
)

# Show all windows (both your static grid and the animation)
plt.show()
