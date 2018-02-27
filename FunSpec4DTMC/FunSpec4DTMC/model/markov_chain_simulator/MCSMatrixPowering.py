
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
from FunSpec4DTMC.model.markov_chain_simulator.MarkovChainSimulator import MarkovChainSimulator
import FunSpec4DTMC.model.markov_chain.MarkovChain as MarkovChain


class MCSMatrixPowering(MarkovChainSimulator):
    def __init__(self, markov_chain: MarkovChain = None, identification: str = None):
        """
        Constructor MCSMatrixPowering
        :param: markov_chain: MarkovChainConventionalApproach
        :param: get_identification: str
        """
        MarkovChainSimulator.__init__(self, markov_chain, identification)
        self._type = "MCSMatrixPowering"

    def calculate_stationary_state_distribution(self, simulation_steps: int, alpha: float = 1, specified_period:int=1):
        """
        Method for calculating the stationary state distribution
        :param simulation_steps: number of iteration steps
        :param alpha: value used for the alpha relaxation
        :param specified_period: specified value for period
        :return stationary state distribution
        """
        state_distribution = self.get_markov_chain().get_initial_state_vector()[:]
        transition_matrix = self.get_markov_chain().get_transition_matrix().copy()
        predecessor_state_distribution = np.zeros(len(state_distribution))
        if simulation_steps == 0:
            step = 0
            norm = self.norm(state_distribution, predecessor_state_distribution)
            while norm > self.get_calculation_precision():
                step += 1
                try:
                    self.notify_calculation_listeners(step, norm)
                except:
                    raise InterruptedError
                predecessor_state_distribution = state_distribution
                transition_matrix = self._transition(transition_matrix)
                state_distribution = transition_matrix[0]
                state_distribution = alpha * state_distribution + \
                                     (1 - alpha) * predecessor_state_distribution
                state_distribution /= sum(state_distribution)
                norm = self.norm(state_distribution, predecessor_state_distribution)
            try:
                self.notify_calculation_listeners(step, norm)
            except:
                raise InterruptedError
        else:
            step = 0
            for step in range(1, simulation_steps):
                try:
                    self.notify_calculation_listeners(step)
                except:
                    raise InterruptedError
                predecessor_state_distribution = state_distribution
                transition_matrix = self._transition(transition_matrix)
                state_distribution = transition_matrix[0]
                state_distribution = alpha * state_distribution + \
                                     (1 - alpha) * predecessor_state_distribution
                state_distribution\
                    /= np.sum(state_distribution)
            norm = self.norm(state_distribution, predecessor_state_distribution)
            try:
                self.notify_calculation_listeners(step, norm)
            except:
                raise InterruptedError
        return state_distribution

    def _transition(self, transition_matrix):
        """
        Method for calculating the successor state distribution
        :param cesaro_sum: current state distribution
        :return: successor state distribution
        """
        transition_matrix = np.dot(transition_matrix, transition_matrix)
        for index in range(len(transition_matrix)):
            transition_matrix[index] = transition_matrix[index]/sum(transition_matrix[index])
        return transition_matrix
