#!/usr/bin/env python3
# -*- Coding UTF-8 -*-
# varbee.py - the classes used for the VarBee model
"""
varbee.py

@author: David Nicholson

A module containing the classes needed for the VarBee model. The classes
contained are as follows:

    - Insect
    - Bee
    - Mite
    - Hive
    - Flower
    """
import random
import numpy as np

class Insect:
    """
    The Insect class is a super class used as the basis for the insects in the
    model. It contains the variables and methods common to all insect classes
    """

    def __init__(self, lifespan, current_mode, virus_present, environment,
                 mode_list):
        """
        Initialisation of the Insect superclass

        lifespan:      The lifespan of the insect in time units of the model
                       run
        current_mode:  The current objective of the insect, i.e. what it is
                       currently aiming to do
        virus_present: True if the virus is present, False otherwise
        environment:   A copy of the environment the agents occupy
        mode_list:     A list of valid modes for the insect
        """

        self.set_lifespan(lifespan)
        self.set_mode_list(mode_list)
        self.set_current_mode(current_mode)
        self.set_virus_present(virus_present)
        self.set_environment(environment)
        self.alive = True

    def change_mode(self, mode):
        """
        change_mode takes a string and sets the mode to that string

        mode:       The mode to change to
        """
        self.set_current_mode(mode)

    ###########################################################################
    #                                                                         #
    # Get, set and del methods                                                #
    #                                                                         #
    ###########################################################################

    def get_lifespan(self):
        return self._lifespan

    def get_current_mode(self):
        return self._current_mode

    def get_virus_present(self):
        return self._virus_present

    def get_environment(self):
        return self._environment

    def get_mode_list(self):
        return self._mode_list

    def set_lifespan(self, value):
        self._lifespan = value

    def set_current_mode(self, value):
        if value in self.mode_list:
            self._current_mode = value

    def set_virus_present(self, value):
        self._virus_present = value

    def set_environment(self, value):
        self._environment = value

    def set_mode_list(self, value):
        self._mode_list = value

    def del_lifespan(self):
        del self._lifespan

    def del_current_mode(self):
        del self._current_mode

    def del_virus_present(self):
        del self._virus_present

    def del_environment(self):
        del self._environment

    def del_mode_list(self):
        del self._mode_list

    ###########################################################################
    #                                                                         #
    # End of get, set and del methods                                         #
    #                                                                         #
    ###########################################################################

    lifespan = property(get_lifespan, set_lifespan, del_lifespan,
                        "The lifespan of the Insect")
    current_mode = property(get_current_mode, set_current_mode,
                            del_current_mode, "The current mode of the Insect")
    virus_present = property(get_virus_present, set_virus_present,
                             del_virus_present, "Presence of virus")
    environment = property(get_environment, set_environment, del_environment,
                           "The environment")
    mode_list = property(get_mode_list, set_mode_list, del_mode_list,
                         "The list of valid modes")

class Bee(Insect):
    """
    The class representing the Bee. Contains all of the attributes of the
    Insect class, plus those needed by the Bee class.
    """
    def __init__(self, lifespan=100, current_mode="SEARCH",
                 virus_present=False, environment=[],
                 mode_list=["SEARCH",
                            "FORAGE"],
                 hive_location=(),
                 hives={},
                 max_nectar_level=100,
                 bees=[],
                 mites=[]):

        """
        Initialise the Bee class

        lifespan:               The lifespan of the insect in time units of
                                the model run
        current_mode:           The current objective of the insect, i.e. what
                                it is currently aiming to do
        virus_present:          True if the virus is present, False otherwise
        environment:            The environment containing flower and hive
                                locations
        mode_list:              A list of strings describing the valid modes
        hive_location:          The location of this bees hive
        hives:                  a dictionary containing all the hives with
                                tuples of the coordinates as keys
        known_flower_locations: A list of tuples containing the coordinates
                                of known flowers (i.e. food sources)
        max_nectar_level:       The maximum nectar the bee can carry
        nectar_level:           The current level of nectar
        """
        Insect.__init__(self, lifespan, current_mode, virus_present,
                        environment, mode_list)
        self.x_size = len(environment)
        self.y_size = len(environment[0])
        self._max_nectar_level = max_nectar_level
        self._nectar_level = 0
        self.set_hive_location(hive_location)
        self._current_position = self.set_initial_position()
        self._current_target = None
        # Create the move array. I use a variable to hold it for
        # adding to another array to find the final position
        self.move = np.array([[-1, -1],
                              [-1, 0],
                              [-1, 1],
                              [0, -1],
                              [0, 1],
                              [1, -1],
                              [1, 0],
                              [1, 1]])
        self.store = 0
        self.last_target_amount = 0
        self.last_target_location = hive_location
        self.hives = hives
        self.bees = bees
        self.mites = mites

    def update(self):
        """
        Decide what to do, be that any of the following:
            - move
            - forage for nectar if at the target flower
            - drop nectar and set new target if at the hive
            - check and set the current target

        Note the use of tuple() to convert the numpy array so that the
        locations can be correctly compared.
        """
        # Set a variable containing our bees hive object
        own_hive = self.hives[self.hive_location]

        if self.current_mode == "FORAGE" and self.alive:
            if self.check_pos(self.current_position, self.current_target):
                # If the bee is at the hive
                if self.check_pos(self.current_position, self.hive_location):
                    #add the nectar to the hive store
                    own_hive.hive_store += self.store
                    self.store = 0
                    #add/change the last known nectar amount to the flower list
                    own_hive.known_flower_locations\
                            [tuple(self.last_target_location)] =\
                            self.last_target_amount
                    #change the target to the flower currently known to have
                    #the most nectar
                    self.current_target = max(own_hive.known_flower_locations,
                                              key=lambda key:
                                              own_hive.known_flower_locations[key])

                # If the bee isn't at the hive (and therefore the
                # target flower)
                else:
                    #if nectar level == 0, set the mode to search
                    if (self.environment[self.current_position[1]]
                            [self.current_position[0]] == 0):
                        self.current_mode = "SEARCH"
                    #take remaining nectar from the flower (if available)
                    if (0 < self.environment[self.current_position[1]]
                            [self.current_position[0]] < 10):
                        self.store += self.environment[self.current_position[1]]\
                                                 [self.current_position[0]]
                        self.environment[self.current_position[1]]\
                                   [self.current_position[0]] = 0
                        #and set target to the hive
                        self.current_target = self.hive_location
                        #set the last target location and amount
                        self.last_target_amount =\
                            self.environment[self.current_position[1]]\
                                       [self.current_position[0]]
                        self.last_target_location = tuple(self.current_position)
                    #take 10 nectar from the flower (if available)
                    if (self.environment[self.current_position[1]]
                            [self.current_position[0]] > 9):
                        self.store += 10
                        self.environment[self.current_position[1]]\
                                   [self.current_position[0]] -= 10
                        #and set target to the hive
                        self.current_target = self.hive_location
                        #set the last target location and amount
                        self.last_target_amount =\
                            self.environment[self.current_position[1]]\
                                       [self.current_position[0]]
                        self.last_target_location = tuple(self.current_position)

        if self.alive:
            self.take_move(self.current_target)

        if self.current_mode == "SEARCH" and self.alive:
            if (self.environment[self.current_position[0]]
                    [self.current_position[1]] > 0):
                self.current_target = self.current_position
                self.current_mode = "FORAGE"

        # Reduce the lifespan, reducing by more if infected with virus
        if self.virus_present:
            self.lifespan -=3
        self.lifespan -= 1
        # randomly determine if a bee should die. The bee will live at
        # least 55 time-steps
        if self.lifespan < random.randint(0, 45):
            self.alive = False

    def check_pos(self, pos1, pos2):
        """
        Check if one position is the same as another
        """
        if pos1[0] == pos2[0] and pos1[1] == pos2[1]:
            return True
        else:
            return False

    def take_move(self, current_target):
        """
        Move the bee. if set to SEARCH, perform a random move. If set to
        FORAGE move towards the current target (be it Hive or Flower)
        """
        if self.current_mode == "SEARCH":
            self.random_move()
        if self.current_mode == "FORAGE":
            self.targeted_move(current_target)

    def random_move(self):
        """
        Move the bee randomly. Choose a direction from the numpy array using
        random.choice, then set the new location by summing the arrays.
        """
        potential_position = self.get_position() + random.choice(self.move)
        while (potential_position[0] >= self.x_size or
               potential_position[0] < 0 or
               potential_position[1] >= self.y_size or
               potential_position[1] < 0):
            potential_position = self.get_position() + random.choice(self.move)

        self.set_position(potential_position)

    def targeted_move(self, target):
        """
        Take the shortest path to the target. The distance to the
        target from the current position is calculated for each
        of the eight possible directions. The shortest of these
        distances is chosen as the "move". If more than one direction
        is equal, a random direction is chosen

        target:     A tuple containing coordinates to the target
        """
        shortest_moves = []
        current_shortest = -1
        for possible_move in self.move:
            new_location = self.current_position + possible_move
            # If this is the first possible move, it is automatically the
            # shortest.
            if current_shortest == -1:
                current_shortest = self.distance_between(new_location, target)
                shortest_moves = [possible_move]
                next

            # If this potential move is is the shortest yet, set it as the
            # only move and reset distance
            if self.distance_between(new_location, target) < current_shortest:
                shortest_moves = [possible_move]
                current_shortest = self.distance_between(new_location,
                                                         target)

            # If this potential move is equal in distance to any previous
            # move, add it to the list of shortest moves
            if self.distance_between(new_location, target) == current_shortest:
                shortest_moves.append(possible_move)

        # Choose one of the shortest moves randomly
        self.current_position += random.choice(shortest_moves)

    def distance_between(self, location1, location2):
        """
        location1:   The first location for comparison
        location2:   The second location for comparison

        returns:     The Euclidian distance between the two location2s
        """
        return (((location1[0] - location2[0])**2) +
                ((location1[1] - location2[1])**2))**0.5

    def set_initial_position(self):
        """
        Sets the initial position of the agent

        returns: A numpy array with the position
        """
        # Set the initial position to that of the hive
        return self.hive_location

    ###########################################################################
    #                                                                         #
    # Get, set and del methods                                                #
    #                                                                         #
    ###########################################################################
    def set_position(self, position):
        self._current_position = position

    def set_hive_location(self, position):
        if (0 <= position[0] <= len(self.environment) and
                0 <= position[1] <= len(self.environment)):
            self._hive_location = position
        else:
            print("hive_location not valid, setting to the middle of the\
                   environment")
            self._hive_location = ((len(self.environment[0]/2)),
                                   len(self.environment[1]/2))

    def set_current_target(self, target):
        self._current_target = target

    def set_max_nectar_level(self, target):
        self._max_nectar_level = target

    def get_position(self):
        return self._current_position

    def get_hive_location(self):
        return self._hive_location

    def get_current_target(self):
        return self._current_target

    def get_max_nectar_level(self):
        return self._max_nectar_level

    def del_position(self):
        del self._current_position

    def del_hive_locaton(self):
        del self._hive_location

    def del_current_target(self):
        del self._current_target

    def del_max_nectar_level(self):
        del self._max_nectar_level

    ###########################################################################
    #                                                                         #
    # End get, set and del methods                                            #
    #                                                                         #
    ###########################################################################

    current_position = property(get_position, set_position, del_position,
                                "The current position")
    hive_location = property(get_hive_location, set_hive_location,
                             del_hive_locaton, "The hive location")
    current_target = property(get_current_target, set_current_target,
                              del_current_target, "The current target")
    max_nectar_level = property(get_max_nectar_level, set_max_nectar_level,
                                del_max_nectar_level, "The max nectar level")

class Hive:
    """
    The hive class. Used as a base for the bees storing food and flower
    location information
    """
    def __init__(self, environment, hive_location, bees, num_iterations):
        """
        Initialise the hive with its location, an empty dict to store the
        current knowledge of flower locations and nectar levels
        """
        self.set_environment(environment)
        self.set_hive_location(hive_location)
        self.known_flower_locations = {}
        self.hive_store = 0
        self.bees = bees
        self.timestep = 1
        self.num_iterations = num_iterations

    def update(self):
        """
        Update hive - increase the bee numbers by one bee per timestep
        """
        self.bees.append(Bee(lifespan=100,
                             current_mode="SEARCH",
                             virus_present=False,
                             environment=self.environment,
                             mode_list=["SEARCH",
                                        "FORAGE"],
                             hive_location=self.hive_location,
                             hives=self.bees[0].hives,
                             max_nectar_level=self.bees[0].get_max_nectar_level,
                             bees=self.bees))

    ###########################################################################
    #                                                                         #
    # Get, set and del methods                                                #
    #                                                                         #
    ###########################################################################

    def get_hive_location(self):
        return self._hive_location

    def set_hive_location(self, position):
        if (0 <= position[0] <= len(self.environment) and
                0 <= position[1] <= len(self.environment)):
            self._hive_location = position
        else:
            print("hive_location not valid, setting to the middle of the\
                   environment")
            self._hive_location = ((len(self.environment[0]/2)),
                                   len(self.environment[1]/2))

    def del_hive_location(self):
        del self._hive_location

    def get_environment(self):
        return self._environment

    def set_environment(self, value):
        self._environment = value

    def del_environment(self):
        del self._environment

    ###########################################################################
    #                                                                         #
    # End get, set and del methods                                            #
    #                                                                         #
    ###########################################################################

    environment = property(get_environment, set_environment, del_environment,
                           "The environment")
    hive_location = property(get_hive_location, set_hive_location,
                             del_hive_location, "The hive location")

class Mite(Insect):
    """
    The mite class. This agent is different as it doesn't have the
    ability to move of its own accord. The mite starts off in a random
    place in the environment (i.e. on a flower) and waits for a bee.
    When a bee arrives the mite attaches to the bee and is transported
    to the hive.

    Each time-step, the mite has a chance to reproduce, and if above
    the carrying capacity of the bee, the new mite will fall off in the
    current location.

    TODO: Implement lifespan reduction of bees.
    """
    def __init__(self, host_infected=None, current_position=(0, 0),
                 lifespan=100, current_mode="WAIT",
                 virus_present=False, environment=[],
                 mode_list=["WAIT",
                            "TRANSPORT",
                            "REPRODUCE",
                            "DROP"],
                 bees=[],
                 mites=[]):
        """
        Initialise the mite.
        """
        Insect.__init__(self, lifespan, current_mode,
                        virus_present, environment,
                        mode_list)
        self.host_infected = host_infected
        self.current_position = current_position
        self.bees = bees
        self.mites = mites

    def update(self):
        """
        Perform an update for the mite class. First perform operations
        depending on the current mode, then do a lifespan check. Note
        that if the bee carrying the mites dies, it is also assumed
        that the mites die.
        """
        if self.current_mode == "WAIT":
            self.wait()

        if self.current_mode == "TRANSPORT":
            self.transport()

        if self.current_mode == "REPRODUCE":
            self.reproduce()

        if self.current_mode == "DROP":
            self.drop()

        self.lifespan -= 1
        if self.host_infected:
            self.host_infected.lifespan -= 1
            if not self.host_infected.alive:
                self.alive = False
        if random.randint(0, 45) > self.lifespan:
            self.alive = False

    def wait(self):
        """
        Perform actions while waiting
        """
        # Check if there are any bees in the current location
        bees_here = []
        for bee in self.bees:
            if tuple(bee.current_position) == tuple(self.current_position):
                bees_here.append(bee)

        # If there are bees, randomly attach to one
        if bees_here:
            self.infect(random.choice(bees_here))
            self.current_mode = "TRANSPORT"

        # Mites waiting are dormant and assumed they won't die
        self.lifespan += 1

    def transport(self):
        """
        Perform actions to wait on a bee until the hive is reached
        """
        self.current_position = self.host_infected.current_position
        if tuple(self.current_position) == tuple(self.host_infected.hive_location):
            self.current_mode = "REPRODUCE"
            self.host_infected = None
        # Small chance the mite will drop off
        if random.randint(0, 100) < 2:
            self.current_mode = "WAIT"
            self.drop()

    def reproduce(self):
        """
        If in a hive there is a chance to reproduce and a chance to attach
        to a new bee.

        The mite population will not increase if it is greater than four
        times the bee population.
        """
        if random.randint(0, len(self.bees) * 4) > len(self.mites):
            self.mites.append(Mite(current_position=self.current_position,
                                   environment=self.environment,
                                   bees=self.bees, mites=self.mites))

        if random.randint(0, 100) > 95:
            self.current_mode = "WAIT"

    def drop(self):
        """
        Drop in the current location (i.e. set mode to wait)
        """
        self.host_infected = None
        self.current_mode = "WAIT"

    def infect(self, host):
        """
        Infect a host when one appears at the same location
        """
        self.host_infected = host

    def get_position(self):
        """ Get the current position """
        return self.current_position

class Environment:
    """
    The environment class is used to update the environment - i,e, the
    "growth" of flowers
    """
    def __init__(self, environment):
        self.environment = environment
        self.replenishment = self.replenish_calc(environment)

    def replenish_calc(self, environment):
        """
        Calculate a grid to determine how much to replenish the
        environment by. Note that not all squares will replenish.

        environment: A list representing the environment

        returns: A list containing how much to replenish the environment
        """
        temp_replenishment = []
        original_environment = []
        for row in environment:
            temp_row = []
            temp_original_environment = []
            for value in row:
                # The replenishment follows an exponential curve
                temp_row.append(int(value**2/2000))
                # copy the environment so we don't produce too many resources
                temp_original_environment.append(value)
            temp_replenishment.append(temp_row)
            original_environment.append(temp_original_environment)
        self.original_environment = original_environment
        return temp_replenishment

    def update(self):
        """
        Update the environment, based on the replenishment list.
        """
        for row in range(len(self.environment)):
            for val in range(len(self.environment[row])):
                if self.environment[row][val] < self.original_environment[row][val]:
                    self.environment[row][val] += self.replenishment[row][val]
