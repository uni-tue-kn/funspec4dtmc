
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
import numpy as np
from FunSpec4DTMC.model.Systems.distributions.DiscretizedDistribution import DiscretizedDistribution


class DiscretizedHyperexponentialDistribution(DiscretizedDistribution):

    def __init__(self, interval_size: float, maximum: float, li: list, pi: list):
        """
        Constructor hyperexponential distrbution
        :param: lambda values of the hyperexponential distribution
        :param: probabilities of the different exponential distributions
        :param interval_size: Discretization interval size
        :param maximum: Truncation maximum of discretization
        """
        if (interval_size) > 0:
            DiscretizedDistribution.__init__(self, interval_size, maximum)
            self._pi = pi
            self._li = li
            self._type = 'DiscretizedHyperxponentialDistribution ($p_i$={pi}, $\lambda_i$={li}):'.format(pi=self._pi, li= self._li)
        else:
            raise ValueError

    def _cdf(self, value: float):
        """
        Defines the cumulative hyperexponential distribution function
        :param value: x_value
        :return: Function value at point x
        """
        if value >= 0:
            sum = 0
            for i in range(len(self._li)):
                sum += self._pi[i] * np.exp(- self._li[i] * value)
            return 1 - sum
        else:
            return 0

    def _pdf(self, value: float):
        """
        Defines the hyperexponential distributiom
        :param value: x-value
        :return: Function value at point x
        """
        if value >= 0:
            sum = 0
            for i in range(len(self._li)):
                sum += self._pi[i] * self._li[i]* np.exp(- self._li[i] * value)
            return sum
        else:
            return 0

    def get_mean(self):
        """
        Calculates mean value of hyperexponential distribution
        :return: mean
        """
        sum = 0
        for i in range(len(self._pi)):
            sum += 1/self._li[i] * self._pi[i]
        return sum

    def get_variance(self):
        """
        Calculates variance of hyperexponential distribution
        :return: mean
        """
        sum = 0
        for i in range(len(self._pi)):
            sum += 2 / math.pow(self._li[i], 2) * self._pi[i]
        return sum - math.pow(self.get_mean(), 2)

    def get_standard_deviation(self):
        """
        Calculates standard deviation of hyperexponential distribution
        :return: mean
        """
        return np.sqrt(self.get_variance())
