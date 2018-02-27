
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
from scipy.stats import expon
from FunSpec4DTMC.model.Systems.distributions.DiscretizedDistribution import DiscretizedDistribution


class DiscretizedExponentialDistribution(DiscretizedDistribution):

    def __init__(self, interval_size: float, maximum, rate: float = 1):
        """
        Constructor exponential distribution
        :param: rate: Rate of the exponential distribution
        :param interval_size: Discretization interval size
        :param maximum: Truncation maximum of discretization
        """
        if (interval_size, rate) > (0, 0):
            DiscretizedDistribution.__init__(self, interval_size, maximum)
            self._rate = rate
            self._type = 'DiscretizedExponentialDistribution($\lambda$={rate}):'.format(rate=self._rate)
        else:
            raise ValueError

    def _cdf(self, value: float):
        """
        Defines the  cumulative exponential distribution function
        :param value: x-value
        :return: Function value at point x
        """
        if self._research_mode:
            return expon.cdf(value, scale=1/self.rate)
        else:
            if value >= 0:
                return 1 - math.exp(-self._rate * value)
            else:
                return 0

    def _pdf(self, value: float):
        """
        Defines the exponential distribution
        :param value: x-value
        :return: Function value at point x
        """
        if self._research_mode:
            return expon.pdf(value, scale=1/self.rate)
        else:
            if value >= 0:
                return self._rate * math.exp(-self._rate * value)
            else:
                return 0

    @property
    def rate(self):
        """
        Returns the rate of the exponential distribution
        :return: rate
        """
        return self._rate

    @rate.setter
    def rate(self, rate: float):
        """
        Sets rate of exponential distribution
        :param: rate of the exponential distribution
        """
        if rate > 0:
            self._rate = rate
        else:
            raise ValueError

    def get_mean(self):
        """
        Calculates mean value of exponential distribution
        :return: mean
        """
        return 1.0/self._rate

    def get_variance(self):
        """
        Calculates variance of exponential distribution
        :return: variance
        """
        return 1.0/math.pow(self._rate, 2)

    def get_standard_deviation(self):
        """
        Calculates standard deviation of exponential distribution
        :return: standard deviation
        """
        return 1.0 / self._rate