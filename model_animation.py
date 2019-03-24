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
import random

NUM_BEES = 100
HIVES = {} #Store hives as a dict so bees can access the obj by location
NUM_HIVES = 1
HIVE_LOCATIONS = [(25, 25)]
ENVIRONMENT = []
NUM_ITERATIONS = 1
BEES = []
rowlist = []
heat_map = {}

# Initialise environment
with open('environment.csv', newline='') as file1:
    DATASET = csv.reader(file1, quoting=csv.QUOTE_NONNUMERIC)
    for row in DATASET:
        for values in row:
            rowlist.append(values)
        ENVIRONMENT.append(rowlist)
        rowlist = []

# Create the hive(s)
for j in range(NUM_HIVES):
    HIVES[HIVE_LOCATIONS[j]] = varbee.Hive(environment=ENVIRONMENT,
                                           hive_location=HIVE_LOCATIONS[j])

print(HIVES)

# Create Bees
hivechoice = random.choice([i for i in range(len(HIVES))])
print(hivechoice)
for j in range(NUM_BEES):
    BEES.append(varbee.Bee(environment=ENVIRONMENT,
                hive_location=(25,25), hives=HIVES))

# Make a heat map for all locations
for i in range(len(ENVIRONMENT[0])):
    for j in range(len(ENVIRONMENT)):
        heat_map[(i, j)] = 0

def update(frame_number):
    fig.clear()

    # Move Bees
    for i in range(NUM_ITERATIONS):
        for k in range(NUM_BEES):
            # Move bees
            BEES[k].update()

    # Count the number of bees in the current location and add to a dict
    for i in range(len(ENVIRONMENT)):
        for j in range(len(ENVIRONMENT[0])):
            for bee in BEES:
                if tuple(bee.current_position) == (i, j):
                    heat_map[(i, j)] += 1

    plt.imshow(ENVIRONMENT, interpolation='none')
    for i in range(NUM_BEES):
        plt.scatter(BEES[i].get_position()[0], BEES[i].get_position()[1],
                    color="yellow")
    plt.scatter(BEES[0].hive_location[0], BEES[0].hive_location[1],
                color = "pink")

fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

model_animation = animation.FuncAnimation(fig, update, 200, interval=1,
                                          repeat=False)
plt.show()

heat = []
heat_initial = [i for i in range(len(ENVIRONMENT[0]))]
for i in range(len(ENVIRONMENT)):
    heat.append(heat_initial[:])
for key in heat_map.keys():
    heat[key[0]][key[1]] = heat_map[key]

with open('heatmap.csv', 'w', newline='') as file2:
    writer = csv.writer(file2)
    for row in heat:
        writer.writerow(row)
