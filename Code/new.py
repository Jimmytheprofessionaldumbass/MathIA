import csv
import math

with open("Test/accelerometer.csv") as dataobject:
    data = tuple(tuple(float(item) for item in row) for row in list(csv.reader(dataobject))[1:])
    # The first row is 
