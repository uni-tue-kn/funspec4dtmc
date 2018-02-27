
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
from FunSpec4DTMC.model.Systems.distributions.DiscretizedDistribution \
    import DiscretizedDistribution


class UserDefinedDistribution(DiscretizedDistribution):

    def __init__(self, values: np.ndarray, probabilities: np.ndarray):
        """
        Constructor General independent distribution
        :param: values: values of the general independent distribution
        :param: probabilities: probabilities of the general independent distribution
        """
        self._values = values
        self._probabilities = probabilities
        self._type = "General independent distribution"

    def get_distribution(self, service_time_adjustment: bool=None):
        """
        Calculation of general independent distribution as vector
        :param service_time_adjustment: adjustment of the selected service time to calculation precision
        :return: general independent distribution as vector
        """
        return self._values, self._probabilities, None

    def get_distribution_function(self, service_time_adjustment: bool = None):
        """
        Calculation of general independent distribution function as vector
        :param service_time_adjustment: adjustment of the selected service time to calculation precision
        :return: general independent distribution function as vector
        """
        return self._values, np.cumsum(self._probabilities)

    def plot_distribution(self):
        """
        Plots discretized general independent distribution
        """
        plt.step(self._values, self._probabilities, where="post")
        plt.ylim([0, 1])
        plt.ylabel('Probability')
        plt.xlabel('States')
        plt.title('Distribution')
        plt.show()
        return [*zip(*[self._values, self._probabilities])]

    def plot_distribution_function(self):
        """
        Plots discretized cumulative general independent distribution function
        """
        self._values.insert(0, 0)
        self._probabilities.insert(0, 0)
        self._values.append(self._values[-1]+1)
        self._probabilities.append(self._probabilities[-1])

        plt.step(self._values, np.cumsum(self._probabilities), where="post")
        plt.xlim([1, self._values[-1]+1])
        plt.ylim([0, 1])
        plt.ylabel('Probability')
        plt.xlabel('States')
        plt.title('Discretized Distribution Function')
        plt.show()
        return [*zip(*[self._values, self._probabilities])]

    def get_distribution_plot(self):
        """
        Plotting the general independent distribution
        :return: general independent distribution plot
        """
        figure = plt.figure()
        factors, probabilities = self.get_distribution()[0:1]
        factors = np.insert(factors, 0, 0)
        probabilities = np.insert(probabilities, 0, 0)
        factors = np.append(factors, factors[-1] + 1)
        probabilities = np.append(probabilities, 0)

        ax = figure.add_subplot(111)
        ax.step(factors, probabilities, where="post")

        ax.text(0.85, 0.02, " mean =  {mean}\n  SDev =  {sdev} ".format(mean=round(self.get_discretized_mean(), 3),

                                                                        sdev=round(
                                                                            self.get_discretized_standard_deviation(),
                                                                            3)),
                horizontalalignment='left',
                verticalalignment='bottom',
                transform=ax.transAxes)
        plt.ylabel('Probability')
        plt.xlabel('Factor size (as multiple of the service time)')
        plt.title('{distribution}'.format(distribution=self.get_type()))

        return figure

    def get_distribution_function_plot(self, service_time_adjustment: bool):
        """
        Plotting the general independent distribution function
        :return: general independent cumulative distribution function plot
        """
        figure = plt.figure()
        factors, probabilities = self.get_distribution_function()
        factors = np.insert(factors, 0, 0)
        probabilities = np.insert(probabilities, 0, 0)

        factors = np.append(factors, factors[-1]+1)
        probabilities = np.append(probabilities, 1)
        ax = figure.add_subplot(111)
        ax.step(factors, probabilities, where="post")
        ax.text(0.85, 0.02, " mean =  {mean}\n  SDev =  {sdev} ".format(mean=round(self.get_discretized_mean(), 3),
                sdev=round(self.get_discretized_standard_deviation(), 3)),
                horizontalalignment='left',
                verticalalignment='bottom',
                transform=ax.transAxes)
        plt.ylabel('Probability')
        plt.xlabel('Factor size')
        plt.title('{distribution}'.format(distribution=self.get_type()))

        return figure, None

    def get_discretized_mean(self, factors: np.ndarray=None, factor_distribution: np.ndarray=None):
        """
        Calculation of the mean of the general independent distribution
        :param factors: list of factors
        :param factor_distribution: list of probabilities of the factors
        :return: mean of the general independent distribution
        """
        return self._get_discretized_moment(self._values, self._probabilities, 1)

    def get_discretized_variance(self, factors: np.ndarray=None, factor_distribution: np.ndarray=None):
        """
        Calculation of the variance of the general independent distribution
        :param factors: list of factors
        :param factor_distribution: list of probabilities of the factors
        :return: variance of the general independent distribution
        """
        mean = self.get_discretized_mean(self._values, self._probabilities)
        return self._get_discretized_moment(self._values, self._probabilities, 2) - np.power(mean, 2)

    def _factor_to_value(self, factor):
        """
        Calculation of the x-value from factor
        :param factor
        :return: x-value
        """
        return factor
