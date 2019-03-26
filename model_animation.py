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

NUM_BEES = 40
NUM_MITES = 20
HIVES = {} #Store hives as a dict so bees can access the obj by location
NUM_HIVES = 1
HIVE_LOCATIONS = [(25, 25)]
ENVIRONMENT = []
NUM_ITERATIONS = 1
BEES = []
MITES = []
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
                                           hive_location=HIVE_LOCATIONS[j],
                                           bees=BEES, num_iterations=NUM_ITERATIONS)

print(HIVES)

# Create Bees
hivechoice = random.choice([i for i in range(len(HIVES))])
print(hivechoice)
for j in range(NUM_BEES):
    BEES.append(varbee.Bee(environment=ENVIRONMENT,
                hive_location=(25,25), hives=HIVES, bees=BEES, mites=MITES))

# Create mites in random locations
for i in range(NUM_MITES):
    randloc = (random.randint(0, len(ENVIRONMENT[0])),
               random.randint(0, len(ENVIRONMENT)))
    MITES.append(varbee.Mite(current_position=randloc, environment=ENVIRONMENT,
                             bees=BEES, mites=MITES))

# Make a heat map for all locations
for i in range(len(ENVIRONMENT[0])):
    for j in range(len(ENVIRONMENT)):
        heat_map[(i, j)] = 0

def update(frame_number):
    fig.clear()

    # Process mites
    if MITES:
        for mite in MITES:
            mite.update()
            #plt.scatter(mite.get_position()[0], mite.get_position()[1],
            #            color="red")

    # Move Bees
    if BEES:
        for bee in BEES:
            # Move bees
            bee.update()

        # Count the number of bees in the current location and add to a dict
        for i in range(len(ENVIRONMENT)):
            for j in range(len(ENVIRONMENT[0])):
                for bee in BEES:
                    if tuple(bee.current_position) == (i, j):
                        heat_map[(i, j)] += 1

        for bee in BEES:
            plt.scatter(bee.get_position()[0], bee.get_position()[1],
                        color="yellow")
        plt.scatter(BEES[0].hive_location[0], BEES[0].hive_location[1],
                color = "pink")

    plt.imshow(ENVIRONMENT, interpolation='none')

    # Hive actions (make more bees)
    if HIVES:
        for location in HIVES:
            HIVES[location].update()
            HIVES[location].status()

    # Cleanup dead insects
    if BEES:
        bees_to_remove = []
        for bee in BEES:
            if not bee.alive:
                bees_to_remove.append(bee)

        for bee in bees_to_remove:
            BEES.remove(bee)

    if MITES:
        mites_to_remove = []
        for mite in MITES:
            if not mite.alive:
                mites_to_remove.append(mite)

        for mite in mites_to_remove:
            MITES.remove(mite)

fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

model_animation = animation.FuncAnimation(fig, update, 400, interval=1,
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
