
#  Copyright (C) 2018 University of Tuebingen
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

import numpy as np

class MarkovChain(object):

    def __init__(self, states: np.ndarray, initial_state_vector: np.ndarray, state_designation: np.ndarray=None):

        """
        Constructor of the interface class Markov cChain
        :param states: states of the Markov chain
        :param initial_state_vector:  vector which indicates the system state at beginning of the analysis
        :param state_designation: designation of the states of the Markov chain
        """
        self._number_of_states = len(initial_state_vector)
        if states is None:
            self._states = range(self.get_number_of_states())
        else:
            self._states = states
        self._state_designations = state_designation
        self._initial_state_vector = initial_state_vector
        self._type = "MarkovChain"
        self._graph = None
        self._closures = []
        self._period = 0
        self._stationary_state_distribution = None



    def get_initial_state_vector(self):
        """
        Getter method of the initial state vector
        :return: initial state vector
        """
        return self._initial_state_vector[:]


    def get_state_designations(self):
        """
        Getter method of the state designations
        :return: state designations
        """
        return self._state_designations

    def get_states(self):
        """
        Getter method of the state space
        :return: states
        """
        return self._states

    def get_number_of_states(self):
        """
        Getter method of the cardinality of the state space
        :return: cardinality of states
        """
        return self._number_of_states

    def get_type(self):
        """
        Getter method of Markov chain type
        :return: MC type
        """
        return self._type

    def set_graph(self, graph):
        """
        Setter method of the MC graph
        """
        self._graph = graph

    def get_graph(self):
        """
        Getter method of MC graph
        :return: MC graph
        """
        return self._graph

    def set_closures(self, closures):
        """
        Setter method of the MC closures
        """
        self._closures = closures

    def get_closures(self):
        """
        Getter method of MC closures
        :return: MC closures
        """
        return self._closures

    def set_period(self, period):
        """
        Setter method of the MC period
        """
        self._period = period

    def get_period(self):
        """
        Getter method of the period of the MC
        :return period
        """
        return self._period

    def set_stationary_state_distribution(self, ssd):
        """
        Setter method of the stationary state distribution of the MC
        """
        self._stationary_state_distribution = ssd

    def get_stationary_state_distribution(self):
        """
        Getter method of the stationary state distribution of the MC
        :return stationary state distribution
        """
        return self._stationary_state_distribution
