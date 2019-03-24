#!/usr/bin/env python3
"""
model.py - The driver for the VarBee model

Here one can set the model parameters for the VarBee model.

The number of bees and the number of iterations has a big impact on the
running time of the model. While the model is running, the progress is
displayed in the terminal window as a percent the model is complete.
"""
# TODO: Place mites
import csv
import random
import varbee

NUM_BEES = 50
HIVES = {} #Store hives as a dict so bees can access the obj by location
NUM_HIVES = 1
HIVE_LOCATIONS = [(25, 25)] # Just one hive for now
ENVIRONMENT = []
NUM_ITERATIONS = 500
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
                hive_location=(25,25), hives=HIVES, bees=BEES))

# Make a heat map for all locations
for i in range(len(ENVIRONMENT[0])):
    for j in range(len(ENVIRONMENT)):
        heat_map[(i, j)] = 0

def update():

    # Move Bees
    if len(BEES) > 0:
        for k in range(len(BEES)):
            # Move bees
            BEES[k].update()

        # Count the number of bees in the current location and add to a dict
        for i in range(len(ENVIRONMENT)):
            for j in range(len(ENVIRONMENT[0])):
                for bee in BEES:
                    if tuple(bee.current_position) == (i, j):
                        heat_map[(i, j)] += 1

    # Cleanup dead insects
    if BEES:
        bees_to_remove = []
        for i in range(len(BEES)):
            if not BEES[i].alive:
                bees_to_remove.append(BEES[i])

        for i in bees_to_remove:
            print("Removing BEE ", i, "Lifespan was ", i.lifespan)
            BEES.remove(i)

print("Percent completed:")
for i in range(NUM_ITERATIONS):
    print(int((i / NUM_ITERATIONS) * 100.0), "\r", end='', flush=True)
    update()
print()

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
