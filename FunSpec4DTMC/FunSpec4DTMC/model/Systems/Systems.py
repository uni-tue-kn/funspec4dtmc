
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
from FunSpec4DTMC.model.Systems.distributions.DiscretizedExponentialDistribution import \
    DiscretizedExponentialDistribution
from FunSpec4DTMC.model.Systems.distributions.DiscretizedGammaDistribution import \
    DiscretizedGammaDistribution
from FunSpec4DTMC.model.Systems.distributions.DiscretizedKErlangDistribution \
    import DiscretizedKErlangDistribution
from FunSpec4DTMC.model.Systems.distributions.DiscretizedUniformDistribution import \
    DiscretizedUniformDistribution
from FunSpec4DTMC.model.Systems.distributions.UserDefinedDistribution import UserDefinedDistribution
from FunSpec4DTMC.model.Systems.distributions.DiscretizedHyperexponentialDistribution import DiscretizedHyperexponentialDistribution

class System:


    def __init__(self):
        """
        Constructor of the system interface
        """
        self._type = "System"
        self._research_mode = False
        self._discretization_precision = 10e-9

    def set_discretization_precision(self, precision: float):
        self._discretization_precision = precision


    def enableResearchMode(self, enabled: bool):
        """
        Method for setting up the usage mode.
        :param enabled: Activation of research Mode
        """
        self._research_mode = enabled



    def calculate_mc_specification(self, separated_factors: bool):
        """
        Interface function for Markov chain specification determination
        :param separated_factors:
        """
        raise NotImplementedError

    def get_states(self, separated_factors: bool):
        """
        Calculation method of the states of the Markov chain
        """
        raise NotImplementedError


    def get_initial_state_vector(self):
        """
        Calculation method the initial state vector of the Markov chain
        """
        raise NotImplementedError

    def get_state_designations(self):
        """
        Determination method of he state designations of the Markov chain
        """
        raise NotImplementedError

    def calculate_factor_distribution(self):
        """
        Calculation method of the factors of the Markov chain
        """
        raise NotImplementedError

    def plot_factor_distribution(self):
        """
        Calculation method of the factor probabilities of the Markov chain
        """
        raise NotImplementedError


class GIGI1Qmax(System):

    def __init__(self,
                 arrival_time_distribution: list,
                 batch_size_distribution: list,
                 service_time: float,
                 q_max: int,
                 transition_functions: str):
        """
        Constructor of the GI^GI/D/1-Qmax system
        :param arrival_time_distribution: Specification of the arrival time distribution
        :param batch_size_distribution: Specification of the batch size distribution
        :param service_time: Service time of the system
        :param q_max: Maximum Queue size
        :param transition_functions: Transition function that specifies the system behavior.
        """
        System.__init__(self)
        self._service_time = service_time
        self._arrival_time_distribution = self.get_distribution(arrival_time_distribution)
        self._batch_size_distribution = self.get_distribution(batch_size_distribution)
        self._q_max = q_max
        self._transition_functions = transition_functions
        self._type = "GI/GI/1-Qmax-System"
        self._factors = []
        self._factor_distribution = []

    def enableResearchMode(self, enabled: bool):
        """
        Method for setting up the usage mode.
        :param enabled: Activation of research Mode
        """
        self._research_mode = enabled
        self._arrival_time_distribution.enable_research_mode(self._research_mode)
        self._batch_size_distribution.enable_research_mode(self._research_mode)

    def calculate_mc_specification(self, service_time_adjustment: bool=False, separated_factors: bool=True):
        """
        Method for Markov chain specification from the GI^GI/D/^-Qmax-system
        :param service_time_adjustment: Adjustment of the service time to calculation precision
        :param separated_factors: Separation of the factor space
        :return MC specification
        """
        factors, factor_probabilities = self.calculate_factor_distribution(service_time_adjustment,
                                                                           separated_factors)
        return (self.get_states(separated_factors),
               self.get_state_designations(),
               self.get_initial_state_vector(),
               factors,
               factor_probabilities,
               self._transition_functions)

    def get_states(self, separated_factors: bool):
        """
        Calculation method of the states of the Markov chain
        :param separated_factors: Separation of the factor space
        :return: states
        """
        states = np.array([round(n * self._service_time, 13) for n in range(self._q_max+2)], dtype=float)
        if separated_factors:
            return [states, states]
        else:
            return [states]

    def get_state_designations(self):
        """
        Determination method of the state designations of the Markov chain
        :param: state designations of the system
        """
        return ["x{state}".format(state=state) for state in range(self._q_max+2)]

    def get_initial_state_vector(self, initial_state: int=0):
        """
        Calculation method the initial state vector of the Markov chain
        :param initial_state: system state at initialisation time
        :return: initial state vector
        """
        initial_state_vector = np.zeros(self._q_max+2)
        initial_state_vector[initial_state] = 1.0
        return initial_state_vector

    def calculate_factor_distribution(self, service_time_adjustment: bool = False, separated_values: bool = True):
        """
        Calculation of the factor distribution based on the system specification
        :param service_time_adjustment: Adjustment of the service time to calculation precision
        :param separated_values: separated_factors: Separation of the factor space
        :return: factor distribution of the MC specification
        """
        if not (self._factors and self._factor_distribution):
            self._factors, self._factor_distribution = [], []
            arrival_times, arrival_time_distribution, batch_sizes, batch_size_distribution = \
                self.get_distributions(service_time_adjustment)
            if separated_values:
                self._factors = [batch_sizes, arrival_times]
                arrival_time_distribution /= np.sum(arrival_time_distribution)
                batch_size_distribution /= np.sum(batch_size_distribution)
                self._factor_distribution = [batch_size_distribution, arrival_time_distribution]
            else:
                for arrival_time in range(len(arrival_times)):

                    for service_time in range(len(batch_sizes)):
                        self._factors.append((arrival_times[arrival_time], batch_sizes[service_time]))
                        self._factor_distribution.append((arrival_time_distribution[arrival_time] *
                                                          batch_size_distribution[service_time]))
                self._factor_distribution /= np.sum(self._factor_distribution)
        return [self._factors], [self._factor_distribution]

    def plot_factor_distribution(self):
        """
        Creating the plot of the factor distribution
        :return: factor distribution plot
        """
        figure = plt.figure()
        number_factors = len(self._factors)
        x_values = range(number_factors)
        if number_factors <= 25:
            ax1 = figure.add_subplot(111)
            ax1.bar(x_values, self._factor_distribution)
            plt.xticks(x_values, self._factors)
            plt.ylabel('Probability')
            plt.xlabel('Factors')
            plt.title('Factor Distribution')

        else:
            ax1 = figure.add_subplot(111)
            x_values_arrival, probabilities_arrival = self._arrival_time_distribution.get_distribution()
            x_values_batch, probabilities_batch = self._batch_size_distribution.get_distribution()
            ax1.step(x_values_arrival, np.cumsum(probabilities_arrival))
            ax1.step(x_values_batch, np.cumsum(probabilities_batch))

        return figure

    def get_distribution(self, distribution: dict):
        """
        Determination of the distribution from input spezification
        :param distribution: Input configuration of the arivial time or service time distribution
        :return: discrete distribution of the service time or arrival time
        """
        maximum = distribution["maximum"]
        if distribution["name"] in ["Exponential", "Exponential distribution"]:
            rate = distribution["rate"]
            discretizedDistribution = DiscretizedExponentialDistribution(self._service_time, maximum, rate)

        elif distribution["name"] in ["K-Erlang", "K-Erlang distribution"]:
            rate = distribution["rate"]
            k = distribution["k"]
            discretizedDistribution = DiscretizedKErlangDistribution(self._service_time, maximum, rate, k)

        elif distribution["name"] in ["Gamma", "Gamma distribution"]:
            alpha = distribution["alpha"]
            beta = distribution["beta"]
            discretizedDistribution = DiscretizedGammaDistribution(self._service_time, maximum, alpha, beta)

        elif distribution["name"] in ["Hyperexponential", "Hyperexponential distribution"]:

            pi = distribution["pi"]
            li = distribution["li"]
            discretizedDistribution = DiscretizedHyperexponentialDistribution(self._service_time, maximum, li, pi)

        elif distribution["name"] in ["Uniform", "Uniform distribution"]:
            minimum = distribution["minimum"]
            discretizedDistribution = DiscretizedUniformDistribution(self._service_time, minimum, maximum)

        elif distribution["name"] in ["General independent distribution"]:
            inputValues = distribution["input values"]
            probabilities = distribution["probabilities"]
            discretizedDistribution = UserDefinedDistribution(inputValues, probabilities)

        else:
            raise NotImplementedError

        discretizedDistribution.enable_research_mode(self._research_mode)
        return discretizedDistribution

    def set_service_time(self, service_time: float):
        """
        Prcedure to adapt the service time.
        :param service_time:  service time of the queueing system
        """
        if service_time is not None:
            self._service_time = service_time
            self.get_arrival_time_distribution().set_interval_size(service_time)
            self.get_batch_size_distribution().set_interval_size(service_time)

    def get_arrival_time_distribution(self):
        """
        Getter method of the arrivial time distribution
        :return: arrivial time distribution
        """
        self._arrival_time_distribution.set_epsilon(self._discretization_precision)
        return self._arrival_time_distribution

    def get_batch_size_distribution(self):
        """
        Getter method of the batch size distribution
        :return: batch size distribution
        """
        self._batch_size_distribution.set_epsilon(self._discretization_precision)
        return self._batch_size_distribution

    def get_distributions(self, service_time_adjustment):
        """
        Getter method of the arrival time and batch size distribution
        :return: arrival time and batch size distribution
        """
        arrival_times, arrival_time_distribution, interval_size_arrival = self.get_arrival_time_distribution().get_distribution(
            service_time_adjustment)
        if interval_size_arrival is not None:
            self.set_service_time(interval_size_arrival)
        batch_sizes, batch_size_distribution, interval_size_batch = self.get_batch_size_distribution().get_distribution(
            service_time_adjustment)
        if interval_size_batch is not None:
            self.set_service_time(interval_size_batch)
        if interval_size_arrival is not None and interval_size_batch is not None and interval_size_arrival > interval_size_arrival :
            arrival_times, arrival_time_distribution, service_time_arrival = self.get_arrival_time_distribution().get_distribution(
                service_time_adjustment=False)
        return arrival_times, arrival_time_distribution, batch_sizes, batch_size_distribution

    def get_arrival_time_distribution_function_plot(self, service_time_adjustment):
        """
        Method for creating the arrival time distribution plot
        :return: arrival time distribution plot
        """
        plot, service_time = self.get_arrival_time_distribution().get_distribution_function_plot(
            service_time_adjustment)
        if service_time is not None:
            self.set_service_time(service_time)
        return plot, service_time

    def get_batch_size_distribution_function_plot(self, service_time_adjustment):
        """
        Method for creating the batch size distribution plot
        :return: batch size distribution plot
        """
        plot, service_time = self.get_batch_size_distribution().get_distribution_function_plot(service_time_adjustment)
        if service_time is not None:
            self.set_service_time(service_time)
        return plot, service_time

    def get_distribution_function_plots(self, service_time_adjustment):
        """
        Method for creating the arrival time and batch size distribution plot
        :return: arrival time and batch size distribution plot
        """
        arrival_time_distribution_function_plot, service_time_arrival = \
            self.get_arrival_time_distribution_function_plot(service_time_adjustment)
        batch_size_distribution_function_plot, service_time_batch = \
            self.get_batch_size_distribution_function_plot(service_time_adjustment)
        if service_time_arrival is not None and service_time_batch is not None and service_time_arrival > service_time_batch:            arrival_time_distribution_function_plot, service_time_arrival = \
                self.get_arrival_time_distribution_function_plot(service_time_adjustment=False)
        return arrival_time_distribution_function_plot, batch_size_distribution_function_plot
