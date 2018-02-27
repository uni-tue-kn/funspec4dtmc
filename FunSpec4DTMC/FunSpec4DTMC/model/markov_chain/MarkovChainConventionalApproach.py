
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
from FunSpec4DTMC.model.markov_chain.MarkovChain import MarkovChain

class MarkovChainConventionalApproach(MarkovChain):

    def __init__(self, initial_state_vector: np.ndarray, transition_matrix: np.ndarray,
                 state_designation: np.ndarray=None):
        """
        Constructor for Markov chains in conventional specification
        :param initial_state_vector: vector which indicates the system state at beginning of the analysis
        :param transition_matrix: matrix that defines the Markov chain
        :param state_designation: designation of the states of the Markov chain
        """
        if initial_state_vector is not None:
            MarkovChain.__init__(self, None, initial_state_vector, state_designation)
        if transition_matrix is not None:
            self._transition_matrix = TransitionMatrix(transition_matrix)
        self._type = "MarkovChainConventionalApproach"

    def get_transition_matrix(self):
        """
        Returns transition matrix of Markov chain
        :return: transition matrix
        """
        return self._transition_matrix.get_transition_matrix()

    def set_transition_matrix(self, transition_matrix: np.ndarray) -> None:
        """
        Sets the transition matrix of markov chain
        :param transition_matrix
        """
        self._transition_matrix = TransitionMatrix(transition_matrix)


    def get_type(self):
        """
        Getter method of the Markov chain
        :return: type: MarkovChainConventionalApproach
        """
        return self._type



class TransitionMatrix(object):

    def __init__(self, transition_matrix: np.ndarray):
        """
        Constructor of the class TransitionMatrix
        :param transition_matrix: stochastic matrix that defines the Markov chain
        """
        if self.check_for_probability_matrix(transition_matrix):
            if isinstance(transition_matrix[0], np.ndarray):
                self._transition_matrix = transition_matrix
                self._number_of_states_of_states = len(transition_matrix)

            elif isinstance(transition_matrix[0], np.float64):
                self._number_of_states_of_states = int(np.sqrt(len(transition_matrix)))
                self._transition_matrix = transition_matrix
                self._transition_matrix.shape = (self._number_of_states,
                                                 self._number_of_states)
            else:
                raise NotImplementedError
        else:
            raise FloatingPointError

    @staticmethod
    def check_for_probability_matrix(matrix: np.ndarray):
        """
        Checks the probability characteristic of a matrix
        :param: matrix: input matrix to check
        """
        dimension = matrix.shape
        if dimension[0] != dimension[1]:
            return False
        elif np.sum(matrix.sum(1) - np.ones(dimension[0])) > 10e-15:
            return False
        elif (matrix < 0).any():
            return False
        elif (matrix > 1).any():
            return False
        else:
            return True

    def set_transition_probability(self, resent_state: int, subsequent_state: int, transition_probability: int):
        """
        ...
        :param resent_state: state where transition begins
        :param subsequent_state: state where transition ends
        :param transition_probability: probability for transition from resent state to subsequent state
        """
        self._transition_matrix[resent_state][subsequent_state] = transition_probability
        if not self.check_for_probability_matrix( self._transition_matrix):
            raise ValueError

    def get_transition_matrix(self):
        """
        Returns stochastic transition matrix
        :rtype: TransitionMatrix
        """
        return self._transition_matrix

    def set_transition_matrix(self, tr_matrix: np.ndarray):
        """
        Sets transition matrix
        :param tr_matrix: matrix of floats
        """
        self._transition_matrix = tr_matrix
        if not self.check_for_probability_matrix(self._transition_matrix):
            raise ValueError


