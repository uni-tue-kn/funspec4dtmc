
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

from FunSpec4DTMC.model.markov_chain.MarkovChain import MarkovChain

class MarkovChainForwardApproach(MarkovChain):

    def __init__(self, initial_state_vector, state_space_names, factors, factor_space_names, factor_distribution, transition_functions,
                 states=None, state_designation=None) -> None:
        """
        Constructor for Markov chains in functional specification
        :param initial_state_vector: vector of the initial state distribution
        :param state_space_names: names of the various state spaces
        :param factors: factors that indicate the Markov chain behaviour
        :param factor_space_names: names of the factor space
        :param factor_distribution: distribution of the factors
        :param transition_functions: transition functions affecting the system behaviour
        :param states: state space of the Markov chain
        :param state_designation: designations of the states of the Markov chain
        """
        MarkovChain.__init__(self, states, initial_state_vector, state_designation)
        self._state_space_names = state_space_names
        self._factors = factors
        self._factor_space_names = factor_space_names
        self._factor_distributions = factor_distribution
        self._transition_functions = transition_functions
        self._type = "MarkovChainForwardApproach"

    def get_state_space_names(self):
        """
        etter method for the state space names
        :return: state space names
        """
        return self._state_space_names

    def get_factors(self):
        """
        Getter method for the factors of the MC definiton
        :return: factors
        """
        return self._factors

    def get_factor_space_names(self):
        """
        Getter method for the factors space names of the MC definiton
        :return: factor space names
        """
        return self._factor_space_names

    def get_factor_distributions(self):
        """
        Getter method for the factor probabilities of the MC definiton
        :return: factor probabilities
        """
        return self._factor_distributions

    def get_transition_functions(self):
        """
        Getter method for the transition functions of the MC definiton
        :return: transition functions
        """
        return self._transition_functions

    def get_type(self):
        """
        returns the type MarkovChainForwardApproach
        :return: type MarkovchainApproach
        """
        return self._type

