
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


class MCSCesaroLimit(MarkovChainSimulator):

    def __init__(self, markov_chain: MarkovChain=None, identification: str=None):
        """
        Constructor MCSCesaroLimit
        :param: markov_chain: MarkovChainConventionalApproach
        :param: get_identification: str
        """
        MarkovChainSimulator.__init__(self, markov_chain, identification)
        self._type = "MCSCesaroLimit"


    def calculate_stationary_state_distribution(self, simulation_steps: int, alpha=1, specified_period:int=1):
        """
        Method for calculating the stationary state distribution
        :param simulation_steps: number of iteration steps
        :param alpha: value used for the alpha relaxation
        :param specified_period: specified value for period
        :return stationary state distribution
        """
        cesaro_sum = self.get_markov_chain().get_initial_state_vector()[:]
        predecessor_cesaro_sum = np.zeros(len(cesaro_sum))

        if simulation_steps == 0:
            step = 0
            norm = self.norm(cesaro_sum, predecessor_cesaro_sum)
            while norm > self.get_calculation_precision():
                step += 1
                try:
                    self.notify_calculation_listeners(step, norm)
                except:
                    raise InterruptedError
                predecessor_cesaro_sum = cesaro_sum
                cesaro_sum = (step * cesaro_sum + self._transition(cesaro_sum))/(step+1)
                cesaro_sum = alpha * cesaro_sum + (1 - alpha) * predecessor_cesaro_sum
                cesaro_sum /= sum(cesaro_sum)
                norm = self.norm(cesaro_sum, predecessor_cesaro_sum)
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
                predecessor_cesaro_sum = cesaro_sum
                cesaro_sum = (step * cesaro_sum + self._transition(cesaro_sum)) / (step + 1)
                cesaro_sum = alpha * cesaro_sum + (1 - alpha) * predecessor_cesaro_sum
                cesaro_sum /= sum(cesaro_sum)
            norm = self.norm(cesaro_sum, predecessor_cesaro_sum)
            try:
                self.notify_calculation_listeners(step, norm)
            except:
                raise InterruptedError
        return cesaro_sum

    def _transition(self, cesaro_sum: np.ndarray):
        """
        Method for calculating the successor state distribution
        :param cesaro_sum: current state distribution
        :return: successor state distribution
        """
        return np.dot(cesaro_sum, self.get_markov_chain().get_transition_matrix())


