
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
from scipy.stats import gamma
from FunSpec4DTMC.model.Systems.distributions.DiscretizedDistribution import DiscretizedDistribution


class DiscretizedGammaDistribution(DiscretizedDistribution):
    def __init__(self, interval_size: float, maximum: float, alpha: float = 1, beta: float=1):
        """
        Constructor of the discrtized gamma distribution
        :param: rate: Rate of the gamma distribution
        :param interval_size: Discretization interval size
        :param maximum: Truncation maximum of discretization
        """
        if (interval_size, alpha, beta) > (0, 0, 0):
            DiscretizedDistribution.__init__(self, interval_size, maximum)
            self._alpha = alpha
            self._beta = beta
            self._type = 'DiscretizedGammaDistribution($\\alpha$={alpha}, $\\beta$={beta}):'.format(alpha=self.alpha, beta=self.beta)
        else:
            raise ValueError

    def _cdf(self, value: float):
        """
        Defines the  cumulative gamma distribution function
        :param value: x-value
        :return: Function value at point x
        """
        return gamma.cdf(value, a=self._alpha, scale=self._beta)

    def _pdf(self, value: float):
        """
        Defines the gamma distribution
        :param value: x-value
        :return: Function value at point x
        """
        if self._research_mode:
            return gamma.pdf(value, a=self._alpha, scale=self._beta)
        else:
            if value > 0:
                return (math.pow(self.beta, -self.alpha) * math.pow(value, self.alpha-1) * math.exp(-value/self.beta)) / \
                       math.gamma(self.alpha)
            else:
                return 0


    def get_distribution(self, service_time_adjustment: bool=False):
        """
        Returns discretized gamma distribution as a vector
        :return: discretized gamma distribution
        """
        probabilities = []
        factors = []
        if self._maximum is not None:

            number_of_factors = int(np.ceil(self._maximum / self._interval_size))

            for factor in range(number_of_factors):
                factors.append(factor)
                probabilities.append(self._pdf(self._factor_to_value(factor) + self._interval_size / 2)*self._interval_size)
        else:
            criteria = False
            self._interval_size *= 10

            while not criteria:
                factor = 0
                probabilities = []
                self._interval_size /= 10
                while max(1 - self._cdf(self._factor_to_value(factor)), 0) > self.epsilon:
                    probabilities.append(self._pdf(self._factor_to_value(factor) + self._interval_size / 2)*self._interval_size)
                    factor += 1
                factors = range(len(probabilities))
                mean = self.get_discretized_mean(factors, probabilities)
                if service_time_adjustment:
                    if (abs(mean - self.get_mean()) < self.epsilon):
                        sdev = self.get_discretized_standard_deviation_by_mean(mean, factors, probabilities)
                        criteria = (abs(sdev - self.get_standard_deviation()) < self.epsilon)
                else:
                    criteria = True

        probabilities /= np.sum(probabilities)
        return factors, probabilities, self._interval_size

    @property
    def alpha(self):
        """
        Returns the rate of the alpha value
        :return: alpha
        """
        return self._alpha

    @alpha.setter
    def alpha(self, alpha: float):
        """
        Sets alpha of gamma distribution
        """
        if alpha > 0:
            self._alpha = alpha
        else:
            raise ValueError

    @property
    def beta(self):
        """
        Returns beta of the gamma distribution
        :return: rate
        """
        return self._beta

    @beta.setter
    def beta(self, beta: float):
        """
        Sets beta of the gamma distribution
        """
        if beta > 0:
            self._beta = beta
        else:
            raise ValueError

    def get_mean(self):
        """
        Calculates mean value of the gamma distribution
        :return: mean
        """
        return self.alpha*self._beta

    def get_variance(self):
        """
        Calculates variance of gamma distribution
        :return: variance
        """
        return self.alpha*math.pow(self.beta, 2)

    def get_standard_deviation(self):
        """
        Calculates standard deviation of the gamma distribution
        :return: standard deviation
        """
        return math.sqrt(self.get_variance())

    def get_coefficient_of_variation(self):
        """
        Calculates coefficient of variation of the gamma distribution
        :return: coefficient of variation
        """
        return 1/math.sqrt(self.alpha)
