#!/usr/bin/env python3
"""
NAME
    model.py - The driver for the VarBee model

SYNOPSIS
    python3 model.py File [number1] [number2] [number3]

    File: A CSV file containing the environment
    number1: The Number of iterations to run
    number2: The number of bees to start with
    number3: The number of mites to start with

DESCRIPTION
    The model simulates

    The number of bees and the number of iterations has a big impact on the
    running time of the model. While the model is running, the progress is
    displayed in the terminal window as a percent the model is complete.
"""
###############################################################################
#                                                                             #
#  Python library imports                                                     #
#                                                                             #
###############################################################################
import sys
import csv
import random
import matplotlib.pyplot as plt
import numpy as np

###############################################################################
#                                                                             #
#  Custom imports                                                             #
#                                                                             #
###############################################################################
import varbee

###############################################################################
#                                                                             #
#  Model parameters                                                           #
#                                                                             #
###############################################################################
ENVIRONMENT_FILE = 'environment_weighted.csv'
NUM_BEES = 40
NUM_MITES = 40
NUM_HIVES = 1
HIVE_LOCATIONS = [(25, 25)] # Just one hive for now
NUM_ITERATIONS = 100

###############################################################################
#                                                                             #
#  Model storage structures                                                   #
#                                                                             #
###############################################################################
HIVES = {} #Store hives as a dict so bees can access the obj by location
BEES = []
ENVIRONMENT = []
MITES = []
bee_count = {}
mite_pop = []
bee_pop = []

###############################################################################
#                                                                             #
#  Model start                                                                #
#                                                                             #
###############################################################################

#Command line processing
try:
    if sys.argv[1]:
        ENVIRONMENT_FILE = sys.argv[1]
    if int(sys.argv[2]) > 0:
        NUM_ITERATIONS = int(sys.argv[2])
    if int(sys.argv[3]) > 0:
        NUM_BEES = int(sys.argv[3])
    if int(sys.argv[4]) > 0:
        NUM_MITES = int(sys.argv[4])
except:
    pass

# check all rows have same number of columns
def col_check(input_list):
    '''
    Function to check all rows have the same number of columns.

    returns:    True if all columns are the same, False otherwise
    '''
    incorrect_cols = []

    for row in input_list:
        col_zero = col_count(input_list[0])
        if col_count(row) == col_zero:
            incorrect_cols.append(0)
        else:
            incorrect_cols.append(1)

    if sum(incorrect_cols) != 0:
        return False
    else:
        return True

def col_count(col):
    count = 0
    for value in col:
        if value != '':
            count += 1
    return count

# Initialise environment
with open(ENVIRONMENT_FILE, newline='') as file1:
    DATASET = csv.reader(file1, quoting=csv.QUOTE_NONNUMERIC)
    for row in DATASET:
        rowlist = []
        for value in row:
            if value != '':
                rowlist.append(int(value))
        ENVIRONMENT.append(rowlist)

if not col_check(ENVIRONMENT):
    print("The environment file does not have an equal number of columns.\
          Model run aborted")
    raise IndexError

# Create the environment object
environment_object = varbee.Environment(ENVIRONMENT)

# Create the hive(s)
for j in range(NUM_HIVES):
    HIVES[HIVE_LOCATIONS[j]] = varbee.Hive(environment=ENVIRONMENT,
                                           hive_location=HIVE_LOCATIONS[j],
                                           bees=BEES,
                                           num_iterations=NUM_ITERATIONS)

# Create Bees
hivechoice = random.choice([i for i in range(len(HIVES))])
for j in range(NUM_BEES):
    BEES.append(varbee.Bee(environment=ENVIRONMENT,
                hive_location=(25,25), hives=HIVES, bees=BEES, mites=MITES))

# Create mites in random locations
for i in range(NUM_MITES):
    randloc = (random.randint(0, len(ENVIRONMENT[0])),
               random.randint(0, len(ENVIRONMENT)))
    MITES.append(varbee.Mite(current_position=randloc, environment=ENVIRONMENT,
                             bees=BEES, mites=MITES))

# Make a blank heat map for all locations
for i in range(len(ENVIRONMENT[0])):
    for j in range(len(ENVIRONMENT)):
        bee_count[(i, j)] = 0

def update():

    # Process mites
    if MITES:
        for mite in MITES:
            mite.update()

    # Move Bees
    if BEES:
        for bee in BEES:
            bee.update()

        # Count the number of bees in the current location and add to a dict
        for i in range(len(ENVIRONMENT)):
            for j in range(len(ENVIRONMENT[0])):
                for bee in BEES:
                    if tuple(bee.current_position) == (i, j):
                        bee_count[(i, j)] += 1

    # Hive actions (make more bees)
    if HIVES:
        for location in HIVES:
            HIVES[location].update()

    # Clean up dead insects
    if BEES:
        bees_to_remove = []
        for bee in BEES:
            if not bee.alive:
                bees_to_remove.append(bee)

        for i in bees_to_remove:
            BEES.remove(i)

    # If there are mites, move them
    if MITES:
        mites_to_remove = []
        for mite in MITES:
            if not mite.alive:
                mites_to_remove.append(mite)

        for i in mites_to_remove:
            MITES.remove(i)

    # Update the environment
    environment_object.update()


for i in range(NUM_ITERATIONS):
    print("Percent completed: ", int((i / NUM_ITERATIONS) * 100.0),
          "\tNumber of bees remaining = ", len(BEES),
          "\tNumber of mites remaining = ", len(MITES), "\r",
          end='', flush=True)
    update()

    # Log the bee and mite populations
    bee_pop.append(len(BEES))
    mite_pop.append(len(MITES))

print()

fig, ax = plt.subplots()

color = 'tab:green'
ax.plot([i for i in range(len(bee_pop))], bee_pop, color=color)
ax.tick_params(axis='y', labelcolor=color)
ax.set_ylabel("Bee population", color=color)

ax2 = ax.twinx()

color = 'tab:red'
ax2.plot([i for i in range(len(mite_pop))], mite_pop, color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylabel("Mite population", color=color)

plt.xlabel("Time-Step")
plt.title("The Population of Bees and Mites. Timestep = %s" %NUM_ITERATIONS)

plt.show()

# Create a heatmap of the total number of bees in each position on the map
heat = []
heat_initial = [i for i in range(len(ENVIRONMENT[0]))]
for i in range(len(ENVIRONMENT)):
    heat.append(heat_initial[:])
for key in bee_count.keys():
    heat[key[0]][key[1]] = bee_count[key]

with open('heatmap.csv', 'w', newline='') as file2:
    writer = csv.writer(file2)
    for row in heat:
        writer.writerow(row)

with open('results.csv', 'w', newline='') as file3:
    writer = csv.writer(file3)
    for i in range(len(bee_pop)):
        row = [i, bee_pop[i], mite_pop[i]]
        writer.writerow(row)
