import csv
import math

with open("best.csv") as dataobject:
    data = tuple(tuple(float(item) for item in row) for row in list(csv.reader(dataobject))[1:])
    '''((0.0, -0.120582856), (0.004999756, -0.120273575)'''
    
    mean = sum(datum[1] for datum in data)/len(data)
    data = [(datum[0], datum[1]-mean) for datum in data]

    vel = []
    accum_vel = 0

    for index,row in enumerate(data):
        try:
            dt = data[index+1][0] - row[0]
            da = data[index+1][1] - row[1]
            dv = dt*row[1] + (1/2) * da*dt

            accum_vel += dv
            vel.append((data[index+1][0], accum_vel))
        except IndexError:
            break

with open('aligned_best.csv', 'w') as velfile:
    file = csv.writer(velfile)
    file.writerow(('Time', 'x'))
    file.writerows(
        [format(datum, 'f') for datum in row]
        for row in vel
        )
