
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
import FunSpec4DTMC.model.markov_chain.MarkovChain as MarkovChain
from FunSpec4DTMC.model.markov_chain_simulator.MarkovChainSimulator import MarkovChainSimulator


class MCSModifiedCesaroLimit(MarkovChainSimulator):

    def __init__(self, markov_chain: MarkovChain=None, identification: str=None):
        """
        Constructor MCSModifiedCesaroLimit
        :param: markov_chain: MarkovChainConventionalApproach
        :param: get_identification: str
        """
        MarkovChainSimulator.__init__(self, markov_chain, identification)
        self._type = "MCSModifiedCesaroLimit"

    def calculate_stationary_state_distribution(self, simulation_steps: int, alpha=1, specified_period: int=1):
        """
        Method for calculating the stationary state distribution
        :param simulation_steps: number of iteration steps
        :param alpha: value used for the alpha relaxation
        :param specified_period: specified value for period
        :return stationary state distribution
        """
        step = 0
        if (specified_period == 0) or (specified_period is None):
            period = self.calculate_mc_period()
        else:
            period = specified_period
        state_vector = self.get_markov_chain().get_initial_state_vector()[:]
        n = len(state_vector)
        x = []
        norm = []
        for i in range(period):
            x.append(np.zeros(n))
            norm.append(False)
        index = 0


        if simulation_steps == 0:
            while False in norm:
                step += 1
                x[index] = state_vector
                state_vector = self._transition(state_vector)
                state_vector /= sum(state_vector)
                index = (index + 1) % period
                curr_norm = self.norm(state_vector, x[index])
                norm[index] = curr_norm < self.get_calculation_precision()
                try:
                    self.notify_calculation_listeners(step, curr_norm)
                except:
                    raise InterruptedError
        else:
            step = 0
            for step in range(1, simulation_steps):
                self.notify_calculation_listeners(step)
                x[index] = state_vector
                state_vector = self._transition(state_vector)
                state_vector /= sum(state_vector)
                index = (index +1) % period
                norm = self.norm(state_vector, x[index])
            try:
                self.notify_calculation_listeners(step, norm)
            except:
                raise InterruptedError

        xs = np.zeros(n)
        for index in range(period):
            xs = xs + x[index] / period

        xs /= sum(xs)
        return xs

    def _transition(self, state_vector):
        """
        Method for calculating the successor state distribution
        :param cesaro_sum: current state distribution
        :return: successor state distribution
        """
        return np.dot(state_vector, self.get_markov_chain().get_transition_matrix())