import csv
import matplotlib.pyplot as plt
import math

with open("Test/Gravity.csv") as dataobject:#, open("Test/Orientation.csv") as orientationobject:
    #Preprocessing
    data = tuple(tuple(float(item) for item in row) for row in list(csv.reader(dataobject))[1:]) # Because Accelerometer actually records before orientation sensor does
    # Time, seconds_elapsed,z,y,x
    # orientation = tuple(tuple(float(item) for item in row) for row in list(csv.reader(orientationobject))[1:])

    # Centering averages
    # avg_x_displ = sum(datum[1] for datum in data)/len(data)
    # avg_y_displ = sum(datum[2] for datum in data)/len(data)
    # avg_z_displ = sum(datum[3] for datum in data)/len(data)
    # processed = []
    # for row in data:
    #     processed.append((row[0], row[1] - avg_x_displ, row[2] - avg_y_displ, row[3] - avg_z_displ))
    # data = tuple(processed)

    # oriented_accel = [] # ( acceleration_towards_north, acceleration_towards_east )

    index = 0
    # for row in data:
    #     try:
    #         oriented_accel.append((row[2]*math.sin(math.pi/2-orientation[index][-1]) + row[3]*math.sin(orientation[index][-1]-math.pi)))
    #         index += 1
    #     except IndexError:
    #         break

    x_vel_net = 0
    y_vel_net = 0
    z_vel_net = 0
    x_displ_net = 0
    y_displ_net = 0
    z_displ_net = 0
    vel = []
    displ = []
    pred = []

    index = 0
    for row in data: # Integrating to Velocity ----------------------------------------------------------------------------------------
        try:
            dt = data[index+1][1] - row[1] # final time - initial time = change in time

            dx_accel = data[index+1][4] - row[4] # final x_accel - initial x_accel = the change in acceleration of x
            dx_vel = (dt * row[4]) + ((1/2) * dt * dx_accel) # triangle area + square area = area under accel graph = change in velocity
            x_vel_net += dx_vel

            dy_accel = data[index+1][2] - row[2] # final y_accel - initial y_accel = the change in acceleration of y
            dy_vel = (dt * row[2]) + ((1/2) * dt * dy_accel) # triangle area + square area = area under accel graph = change in velocity
            y_vel_net += dy_vel

            dz_accel = data[index+1][3] - row[3] # final z_accel - initial z_accel = the change in acceleration of z
            dz_vel = (dt * row[3]) + ((1/2) * dt * dz_accel) # triangle area + square area = area under accel graph = change in velocity
            z_vel_net += dz_vel

            # print(row)
            vel.append((row[0], x_vel_net, y_vel_net, z_vel_net))

            index += 1
        except IndexError:
            break



    # Centering Velocity Averages
    # avg_x_vel = sum(datum[1] for datum in vel)/len(vel)
    # avg_y_vel = sum(datum[2] for datum in vel)/len(vel)
    # avg_z_vel = sum(datum[3] for datum in vel)/len(vel)
    # processed = []
    # for row in vel:
    #     processed.append((row[0], row[1] - avg_x_vel, row[2] - avg_y_vel, row[3] - avg_z_vel))
    # vel = tuple(processed)

    index = 0
    for row in vel: # Integrating to Displacement ------------------------------------------------------------------------------------
        try:
            dt = vel[index+1][0] - row[0]
            
            dx_vel = vel[index+1][1] - row[1]
            dx_displ = (dt * row[1]) + ((1/2) * dt * dx_vel)
            x_displ_net += dx_displ
            
            dy_vel = vel[index+1][2] - row[2]
            dy_displ = (dt * row[2]) + ((1/2) * dt * dy_vel)
            y_displ_net += dy_displ
            
            dz_vel = vel[index+1][3] - row[3]
            dz_displ = (dt * row[3]) + ((1/2) * dt * dz_vel)
            z_displ_net += dz_displ

            displ.append((row[0], x_displ_net, y_displ_net, z_displ_net))

            index += 1
        except IndexError:
            break





# Processing Data -----------------------------------------------------------------------------
# proc = []
# index = 0
#
# for datum in displ:
#     proc.append(
#         (
#             datum[0],
#             datum[1] - displ[-1][1] * (index/len(displ)),
#             datum[2] - displ[-1][2] * (index/len(displ)),
#             datum[3] - displ[-1][3] * (index/len(displ))
#         )
#     )
#     index += 1



with open('accel.csv', 'w') as outaccel:

    file = csv.writer(outaccel)
    file.writerow(['Time', 'x', 'y', 'z'])
    file.writerows(accel)

with open('vel.csv', 'w') as outvel:

    file = csv.writer(outvel)
    file.writerow(['Time', 'x', 'y', 'z'])
    file.writerows(vel)
    
with open('displ.csv', 'w') as outdispl:

    file = csv.writer(outdispl)
    file.writerow(['Time', 'x', 'y', 'z'])
    file.writerows(displ)


# AI generated plotting stuff ----------------------------------------------------------------

# 1. Extract the columns directly by choosing the correct index
times_accel = [float(row[1]) for row in data[1:]]
x_accels    = [float(row[4]) for row in data[1:]]

times_vel   = [row[0] for row in vel]
x_vels      = [row[1] for row in vel]

times_displ = [row[0] for row in displ]
x_displs    = [row[1] for row in displ]

# 2. Tell matplotlib to stack 3 subplots vertically
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

# 3. Plot using the matching time arrays
ax1.plot(times_accel, x_accels)
ax2.plot(times_vel, x_vels)
ax3.plot(times_displ, x_displs)
plt.show()

