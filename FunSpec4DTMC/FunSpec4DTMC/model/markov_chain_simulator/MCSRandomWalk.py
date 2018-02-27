
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

import matplotlib.pyplot as plt
import numpy as np
from FunSpec4DTMC.model.markov_chain_simulator.MarkovChainSimulator import MarkovChainSimulator
import FunSpec4DTMC.model.markov_chain.MarkovChain as MarkovChain


class MCSRandomWalk(MarkovChainSimulator):

    def __init__(self, markov_chain: MarkovChain.MarkovChain = None, start_state = 0, identification: str=None):
        """
        Constructor MCSMarkovChainSimulation
        :get_type markov_chain: MarkovChainConventionalApproach
        :get_type get_identification: str
        """
        MarkovChainSimulator.__init__(self, markov_chain, identification)
        self._type = "MCSRandomWalk"
        self._start_state = start_state
        self.randomWalk = None

    def get_index_from_start_state(self, start_state):
        if self._markov_chain is not None:

            state_designations = self.get_markov_chain().get_state_designations()
            if (state_designations is not None) and (str(start_state) in state_designations):
                start_state = self.get_markov_chain().get_state_designations().index(start_state)
            else:
                start_state = list(self.get_markov_chain().get_states()).index(float(start_state))
            return start_state
        else:
            return 0
    def calculate_stationary_state_distribution(self, simulation_steps: int, alpha=1, specified_period:int=1):
        """
        Method for calculating the stationary state distribution
        :param simulation_steps: number of iteration steps
        :param alpha: value used for the alpha relaxation
        :param specified_period: specified value for period
        :return stationary state distribution
        """
        current_state = self.get_index_from_start_state(self._start_state)
        state_distribution = np.array([0] * self._markov_chain.get_number_of_states(), dtype=float)
        state_distribution[current_state] = 1
        predecessor_state_distribution = np.zeros(len(state_distribution))

        if simulation_steps == 0:
            step = 1
            norm = self.norm(state_distribution / step,  predecessor_state_distribution / step)
            while norm > self.get_calculation_precision() or step < 10:
                step += 1
                try:
                    self.notify_calculation_listeners(step, norm)
                except:
                    raise InterruptedError
                predecessor_state_distribution = state_distribution.copy()
                current_state = self._transition(current_state)
                state_distribution[current_state] += 1
                norm = self.norm(state_distribution / step, predecessor_state_distribution / step)
            try:
                self.notify_calculation_listeners(step, norm)
            except:
                raise InterruptedError
        else:
            for step in range(simulation_steps):
                state_distribution[current_state] += 1
                current_state = self._transition(current_state)
            for state in range(len(state_distribution)):
                state_distribution[state] /= simulation_steps
            try:
                self.notify_calculation_listeners(step)
            except:
                raise InterruptedError
        return state_distribution




    def _simulate_random_walk(self, simulation_steps: int) -> list:
        """
        Returns list of simulated steps
        :param simulation_steps: iteration steps
        :return: list of simulated steps
        """

        resent_state = self.get_index_from_start_state(self._start_state)

        passed_states = [resent_state]
        for i in range(1, simulation_steps):
            resent_state = self._transition(resent_state)
            passed_states.append(resent_state)
            try:
                self.notify_calculation_listeners("", "")
            except:
                raise InterruptedError
        return passed_states


    def _transition(self, resent_state: int):
        """
        Calculates state distribution
        after a single transition step
            x_n = i
            x_{n+1} = min{k: sum_{j=0}^k pij >= U)
        :param resent_state: State
        :return: subsequent state: State
        """
        u = _get_random_number()
        transition_probabilities = self._markov_chain.get_transition_matrix()[resent_state, :].tolist()

        sum_of_first = 0
        subsequent_state = -1
        while sum_of_first < u:
            sum_of_first += transition_probabilities.pop(0)
            subsequent_state += 1
        return subsequent_state

#######################################################################################################################
#                                                                                                                     #
#                                           plot-methods                                                             #
#                                                                                                                     #
#######################################################################################################################

    def plot_random_walk(self, simulation_steps):
        """
        Method for generating a plot of a possible random walk
        :param simulation_steps: iteration steps
        :return: figure: plot of the random walk
        """
        simulation_steps = max(simulation_steps, 1)
        figure = plt.figure()
        ax = plt.subplot()
        try:
            x_values = range(simulation_steps)
            y_values = self._simulate_random_walk(simulation_steps)
        except:
            raise InterruptedError
        ax.plot(x_values, y_values, "x-")
        plt.xlabel("Steps")
        plt.ylabel('State')
        if self._markov_chain.get_state_designations() is not None:
            ax.set_yticks(range(len(self._markov_chain.get_state_designations())))
            ax.set_yticklabels(self._markov_chain.get_state_designations())
        else:
            ax.set_yticks(self._markov_chain.get_states())
        return figure

    def plot_evolution_of_state_probabilities(self, simulation_steps: int):
        """
        Method for generating a plot of of the state probabilities over time
        :param simulation_steps: iteration steps
        :return: figure: plot of the state probability evolution
        """
        simulation_steps = max(simulation_steps, 1)
        figure = plt.figure()
        try:
            passed_states = self._simulate_random_walk(simulation_steps)
            states = self._markov_chain.get_number_of_states()
        except:
            raise InterruptedError
        probability = [[] for states in range(0, states)]
        for step in range(1, simulation_steps + 1):
            resent_states = passed_states[0:step]

            for state in range(0, states):
                probability[state].append(resent_states.count(state) / step)
        x = range(1, simulation_steps + 1)

        ax = plt.subplot()
        for state in range(0, states):
            ax.plot(x, probability[state], "-", label='State {number}'.format(number=str(state)))

        plt.legend(loc='upper right')
        plt.xlabel("Steps")
        plt.ylabel('Probability')

        return figure

    def plot_evolution_of_state_average(self, simulation_steps: int):
        """
        Method for generating a plot of of the evolution of the average state over time
        :param simulation_steps: iteration steps
        :return: figure: plot of the evolution of the average state
        """
        simulation_steps = max(simulation_steps, 1)
        figure = plt.figure()
        average_state_distributions = []
        try:
            passed_states = self._simulate_random_walk(simulation_steps)
            for steps in range(1, simulation_steps + 1):
                self.notify_calculation_listeners(steps)
                average_state_distributions.append(np.mean(passed_states[0:steps]))
        except:
            raise InterruptedError
        x = range(1, simulation_steps + 1)
        plt.plot(x, passed_states, "x", label='State')
        plt.plot(x, average_state_distributions, ".-", label='Average state', color='red')
        plt.legend(loc='upper right', fontsize='x-large')
        plt.xlabel('Steps')
        plt.ylabel('States')
        if self._markov_chain.get_state_designations is not None:
            plt.yticks(range(len(self._markov_chain.get_states())), self._markov_chain.get_state_designations())
        return figure


def _get_random_number():
    """
    Calculates a U(0,1) random number
    :return: u: float
    """
    u = np.random.uniform()
    if u == 0:
        u = _get_random_number()
    return u
