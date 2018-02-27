
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
import time
import importlib
from FunSpec4DTMC.model.markov_chain_simulator.MarkovChainSimulator import MarkovChainSimulator
from FunSpec4DTMC.model.markov_chain import MarkovChainForwardApproach
import FunSpec4DTMC.model.markov_chain_simulator.forward_algorithm_cython_implementation.ForwardAlgorithm as FA


class MCSForwardApproach(MarkovChainSimulator):


    def __init__(self, markov_chain: MarkovChainForwardApproach = None, cythonMode=False, identification: str = None):
        """
        Constructor of the MCSForwardApproach
        :param markov_chain: MarkovChainForwardApproach
        :param cythonMode: cythonMode selection
        :param identification: designation of the simulator
        """
        MarkovChainSimulator.__init__(self, markov_chain, identification)
        self._type = "MCSForwardApproach"
        self.cythonMode = cythonMode

    def create_transition_function_from_file_path(self, file_path):
        TransitionFunction = importlib.import_module(file_path)
        transition_functions = []
        index = 1
        while hasattr(TransitionFunction
                , 'transition_function{index}'.format(index=index)):
            transition_functions.append(
                getattr(TransitionFunction, 'transition_function{index}'.format(index=index)))
            index += 1
        return transition_functions



    def calculate_stationary_state_distribution(self, simulation_steps: int, alpha=1, specified_period:int=1):
        """
        Method for calculating the stationary state distribution
        :param simulation_steps: number of iteration steps
        :param alpha: value used for the alpha relaxation
        :param specified_period: specified value for period
        :return stationary state distribution
        """
        state_vector = np.array(self.get_markov_chain().get_initial_state_vector()[:])
        number_of_states = len(state_vector)
        if (specified_period == 0) or (specified_period is None):
            period = self.calculate_mc_period()
        else:
            period = specified_period
        step = 0
        x = []
        norm = []
        for i in range(period):
            x.append(np.zeros(number_of_states))
            norm.append(False)

        index = 0
        t= time.clock()
        if simulation_steps == 0:
            while False in norm:
                step += 1
                x[index] = state_vector
                if not self.cythonMode:
                    state_vector = self._forward_algorithm(state_vector)
                else:
                    state_vector = FA.forward_algorithm(
                                        self.get_markov_chain().get_states(),
                                        state_vector,
                                        self.get_markov_chain().get_factors(),
                                        self.get_markov_chain().get_factor_distributions(),
                                        self.get_markov_chain().get_transition_functions())

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
                if not self.cythonMode:
                    state_vector = self._forward_algorithm(state_vector)
                else:

                    state_vector = FA.forward_algorithm(
                                        self.get_markov_chain().get_states(),
                                        state_vector,
                                        self.get_markov_chain().get_factors(),
                                        self.get_markov_chain().get_factor_distributions(),
                                        self.get_markov_chain().get_transition_functions())
                state_vector /= sum(state_vector)
                index = (index + 1) % period
                norm = self.norm(state_vector, x[index])
            try:
                self.notify_calculation_listeners(step, norm)
            except:
                raise InterruptedError
        xs = np.zeros(number_of_states)
        for index in range(int(period)):
            xs = xs + x[index] / period
        xs /= sum(xs)
        print("Zeit:" + str(time.clock()-t))
        return xs


    def _forward_algorithm(self, state_distribution: np.array):
        """
        Calculates the subsequent state distribution by applying the forward algorithm.
        :param state_distribution: current state distribution
        :return: subsequent state distribution
        """
        old = state_distribution[:]
        states = self.get_markov_chain().get_states()
        number_of_states = len(state_distribution)
        factors = self.get_markov_chain().get_factors()
        factor_distributions = self.get_markov_chain().get_factor_distributions()
        transition_functions = self.create_transition_function_from_file_path(
                                            self.get_markov_chain().get_transition_functions())
        new = np.zeros(number_of_states)
        for index in range(len(transition_functions)):
            new = np.zeros(number_of_states)
            curr_states = (states[index])
            map = {}

            for state_index in range(len(curr_states)):
                try:
                    map[str(float(curr_states[state_index]))] = int(state_index)
                except:
                    map[str(self.adjust_input_type(curr_states[state_index]))] = int(state_index)

            for j in range(number_of_states):
                if old[j] != 0.0:
                    curr_factors = factors[index]
                    curr_factor_distribution = factor_distributions[index]
                    l = len(curr_factors)

                    for k in range(l):
                        new[map[str(self.adjust_input_type(transition_functions[index](curr_states[j], curr_factors[k])))]] += \
                            old[j] * curr_factor_distribution[k]
            old = new

        return new



    def enableCythonMode(self, enabled):
        """
        Method to enable the cython mode
        :param enabled: cython mode selection
        """
        self.cythonMode = enabled

    def calculate_transition_matrix(self):
        """
        Calculates the transition matrix by applying the forwarding algorithm.
        :return: transition matrix
        """
        if not self.cythonMode:
            states = self.get_markov_chain().get_states()
            number_of_states = len(states[0])
            factors = self.get_markov_chain().get_factors()
            factor_distributions = self.get_markov_chain().get_factor_distributions()
            transition_functions = self.create_transition_function_from_file_path(
                                            self.get_markov_chain().get_transition_functions())
            transition_matrix = np.eye(number_of_states)
            for index in range(len(transition_functions)):
                new_transition_matrix = np.zeros((number_of_states, number_of_states))
                curr_states = states[index]
                map = {}
                for state_index in range(len(curr_states)):
                    try:
                        map[str(float(curr_states[state_index]))] = int(state_index)
                        map[str(int(curr_states[state_index]))] = int(state_index)
                    except:
                        map[str(tuple(curr_states[state_index]))] = int(state_index)
                for j in range(len(curr_states)):
                    curr_factors = factors[index]
                    curr_factor_distribution = factor_distributions[index]
                    l = len(curr_factors)
                    for k in range(l):

                        new_transition_matrix[map[str(self.adjust_input_type(curr_states[j]))],
                                              map[str(self.adjust_input_type(transition_functions[index](curr_states[j], curr_factors[k])))]] \
                            += curr_factor_distribution[k]
                transition_matrix = np.dot(transition_matrix, new_transition_matrix)

        elif self.cythonMode:

            transition_matrix = FA.transition_matrix(
                                        self.get_markov_chain().get_states(),
                                        self.get_markov_chain().get_factors(),
                                        self.get_markov_chain().get_factor_distributions(),
                                        self.create_transition_function_from_file_path(
                                            self.get_markov_chain().get_transition_functions())
                                        )
        return transition_matrix

    def adjust_input_type(self, input):
        if type(input) in [list, tuple, np.ndarray]:
            return tuple([round(float(value), 13) for value  in input])
        else:
            return round(float(input), 13)
