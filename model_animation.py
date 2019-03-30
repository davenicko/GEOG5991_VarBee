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

def main():
###############################################################################
#                                                                             #
#  Model parameters                                                           #
#                                                                             #
###############################################################################
    NUM_BEES = 40
    NUM_MITES = 20
    NUM_HIVES = 1
    ENVIRONMENT_FILE = 'environment_weighted.csv'
    NUM_ITERATIONS = 1
    HIVE_LOCATIONS = [(25, 25)]

###############################################################################
#                                                                             #
#  Model storage structures                                                   #
#                                                                             #
###############################################################################
    HIVES = {} #Store hives as a dict so bees can access the obj by location
    ENVIRONMENT = []
    BEES = []
    MITES = []
    rowlist = []
    mite_pop = []
    bee_pop = []
    bee_count = {}

###############################################################################
#                                                                             #
#  Model start                                                                #
#                                                                             #
###############################################################################

    #Command line processing
    try:
        if sys.argv[1]:
            ENVIRONMENT_FILE = sys.argv[1]
    except:
        pass
    try:
        if int(sys.argv[2]) > 0:
            NUM_ITERATIONS = int(sys.argv[2])
    except:
        pass
    try:
        if int(sys.argv[3]) > 0:
            NUM_BEES = int(sys.argv[3])
    except:
        pass
    try:
        if int(sys.argv[4]) > 0:
            NUM_MITES = int(sys.argv[4])
    except:
        pass

    # Initialise environment
    with open(ENVIRONMENT_FILE, newline='') as file1:
        DATASET = csv.reader(file1, quoting=csv.QUOTE_NONNUMERIC)
        for row in DATASET:
            for values in row:
                rowlist.append(values)
            ENVIRONMENT.append(rowlist)
            rowlist = []

    if not col_check(ENVIRONMENT):
        print("The environment file does not have an equal number of columns.\
              Model run aborted")
        raise IndexError

    # Create the hive(s)
    for j in range(NUM_HIVES):
        HIVES[HIVE_LOCATIONS[j]] = varbee.Hive(environment=ENVIRONMENT,
                                               hive_location=HIVE_LOCATIONS[j],
                                               bees=BEES, num_iterations=NUM_ITERATIONS)

    # Create the environment object
    environment_object = varbee.Environment(ENVIRONMENT)

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

    # Make a heat map for all locations
    for i in range(len(ENVIRONMENT[0])):
        for j in range(len(ENVIRONMENT)):
            bee_count[(i, j)] = 0

    def update(frame_number):
        print("Timestep = ", frame_number, "/400\r", end='')
        fig.clear()

        # Process mites
        if MITES:
            for mite in MITES:
                mite.update()
                plt.scatter(mite.get_position()[0], mite.get_position()[1],
                            color="red")

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
                            bee_count[(i, j)] += 1

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

        # Update the environment - flower replenishment
        environment_object.update()
    
        # Log the bee and mite populations
        bee_pop.append(len(BEES))
        mite_pop.append(len(MITES))

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_axes([0, 0, 1, 1])

    model_animation = animation.FuncAnimation(fig, update, 400, interval=1,
                                              repeat=False)
    plt.show()

    # Create a heatmap of the total number of bees in each position
    # on the map
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
    '''
    Function to count the values in a list that contain a value
    '''
    count = 0
    for value in col:
        if value != '':
            count += 1
    return count

if __name__ == "__main__":
    main()
