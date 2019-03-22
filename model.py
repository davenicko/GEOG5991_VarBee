#!/usr/bin/env python3
# model.py - The driver for the VarBee model

# Set environment

# Place hives

# Place flowers

# Place bees in hives

# Place mites
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import varbee

NUM_BEES = 100
HIVE_LOCATION = (25, 25)
ENVIRONMENT = []
NUM_ITERATIONS = 1
BEES = []
rowlist = []

# Initialise environment
with open('environment.csv', newline='') as file1:
    DATASET = csv.reader(file1, quoting=csv.QUOTE_NONNUMERIC)
    for row in DATASET:
        for values in row:
            rowlist.append(values)
        ENVIRONMENT.append(rowlist)
        rowlist = []

# Create Bees
for j in range(NUM_BEES):
    BEES.append(varbee.Bee(environment=ENVIRONMENT))

def update(frame_number):
    fig.clear()

    # Move Bees
    for i in range(NUM_ITERATIONS):
        for k in range(NUM_BEES):
            # Move bees
            BEES[k].random_move()

    plt.imshow(ENVIRONMENT, interpolation='none')
    for i in range(NUM_BEES):
        plt.scatter(BEES[i].get_position()[0], BEES[i].get_position()[1])

fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

model_animation = animation.FuncAnimation(fig, update, 100, interval=1,
                                          repeat=False)
plt.show()
