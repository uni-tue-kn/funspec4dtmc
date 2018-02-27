
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


class MCSLimitingDistribution(MarkovChainSimulator):

    def __init__(self, markov_chain: MarkovChain = None, identification: str=None):
        """
        Constructor MCSSeriesLimitSimulation
        :param markov_chain: MarkovChainConventionalApproach
        :param identification: str
        """
        MarkovChainSimulator.__init__(self, markov_chain, identification)
        self._type = "MCSLimitingDistributiion"

    def calculate_stationary_state_distribution(self, simulation_steps: int, alpha=1, specified_period:int=1):
        """
        Method for calculating the stationary state distribution
        :param simulation_steps: number of iteration steps
        :param alpha: value used for the alpha relaxation
        :param specified_period: specified value for period
        :return stationary state distribution
        """
        state_distribution = self.get_markov_chain().get_initial_state_vector()[:]
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
                state_distribution = alpha * self._transition(state_distribution) + \
                                                (1 - alpha) * state_distribution
                state_distribution /= sum(state_distribution)
                norm = self.norm(state_distribution, predecessor_state_distribution)
            try:
                self.notify_calculation_listeners(step, norm)
            except:
                raise InterruptedError
        else:
            step = 0
            for step in range(1, simulation_steps):
                self.notify_calculation_listeners(step)
                state_distribution = alpha * self._transition(state_distribution) + \
                                                (1 - alpha) * state_distribution
                state_distribution /= sum(state_distribution)
            norm = self.norm(state_distribution, predecessor_state_distribution)
            try:
                self.notify_calculation_listeners(step, norm)
            except:
                raise InterruptedError
        return state_distribution

    def _transition(self, state_distribution):
        """
        Calculates state distribution after a single transition step
        state distribution after transition i:
        x_{i+1} =  x_i * P
        :param state_distribution: current state distribution
        :return: successor state distribution
        """
        return np.dot(state_distribution, self._markov_chain.get_transition_matrix())
