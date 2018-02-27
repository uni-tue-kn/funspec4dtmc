
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
from scipy.stats import erlang
from FunSpec4DTMC.model.Systems.distributions.DiscretizedDistribution import DiscretizedDistribution


class DiscretizedKErlangDistribution(DiscretizedDistribution):

    def __init__(self, interval_size: float, maximum: float, rate: float=1, k: int=1):
        """
        Constructor K-Erlang distribution
        :param: rate: Rate of the K-Erlang distribution
        :param: k: k-value of the K-Erlang distribution
        :param interval_size: Discretization interval size
        :param maximum: Truncation maximum of discretization
        """
        if (interval_size, rate, k) > (0, 0, 0, 0):
            DiscretizedDistribution.__init__(self, interval_size, maximum)
            self._rate = rate
            self._k = k
            self._type = 'DiscretizedKErlangDistribution($\lambda$ = {rate}, $k$={k}):'.format(rate=self.rate, k=self.k)
        else:
            raise ValueError



    def _cdf(self, value: float):
        """
        Defines the  cumulative K-Erlang distribution function
        :param value: x-value
        :return: Function value at point x
        """
        if self._research_mode:
            return erlang.cdf(value, a=self._k, scale=1/self.rate)
        else:
            if value >= 0:
                exponential_partial_sum = 0
                for i in range(0, self.k):
                    exponential_partial_sum += math.pow(self.rate * value, i)/math.factorial(i)

                return 1 - math.exp(-self.rate * value) * exponential_partial_sum
            else:
                return 0

    def _pdf(self, value: float):
        """
        Defines the K-Erlang distribution
        :param value:
        :return: Function value at point x
        """
        if self._research_mode:
            return erlang.pdf(value, a=self._k, scale=1 / self.rate)
        else:
            if value >= 0:
                return math.pow(self.rate * value, self.k - 1) / (math.factorial(self.k - 1)) \
                       * self.rate * math.exp(-self.rate * value)
            else:
                return 0

    @property
    def rate(self):
        """
        Returns the rate of the K-Erlang distribution
        :return: rate
        """
        return self._rate

    @rate.setter
    def rate(self, rate: float):
        """
        Sets rate of K-Erlang distribution
        """
        if rate > 0:
            self._rate = rate
        else:
            raise ValueError

    @property
    def k(self):
        """
        Returns the k of the K-Erlang distribution
        :return: rate
        """
        return self._k

    @k.setter
    def k(self, k: int):
        """
        Sets k of the of K-Erlang distribution
        """
        if k > 0:
            self._k = k
        else:
            raise ValueError

    def get_mean(self):
        """
        Calculates mean value of K-Erlang distribution
        :return: mean
        """
        return self.k/self.rate

    def get_variance(self):
        """
        Calculates variance of K-Erlang distribution
        :return: mean
        """
        return self.k/math.pow(self._rate, 2)
