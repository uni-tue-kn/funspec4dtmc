
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

import scipy.linalg
import numpy as np
from FunSpec4DTMC.model.markov_chain_simulator.MarkovChainSimulator import MarkovChainSimulator
import FunSpec4DTMC.model.markov_chain.MarkovChain as MarkovChain

class MCSDirectApproach(MarkovChainSimulator):
    def __init__(self, research_mode, scheme, markov_chain: MarkovChain = None, identification: str = None):
        """
        Constructor MCSDirectApproach
        :param: markov_chain: MarkovChainConventionalApproach
        :param: get_identification: str
        """
        MarkovChainSimulator.__init__(self, markov_chain, identification)
        self._research_mode = research_mode
        self._scheme = scheme
        self._type = "MCSDirectApproach"

    def calculate_stationary_state_distribution(self, simulation_steps: int = None, alpha=None, specified_period:int=1):
        """
        Method for calculating the stationary state distribution
        :param simulation_steps: number of iteration steps
        :param alpha: value used for the alpha relaxation
        :param specified_period: specified value for period
        :return stationary state distribution
        """
        A = self.get_markov_chain().get_transition_matrix()
        Q = np.eye(len(A)) - A
        if self._research_mode:
            P, L, U = scipy.linalg.lu(np.transpose(Q))
        else:
            L, U = self.lu_decomposition(np.transpose(Q))


        if self._scheme == "Gaussian scheme":
            y = np.zeros(len(U)-1)
            U = U[:-1]
            xs = self.backward_substitution(U, y, 1)
        else:
            en = np.zeros(len(U))
            en[-1] = 1 * np.finfo(float).eps
            xs = en
            xs = self.backward_substitution(U, xs)
        return xs/np.sum(xs)


    def pivoting(self, A, i):
        """
        Method that performs the pivoting of the matrix
        :param A: matrix
        :param i: current evaluation index
        :return: pivoted matrix
        """
        dimension = len(A)
        maximum = 0.0
        max = i
        for j in range(i, dimension):
            if (abs(A[j][i]) > maximum):
                maximum = abs(A[j][i])
                max = j

        if i != max:
            self.swap_rows(A, i, max)

        if A[i, i] == 0:
            A[i, i] = np.finfo(np.float32).eps

    def swap_rows(self, A, i, max):
        """
        Method to swap a row i with the pivot row
        :param A: input matrix
        :param i: cuurent evaluation index
        :param max: index of the pivor element
        :return: swapped matrix
        """
        A[[i, max], :] = A[[max, i], :]

    def forward_substitution(self, L, b):
        """
        Method to perform the forward substitution step L*y = b of the LU-decomposition
        :param L: lower triangular matrix
        :param b: result vector
        :return: y: solution vector
        """
        y = np.zeros(len(b))

        for i in range(len(b)):
            y[i] = b[i]

            for j in range(i):
                y[i] -= L[i][j] * y[j]

            y[i] /= L[i][i]

        return y

    def backward_substitution(self, U, y, mu=None):
        """
        Method to perform the backward substitution step U*x = y of the LU-decomposition
        :param L: upper triangular matrix
        :param y: result vector
        :return: x: solution vector
        """
        if mu is None:
            x = np.zeros(len(y))
        else:
            x = np.zeros(len(y) + 1)
            x[-1] = mu

        for i in reversed(range(len(y))):
            x[i] = y[i]
            for j in range(i + 1, len(x)):
                x[i] -= U[i][j] * x[j]
            x[i] /= U[i][i]

        return x


    def lu_decomposition(self, A):
        """
        Method to perform the lu-decomposition of a matrix
        :param A: input matrix
        :return: L: lower triangular matrix
        :return: U: upper triangular matrix
        """
        M = np.copy(A)
        n = len(M)
        L = np.zeros((n,n))
        U = np.zeros((n, n))
        for i in range(n):

            self.pivoting(M, i)
            for j in range(i + 1):
                s = 0
                for k in range(j):
                    s += (U[k][i] * L[j][k])
                U[j][i] = M[j][i] - s

            for j in range(i, n):
                s = 0
                for k in range(i):
                    s += U[k][i] * L[j][k]
                if U[i][i] != 0:
                    L[j][i] = (M[j][i] - s) / U[i][i]
        return L, U
