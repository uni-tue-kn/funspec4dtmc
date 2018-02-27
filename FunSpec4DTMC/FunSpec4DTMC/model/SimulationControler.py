
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
from FunSpec4DTMC.model.markov_chain.MarkovChainForwardApproach import MarkovChainForwardApproach
from FunSpec4DTMC.model.markov_chain.MarkovChainConventionalApproach import MarkovChainConventionalApproach
from FunSpec4DTMC.model.markov_chain_simulator.MCSCesaroLimit import MCSCesaroLimit
from FunSpec4DTMC.model.markov_chain_simulator.MCSModifiedCesaroLimit import MCSModifiedCesaroLimit
from FunSpec4DTMC.model.markov_chain_simulator.MCSForwardApproach import MCSForwardApproach
from FunSpec4DTMC.model.markov_chain_simulator.MCSLimitingDistribution import MCSLimitingDistribution
from FunSpec4DTMC.model.markov_chain_simulator.MCSMatrixPowering import MCSMatrixPowering
from FunSpec4DTMC.model.markov_chain_simulator.MCSRandomWalk import MCSRandomWalk
from FunSpec4DTMC.model.markov_chain_simulator.MCSDirectApproach import MCSDirectApproach
from FunSpec4DTMC.model.markov_chain_simulator.MarkovChainSimulator import MarkovChainSimulator
from FunSpec4DTMC.model.Systems.Systems import GIGI1Qmax, System


class SimulationControler:
    def __init__(self):
        """
        Constructor
        """
        self.markov_chain = MarkovChainConventionalApproach(None, None)
        self.MCSimulator = MarkovChainSimulator(self.markov_chain)
        self.researchMode = True
        self.cythonMode = False
        self.precision = 10e-16
        self.discretization_precision = 10e-9
        self.markov_chains = []
        self.system_reset()
        self._calculation_listener = None
        self.number_of_mc = 0

    def set_queueing_system(self, system_configuration: dict):
        """
        Function for generating a queueing system based on the input specification
        :param system_configuration: input specification
        :return:
        """
        self.system = GIGI1Qmax(*system_configuration)
        self.system.set_discretization_precision(self.discretization_precision)
        self.system.enableResearchMode(self.researchMode)
        return self.system

    def enableResearchMode(self, enabled: bool):
        """
        Method that enables activation of the research modes
        :param research_mode: Selected if research module enables
        """
        self.researchMode = enabled

    def enableCythonMode(self, enabled: bool):
        """
        Method that enables activation of the cython modes
        Method that enables activation of the cython modes
        :param  cython_mode: Selected if Cython module enables
        """
        self.cythonMode = enabled

    def adjust_precision(self, precision: float):
        """
        Method for adjusting the accuracy of calculation of the simulator
        :param precision: Chosen accuracy
        """
        self.precision = precision
        self.MCSimulator.set_calculation_precision(precision)

    def adjust_discretization_precision(self, precision: float):
        """
        Method for adjusting the accuracy of discretization
        :param precision: Chosen accuracy
        """
        self.discretization_precision = precision
        if self.system:
            self.system.set_discretization_precision(precision)


    def set_calculation_listener(self, listener: object):
        """
        Function that allows to set the calculation listener.
        :param listener: Object that observes the calculation
        """
        self._calculation_listener = listener

    def add_conventional_markov_chain(self, initial_state_vector: np.ndarray, transition_matrix: np.ndarray, state_designations: list):
        """
        Function for creating and adding a conventionally specified Markov chain
        :param initial_state_vector: vector describing the start configuration
        :param transition_matrix: matrix defining the Markov chain
        :param state_designations: Optional state designations
        """
        self.markov_chains.append(MarkovChainConventionalApproach(initial_state_vector, transition_matrix,
                                                                  state_designations))
        self.number_of_mc += 1

    def add_forward_markov_chain(self, states: np.ndarray, state_space_names: list, initial_state_vector: np.ndarray,
                                 factors: np.ndarray, factor_space_names: list, factor_distribution: np.ndarray, transition_function: np.ndarray):
        """
        Function for creating and adding a functional specified Markov chain
        :param states: vector describing the state space
        :param state_space_names: optional naming of the state spaces
        :param initial_state_vector: vector describing the start configuration
        :param factors: factors affecting the system behaviour
        :param factor_space_names: optional naming of the factor spaces
        :param factor_distribution: distribution of the factors
        :param transition_function: function describing the system behaviour
        """
        self.markov_chains.append(MarkovChainForwardApproach(initial_state_vector, state_space_names, factors,
                                                             factor_space_names,factor_distribution,
                                                             transition_function, states))
        self.number_of_mc += 1

    def get_number_of_mc(self):
        """
        Returns the number of created Markov chains
        """
        return self.number_of_mc

    def get_markov_chains(self):
        """
        Returns the Markov chains created in the current project
        """
        return self.markov_chains

    def reset_markov_chains(self):
        """
        Allows to reset the stationary state distribution of the Markov chain
        """
        markov_chains = self.get_markov_chains()
        for mc in markov_chains:
            mc.set_stationary_state_distribution(None)

    def instantiate_MCSMatrixPowering(self):
        """
        Function for instantiating the simulator MCSMatrixPowering
        """
        self.reset_markov_chains()
        self.MCSimulator = MCSMatrixPowering()
        self.MCSimulator.set_calculation_precision(self.precision)
        self.MCSimulator.add_calculation_listener(self._calculation_listener)

    def instantiate_MCSRandomWalk(self, start_state: int):
        """
        Function for instantiating the simulator MCSRandomWalk
        """
        self.reset_markov_chains()
        self.MCSimulator = MCSRandomWalk(start_state=start_state)
        self.MCSimulator.set_calculation_precision(self.precision)
        self.MCSimulator.add_calculation_listener(self._calculation_listener)

    def instantiate_MCSCesaroLimit(self):
        """
        Function for instantiating the simulator MCSCesaroLimit
        """
        self.reset_markov_chains()
        self.MCSimulator = MCSCesaroLimit()
        self.MCSimulator.set_calculation_precision(self.precision)
        self.MCSimulator.add_calculation_listener(self._calculation_listener)

    def instantiate_MCSModifiedCesaroLimit(self):
        """
        Function for instantiating the simulator MCSModifiedCesaroLimit
        """
        self.reset_markov_chains()
        self.MCSimulator = MCSModifiedCesaroLimit()
        self.MCSimulator.set_calculation_precision(self.precision)
        self.MCSimulator.add_calculation_listener(self._calculation_listener)

    def instantiate_MCSLimitingDistribution(self):
        """
        Function for instantiating the simulator MCSLimitingDistribution
        """
        self.reset_markov_chains()
        self.MCSimulator = MCSLimitingDistribution()
        self.MCSimulator.set_calculation_precision(self.precision)
        self.MCSimulator.add_calculation_listener(self._calculation_listener)

    def instantiate_MCSDirectApproach(self, scheme:str="Gaussian scheme"):
        """
        Function for instantiating the simulator MCSDirectApproach
        """
        self.reset_markov_chains()
        self.MCSimulator = MCSDirectApproach(self.researchMode, scheme)
        self.MCSimulator.set_calculation_precision(self.precision)
        self.MCSimulator.add_calculation_listener(self._calculation_listener)

    def instantiate_MCSForwardApproach(self):
        """
        Function for instantiating the simulator MCSForwardApproach
        """
        self.reset_markov_chains()
        self.MCSimulator = MCSForwardApproach(cythonMode=self.cythonMode)
        self.MCSimulator.set_calculation_precision(self.precision)
        self.MCSimulator.add_calculation_listener(self._calculation_listener)

    def get_system(self):
        """
        Function to get the current system
        :return current system
        """
        self.system.enableResearchMode(self.researchMode)
        self.system.set_discretization_precision(self.discretization_precision)
        return self.system

    def system_reset(self):
        """
        Functionality to reset the current system
        """
        self.system = None


    def set_system(self):
        """
        Functionality to set the current system
        """
        self.system = System()
        self.system.set_discretization_precision(self.discretization_precision)
        self.system.enableResearchMode(self.researchMode)

    def calculate_period(self):
        """
        Method to calculate the period of the Markov chains of the current project
        :return: results, titles
        """
        results = []
        titles = []
        index = 1
        for mc in self.markov_chains:
            self.MCSimulator.set_markov_chain(mc)
            results.append(self.MCSimulator.calculate_mc_period())
            titles.append("Markov chain {number}".format(number=index))
            index += 1
        return results, titles

    def get_graph_plot(self, graph_layout: str, mark_closures: bool):
        """
        Method to create graph plots of the Markov chains of the current project
        :return: results, titles
        """
        results = []
        titles = []
        index = 1
        for mc in self.markov_chains:
            self.MCSimulator.set_markov_chain(mc)
            results.append(self.MCSimulator.get_graph_plot(graph_layout, mark_closures))
            titles.append("Markov chain {number}".format(number=index))
            index += 1
        return results, titles

    def calculate_stationary_state_distributions(self, steps:int, alpha: float, specified_period: int):
        """
        Method to calculate the stationary state distribution of the Markov chains of the current project
        :param steps: iteration steps for calculation of the stationary state vector
        :param  alpha: value used for alpha-relaxation
        :param specified_period: specified value for period
        :return: results, titles
        """
        results = []
        titles = []
        index = 1
        for mc in self.markov_chains:
            self.MCSimulator.set_markov_chain(mc)
            try:
                results.append(self.MCSimulator.calculate_stationary_state_distribution(steps, alpha, specified_period))
            except:
                raise InterruptedError
            titles.append("Markov chain {number}".format(number=index))
            index += 1
        return results, titles


    def plot_stationary_state_distributions(self, steps: int, alpha: float, specified_period: int, separated:bool=True):
        """
        Method to plot the stationary state distribution of the Markov chains of the current project
        :param steps: iteration steps for calculation of the stationary state vector
        :param  alpha: value used for alpha-relaxation
        :param specified_period: specified value for period
        :return: results, titles
        """
        if separated or len(self.markov_chains) == 1:
            results = []
            titles = []
            index = 1
            for mc in self.markov_chains:
                try:
                    self.MCSimulator.set_markov_chain(mc)
                except:
                    raise InterruptedError
                results.append(self.MCSimulator.plot_stationary_state_distribution(steps, alpha, specified_period))
                titles.append("Markov chain {number}".format(number=index))
                index += 1
        else:
            figure = plt.figure()
            index = 1
            for mc in self.markov_chains:
                self.MCSimulator.set_markov_chain(mc)
                try:
                    label = "Markov chain {number}".format(number=index)
                    figure = self.MCSimulator.plot_stationary_state_distribution(steps, alpha, specified_period,
                                                                                 figure=figure, label=label)
                except:
                    raise InterruptedError
                index += 1
            results = [figure]
            titles = ["all Markov chains"]
        return results, titles

    def plot_cumulative_stationary_state_distributions(self, steps: int, alpha: float, specified_period: int, separated:bool=True):
        """
        Method to plot the cumulative stationary state distribution of the Markov chains of the current project
        :param steps: iteration steps for calculation of the stationary state vector
        :param  alpha: value used for alpha-relaxation
        :param specified_period: specified value for period
        :return: results, titles
        """
        if separated or len(self.markov_chains) == 1:
            results = []
            titles = []
            index = 1
            for mc in self.markov_chains:
                self.MCSimulator.set_markov_chain(mc)
                try:
                    results.append(self.MCSimulator.plot_cumulative_stationary_state_distribution(steps, alpha, specified_period))
                except:
                    raise InterruptedError
                titles.append("Markov chain {number}".format(number=index))
                index += 1

        else:
            figure = plt.figure()
            index = 1
            for mc in self.markov_chains:
                self.MCSimulator.set_markov_chain(mc)
                try:
                    figure = self.MCSimulator.\
                        plot_cumulative_stationary_state_distribution(steps, alpha, specified_period, figure=figure,
                                                                      label="Markov chain {number}".format(number=index))
                except:
                    raise InterruptedError
                index += 1
            results = [figure]
            titles = ["all Markov chains"]
        return results, titles


    def plot_complementary_cumulative_stationary_state_distributions(self, steps: int, alpha: float, specified_period: int, separated: bool=True):
        """
        Method to plot the complementary cumulative stationary state distribution of the Markov chains of the current project
        :param steps: iteration steps for calculation of the stationary state vector
        :param  alpha: value used for alpha-relaxation
        :param specified_period: specified value for period
        :return: results, titles
        """
        if separated or len(self.markov_chains) == 1:
            results = []
            titles = []
            index = 1
            for mc in self.markov_chains:
                self.MCSimulator.set_markov_chain(mc)
                try:
                    results.append(self.MCSimulator.
                                   plot_complementary_cumulative_stationary_state_distribution(steps,
                                                                                               alpha,
                                                                                               specified_period))
                except:
                    raise InterruptedError
                titles.append("Markov chain {number}".format(number=index))
                index += 1
        else:
            figure = plt.figure()
            for mc in self.markov_chains:
                self.MCSimulator.set_markov_chain(mc)
                index=1
                try:
                    figure = self.MCSimulator.plot_complementary_cumulative_stationary_state_distribution(steps,
                                                                                                          alpha,
                                                                                                          specified_period,
                                                                                                          figure=figure,                                                                          label="Markov chain {number}".format(number=index)
                                                                                                          )
                except:
                    raise InterruptedError
                index += 1
            results = [figure]
            titles = ["all Markov chains"]
        return results, titles

    def plot_random_walk(self, steps: int):
        """
        Method to plot a random Walk on the  Markov chains of the current project
        :param steps: number of iteration steps
        :return: results, titles
        """
        results = []
        titles = []
        index = 1
        for mc in self.markov_chains:
            self.MCSimulator.set_markov_chain(mc)
            try:
                results.append(self.MCSimulator.plot_random_walk(steps))
            except:
                raise InterruptedError
            titles.append("Markov chain {number}".format(number=index))
            index += 1
        return results, titles

    def plot_evolution_of_state_average(self, steps: int):
        """
        Method to plot the evolution of the state average on the  Markov chains of the current project
        :param steps: number of iteration steps
        :return: results, titles
        """
        results = []
        titles = []
        index = 1
        for mc in self.markov_chains:
            self.MCSimulator.set_markov_chain(mc)
            try:
                results.append(self.MCSimulator.plot_evolution_of_state_average(steps))
            except:
                raise InterruptedError
            titles.append("Markov chain {number}".format(number=index))
            index += 1
        return results, titles

    def plot_evolution_of_state_probabilities(self, steps: int):
        """
        Method to plot the evolution of the state probabilities on the  Markov chains of the current project
        :param steps: number of iteration steps
        :return: results, titles
        """
        results = []
        titles = []
        index = 1
        for mc in self.markov_chains:
            self.MCSimulator.set_markov_chain(mc)
            try:
                results.append(self.MCSimulator.plot_evolution_of_state_probabilities(steps))
            except:
                raise InterruptedError
            titles.append("Markov chain {number}".format(number=index))
            index += 1
        return results, titles

    def get_mc(self):
        """
        Method to get the current Markov chain
        :return: current Markov chain
        """
        return self.markov_chain

    def get_factor_plot(self):
        """
        Method to get a plot of the factor distribution of the current system
        :return: current factors
        """
        return self.system.plot_factor_distribution()

    def get_transition_matrix(self):
        """
        Method to return the transition matrix of the current Markov chain
        :return: transition matrix
        """
        titles = []
        results = []
        index = 1
        for mc in self.markov_chains:
            self.MCSimulator.set_markov_chain(mc)
            results.append(self.MCSimulator.calculate_transition_matrix())
            titles.append("Markov chain {number}".format(number=index))
            index += 1
        return results, titles
