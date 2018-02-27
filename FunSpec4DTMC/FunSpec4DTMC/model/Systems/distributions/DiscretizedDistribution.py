
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


class DiscretizedDistribution:
    """
    Interface class for discreteized distributions
    """


    def __init__(self, interval_size: float, maximum: float):

        """
        Constructor of the interface class
        :param interval_size: discretization interval size
        :param maximum: Truncation maximum of discretization
        """

        self._type = 'DiscretizedDistribution'
        self._interval_size = interval_size
        self._maximum = maximum
        self._research_mode = False
        self.epsilon = None

    def set_epsilon(self, epsilon: float):
        """
        Method to set the discretization epsilon
        :param epsilon: discretization interval
        """
        self.epsilon = epsilon

    def enable_research_mode(self, enabled: bool):
        """
        Method for activating the research mode. Otherwise, teaching mode is used.
        :param enabled: Selection whether activated.
        """
        self._research_mode = enabled

    def _cdf(self, value: float):
        """
        Cumulative discrete distribution function
        :param value: Evaluation location x
        """
        raise NotImplementedError

    def _pdf(self, value: float):
        """
        Discrete distribution function
        :param value: Evaluation location x
        """
        raise NotImplementedError

    def get_distribution(self, service_time_adjustment: bool=False):
        """
        Calculation of the discrete distribution
        :param service_time_adjustment: Automatic adjustment of the service time
        :return: discretized distribution
        """
        probabilities = []
        factors = []
        if self._maximum is not None:
            number_of_factors = int(np.ceil(self._maximum / self._interval_size))
            for factor in range(number_of_factors):
                factors.append(factor)
                probability = self._cdf(self._factor_to_value(factor + 0.5)) - \
                              self._cdf(self._factor_to_value(factor - 0.5))
                probabilities.append(probability)

        else:
            criteria = False
            self._interval_size *= 10

            while not criteria:
                factor = 0
                factors = []
                probabilities = []
                self._interval_size /= 10
                while abs(1 - self._cdf(self._factor_to_value(factor))) > self.epsilon:
                    probability = self._cdf(self._factor_to_value(factor + 0.5)) - \
                                  self._cdf(self._factor_to_value(factor - 0.5))
                    probabilities.append(round(probability, 13))
                    factors.append(round(self._factor_to_value(factor), 13))
                    factor += 1
                mean = self.get_discretized_mean(factors, probabilities)
                if service_time_adjustment:
                    if (abs(mean - self.get_mean()) < self.epsilon):
                        sdev = self.get_discretized_standard_deviation_by_mean(mean, factors, probabilities)
                        criteria = (abs(sdev - self.get_standard_deviation()) < self.epsilon)
                else:
                    criteria = True
        probabilities /= np.sum(probabilities)
        return factors, probabilities, self._interval_size


    def get_distribution_plot(self, service_time_adjustment: bool):
        """
        Plot of the discrete distribution
        :param service_time_adjustment: Automatic adjustment of the service time
        :return: discretized distribution
        """
        figure = plt.figure()
        factors, probabilities, interval_size = self.get_distribution(service_time_adjustment)
        ax = figure.add_subplot(111)
        ax.step([factor * interval_size for factor in list(factors)], probabilities, where="post")

        ax.text(0.8, 0.98, "Calculated: \n mean = {mean} \n SDev = {sdev} \n "
                           "Expected:\n mean = {expMean} \n SDev = {expSdev}"
                .format(mean=round(self.get_discretized_mean(factors, probabilities), 5),
                        sdev=round(self.get_discretized_standard_deviation(factors, probabilities), 5),
                        expMean=round(self.get_mean(), 5),
                        expSdev=round(self.get_standard_deviation(), 5)),
                horizontalalignment='left',
                verticalalignment='top',
                transform=ax.transAxes)

        plt.ylabel('Probability')
        plt.xlabel('Factor size (as multiple of the service time)')
        plt.title('{distribution}'.format(distribution=self.get_type()))

        return figure, self._interval_size

    def get_distribution_function_plot(self, service_time_adjustment: bool):
        """
        Plot of the discrete distribution function
        :param service_time_adjustment: Automatic adjustment of the service time
        :return: discretized distribution function
        """

        figure = plt.figure()
        factors, probabilities, interval_size = self.get_distribution(service_time_adjustment)
        ax = figure.add_subplot(111)
        ax.step([factor * interval_size for factor in list(factors)], np.cumsum(probabilities), where="post")
        ax.text(0.85, 0.02, "Calculated: \n mean = {mean} \n SDev = {sdev} \n "
                           "Expected:\n mean = {expMean} \n SDev = {expSdev}"
                .format(mean=round(self.get_discretized_mean(factors, probabilities), 3),
                        sdev=round(self.get_discretized_standard_deviation(factors, probabilities), 3),
                        expMean=round(self.get_mean(), 3),
                        expSdev=round(self.get_standard_deviation(), 3)),
                horizontalalignment='left',
                verticalalignment='bottom',
                transform=ax.transAxes)
        plt.ylabel('P(t)')
        plt.xlabel('t')
        plt.title('{distribution}'.format(distribution=self.get_type()))

        return figure, self._interval_size

    def __str__(self):
        """
        Computes a nicely printable string representation
        """
        return self._type

    def get_type(self):
        """
        Returns the get_type of the distribution
        :return: str
        """
        return self._type

    def _get_discretized_moment(self, factors: np.array, factor_distribution: np.array, power: int):
        """
        Calculates the statistical moments of the discretized distribution
        :param factors: List of factors
        :param factor_distribution: List of factor probabilities
        :param power: Exponent of the moment calculation
        :return: discretized moment of the distribution
        """
        moment = 0
        for index in range(len(factors)):
            moment += np.power(self._factor_to_value(factors[index]), power) * factor_distribution[index]
        return moment

    def get_mean(self):
        """
        Calculation of the mean
        """
        raise NotImplementedError

    def get_discretized_mean(self, factors: np.array=None, factor_distribution: np.array=None):
        """
        Calculation of the mean of the discretized distribution
        :param factors: List of factors
        :param factor_distribution: List of factor probabilities
        :return: mean of the discretized distribution
        """
        if factors is None or factor_distribution is None:
            factors, factor_distribution, interval_size = self.get_distribution()
        return self._get_discretized_moment(factors, factor_distribution, 1)

    def get_variance(self):
        """
        Calculation of the variance
        """
        raise NotImplementedError

    def get_discretized_variance(self, factors: np.array=None, factor_distribution: np.array=None):
        """
        Calculation of the variance of the discretized distribution
        :return: discretized variance
        """
        if factors is None or factor_distribution is None:
            factors, factor_distribution, interval_size = self.get_distribution()
        mean = self.get_discretized_mean(factors, factor_distribution)
        return self._get_discretized_moment(factors, factor_distribution, 2) - np.power(mean, 2)

    def get_discretized_variance_by_mean(self, mean: float, factors: np.array=None, factor_distribution: np.array=None):
        """
        Returns the variance using calculated mean
        :return: discretized variance
        """
        if factors is None or factor_distribution is None:
            factors, factor_distribution, interval_size = self.get_distribution()
        return self._get_discretized_moment(factors, factor_distribution, 2) - np.power(mean, 2)

    def get_standard_deviation(self):
        """
        Calculation of the standard deviation
        :return: standard deviation
        """
        return np.sqrt(self.get_variance())

    def get_discretized_standard_deviation(self, factors: np.array=None, factor_distribution: np.array=None):
        """
        Calculation of the standard deviation of the discretized distribution
        :return: discretized standard deviation
        """
        return np.sqrt(self.get_discretized_variance(factors, factor_distribution))

    def get_discretized_standard_deviation_by_mean(self, mean: float, factors: np.array=None, factor_distribution:np.array=None):
        """
        Returns the standard deviation using calculated mean
        :return: discretized standard deviation
        """
        return np.sqrt(self.get_discretized_variance_by_mean(mean, factors, factor_distribution))

    def _factor_to_value(self, factor: float):
        """
        Returns the x_value to related factor
        :return: x-value
        """
        if factor > 0:
            return factor * self._interval_size
        else:
            return 0

    def set_interval_size(self, interval_size: float):
        """
        Setting the interval size for discretization
        :param interval_size: discretization interval
        """
        self._interval_size = interval_size
