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
                 hive_location=(25,25),
                 known_flower_locations=[],
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
        known_flower_locations: A list of tuples containing the coordinates
                                of known flowers (i.e. food sources)
        max_nectar_level:       The maximum nectar the bee can carry
        nectar_level:           The current level of nectar
        """
        Insect.__init__(self, lifespan, current_mode, virus_present,
                        environment, mode_list)
        self.x_size = len(environment)
        self.y_size = len(environment[0])
        self._known_flower_locations = known_flower_locations
        self._max_nectar_level = max_nectar_level
        self._nectar_level = 0
        self._current_position = self.set_initial_position()
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

    def update(self):
        """
        Update the bee status
        """
        self.set_lifespan(self.get_lifespan() - 1)

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
        # Return an array with a random location
        # In the future first generate hives, then add bees?
        return np.array([random.choice(range(self.x_size)),
                         random.choice(range(self.y_size))])

    def set_position(self, position):
        """
        Set the current position. Takes a numpy array
        """
        self._current_position = position

    def get_position(self):
        """
        Get the current position
        """
        return self._current_position

    def del_position(self):
        """
        Delete the current position
        """
        del self._current_position

    current_position = property(get_position, set_position, del_position,
                                "The current position")
