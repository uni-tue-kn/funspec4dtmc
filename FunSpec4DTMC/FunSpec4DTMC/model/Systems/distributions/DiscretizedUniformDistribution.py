
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

import math
from FunSpec4DTMC.model.Systems.distributions.DiscretizedDistribution import DiscretizedDistribution


class DiscretizedUniformDistribution(DiscretizedDistribution):

    def __init__(self, interval_size: float, minimum_value: float=0, maximum_value: float=10):
        """
        Constructor discretized uniform distribution
        :param interval_size: Discretization interval size
        :param minimum: Minimum x-value of the uniform discretization
        :param maximum: Maximum x-value of the uniform discretization
        """
        if (interval_size, maximum_value) > (0, 0):
            DiscretizedDistribution.__init__(self, interval_size, maximum_value)
            self._minimum_value = minimum_value
            self._maximum_value =  maximum_value
            self._type = 'DiscretizedUniformDistribution(a = {min},  b = {max}):'.format(max=self._maximum_value,
                                                                                         min=self._minimum_value)
        else:
            raise ValueError

    def get_distribution(self, service_time_adjustment: bool=False):
        """
        Calculation of uniform distribution as vector
        :param service_time_adjustment: adjustment of the selected service time to calculation precision
        :return: uniform distribution as vector
        """
        probabilities = []
        factors = []
        number_of_states = math.ceil((self._maximum_value + self._interval_size-self._minimum_value)/self._interval_size) + 1
        for factor in range(number_of_states):
            factors.append(factor)
            probability = self._cdf(self._minimum_value + (factor + 1) * self._interval_size) - \
                          self._cdf(self._minimum_value + factor * self._interval_size)
            probabilities.append(probability)
        return factors, probabilities, self._interval_size

    def _cdf(self, value: float):
        """
        Defines the cumulative uniform distribution function
        :param value: x-value
        :return: Function value at point x
        """
        if self._minimum_value <= value <= self._maximum_value:
            return (value-self._minimum_value)/(self._maximum_value+ self._interval_size-self._minimum_value)
        elif value < self._minimum_value:
            return 0.0
        else:
            return 1.0

    def _pdf(self, value: float):
        """
        Defines the unfiform distribution
        :param value: x-value
        :return: Function value at point x
        """
        if self._minimum_value <= value <= self._maximum_value:
            return 1.0 / (self._maximum_value - self._minimum_value)
        else:
            return 0

    def get_mean(self):
        """
        Calculates mean value of the uniform distribution
        :return: mean
        """
        return (self._maximum_value + self._minimum_value)/2

    def get_variance(self):
        """
        Calculates variance of the uniform distribution
        :return: mean
        """
        return math.pow(self._maximum_value - self._minimum_value, 2)/12

    def get_standard_deviation(self):
        """
        Calculates standard deviation of the uniform distribution
        :return: mean
        """
        return math.sqrt(self.get_variance())

