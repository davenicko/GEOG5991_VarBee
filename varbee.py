#!/usr/bin/env python3
# -*- Coding UTF-8 -*-
# varbee.py - the classes used for the VarBee model
"""
VarBee.py

@author: David Nicholson

A module containing the classes needed for the VarBee model. The classes
contained are as follows:

    - Insect
    - Bee
    - Mite
    - Hive
    - Flower
    """

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
        self.set_current_mode(current_mode)
        self.set_virus_present(virus_present)
        self.set_environment(environment)
        self.set_mode_list(mode_list)

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
        if value in mode_list:
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
    def __init__(self, lifespan, current_mode, virus_present, environment,
                 mode_list, known_flower_locations, max_nectar_level,
                 nectar_level, current_position):
        """
        Initialise the Bee class

        lifespan:               The lifespan of the insect in time units of
                                the model run
        current_mode:           The current objective of the insect, i.e. what
                                it is currently aiming to do
        virus_present:          True if the virus is present, False otherwise
        environment:            A copy of the environment the agents occupy
        mode_list:              A list of strings describing the valid modes
        known_flower_locations: A list of tuples containing the coordinates
                                of known flowers (i.e. food sources)
        max_nectar_level:       The maximum nectar the bee can carry
        nectar_level:           The current level of nectar
        """
        Insect.__init__(self, lifespan, current_mode, virus_present,
                        environment, mode_list)
        self._known_flower_locations = known_flower_locations
        self._max_nectar_level = max_nectar_level
        self._nectar_level = 0

    def move(self):
        pass

    def search(self):
        pass

    def feed(self):
        pass

    def forage(self):
        pass

    def swarm(self):
        pass

    def get_flower_locations(self):
        pass
