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

class Insect():
    """
    THe Insect class is a super class used as the basis for the insects in the
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

    def change_mode(self, mode):
        """
        change_mode takes a string and sets the mode to that string

        mode:       The mode to change to
        """
        self.set_current_mode(mode)

    ###########################################################################
    #                                                                         #
    # Get, set and del methods for each variable                              #
    #                                                                         #
    ###########################################################################

    def get_lifespan(self):
        """return the lifespan"""
        return self._lifespan

    def get_current_mode(self):
        """return the current mode"""
        return self._current_mode

    def get_virus_present(self):
        """return the virus presence or absence"""
        return self._virus_present

    def get_environment(self):
        """return the environment"""
        return self._environment

    def get_mode_list(self):
        """return the mode list"""
        return self._mode_list

    def set_lifespan(self, value):
        """Set the lifespan"""
        self._lifespan = value

    def set_current_mode(self, value):
        """Set the current mode"""
        if value in self.mode_list:
            self._current_mode = value

    def set_virus_present(self, value):
        """Set the virus presence or absence"""
        self._virus_present = value

    def set_environment(self, value):
        """Set the environment"""
        self._environment = value

    def set_mode_list(self, value):
        """Set the mode list"""
        self._mode_list = value

    def del_lifespan(self):
        """Delete the lifespan"""
        del self._lifespan

    def del_current_mode(self):
        """Delete the current mode"""
        del self._current_mode

    def del_virus_present(self):
        """Delete the virus presence or absence"""
        del self._virus_present

    def del_environment(self):
        """Delete the environment"""
        del self._environment

    def del_mode_list(self):
        """Delete the mode list"""
        del self._mode_list

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
    The class representing the Bee. contains all of the attributes of the
    Insect class, plus those needed by the Bee class.
    """
    def __init__(self, lifespan=100, current_mode="SEARCH",
                 virus_present=False, environment=[],
                 mode_list=["SEARCH",
                            "FORAGE"],
                 hive_location=(),
                 hives = {},
                 max_nectar_level=100):
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

    def update(self):
        """
        Decide what to do, be that any of the following:
            - move
            - forage for nectar if at the target flower
            - drop nectar and set new target if at the hive
            - check and set the current target
        """
        # Set a variable containing our bees hive object
        own_hive = self.hives[self.hive_location]

        if self.current_mode == "FORAGE":
            if self.check_pos(self.current_position, self.current_target):
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

        self.take_move(self.current_target)

        if self.current_mode == "SEARCH":
            if (self.environment[self.current_position[0]]
                    [self.current_position[1]] > 0):
                self.current_target = self.current_position
                self.current_mode = "FORAGE"

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

#    def update(self):
#        """
#        Update the bee status
#        """
#        self.set_lifespan(self.get_lifespan() - 1)
#
#    def feed(self):
#        pass
#
#    def forage(self):
#        pass

    def get_flower_locations(self):
        pass

    def set_initial_position(self):
        """
        Sets the initial position of the agent

        returns: A numpy array with the position
        """
        # Set the initial position to that of the hive
        return self.hive_location

    def set_position(self, position):
        """
        Set the current position. Takes a numpy array
        """
        self._current_position = position

    def set_hive_location(self, position):
        """
        Set the current hive location. Takes a tuple
        """
        if (0 <= position[0] <= len(self.environment) and
                0 <= position[1] <= len(self.environment)):
            self._hive_location = position
        else:
            print("hive_location not valid, setting to the middle of the\
                   environment")
            self._hive_location = ((len(self.environment[0]/2)),
                                   len(self.environment[1]/2))

    def set_current_target(self, target):
        """
        Set the current target.

        target: A tuple containing the target coordinates
        """
        self._current_target = target

    def get_position(self):
        """
        Get the current position
        """
        return self._current_position

    def get_hive_location(self):
        """
        Get the current hive location
        """
        return self._hive_location

    def get_current_target(self):
        """
        Get the current target
        """
        return self._current_target

    def del_position(self):
        """
        Delete the current position
        """
        del self._current_position

    def del_hive_locaton(self):
        """
        Delete the hive location
        """
#        del self._hive_location
        print("cannot delete hive location!")

    def del_current_target(self):
        """
        Delete the current target
        """
        del self._current_target

    current_position = property(get_position, set_position, del_position,
                                "The current position")
    hive_location = property(get_hive_location, set_hive_location,
                             del_hive_locaton, "The hive location")
    current_target = property(get_current_target, set_current_target,
                              del_current_target, "The current target")

class Hive:
    """
    The hive class. Used as a base for the bees storing food and flower
    location information
    """
    def __init__(self, environment, hive_location):
        """
        Initialise the hive with its location, an empty dict to store the
        current knowledge of flower locations and nectar levels
        """
        self.set_environment(environment)
        self.set_hive_location(hive_location)
        self.known_flower_locations = {}
        self.hive_store = 0

    def get_hive_location(self):
        """
        Get the current hive location
        """
        return self._hive_location

    def set_hive_location(self, position):
        """
        Set the hive location, checking it lies within the environment
        """
        if (0 <= position[0] <= len(self.environment) and
                0 <= position[1] <= len(self.environment)):
            self._hive_location = position
        else:
            print("hive_location not valid, setting to the middle of the\
                   environment")
            self._hive_location = ((len(self.environment[0]/2)),
                                   len(self.environment[1]/2))

    def del_hive_location(self):
        """
        Delete the current hive location
        """
        del self._hive_location

    def get_environment(self):
        """
        Get the current environment
        """
        return self._environment

    def set_environment(self, value):
        """Set the environment"""
        self._environment = value

    def del_environment(self):
        """Set the environment"""
        del self._environment

#    def get_known_flower_locations(self):
#        """return the mode list"""
#        return self._known_flower_locations
#
#    def set_known_flower_locations(self, value):
#        """Set the mode list"""
#        self._known_flower_locations = value
#
#    def append_flower_location(self, location, value):
#        """
#        Append a new (or update an existing) flower location to the dict
#        """
#        self._known_flower_locations[location] = value
#
#    def del_known_flower_locations(self):
#        """Delete the mode list"""
#        del self._known_flower_locations

    environment = property(get_environment, set_environment, del_environment,
                           "The environment")
    hive_location = property(get_hive_location, set_hive_location,
                             del_hive_location, "The hive location")
