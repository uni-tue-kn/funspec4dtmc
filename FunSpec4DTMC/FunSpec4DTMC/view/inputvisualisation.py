
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

from PyQt5.QtWidgets import QDialog
from FunSpec4DTMC.view.ui_inputvisualisation import Ui_InputVisualisation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib import rcParams
rcParams['text.usetex'] = True


class InputVisualisation(QDialog, Ui_InputVisualisation):

    def __init__(self):
        """
        Constructor of the class InputVisualization
         """
        super(InputVisualisation, self).__init__()

        # Set up the user interface created by the Qt Designer.
        self.setupUi(self)
        self.canvas = FigureCanvas(plt.figure())
        self.canvas1 = FigureCanvas(plt.figure())
        self.layoutMatrix.addWidget(self.canvas)
        self.layoutMatrix_2.addWidget(self.canvas1)


    def visualize_input(self, markov_chain, factors=None):
        """
        Method for visualization of a Markov chain
        :param markov_chain: markov chain to be visualized
        :param factors: optional factor input
        """
        layout = r'{'
        for i in range(len(markov_chain.get_initial_state_vector)):
            layout += r'r'
        layout += r'}'

        self.initialStateDistribution = plt.figure()
        self.initialStateDistribution.clear()

        ax = self.initialStateDistribution.add_subplot(111)
        input = self.get_latexarray(markov_chain.get_initial_state_vector)

        self.initialStateDistribution.suptitle(
            r'$\left( \begin{array}' + layout + r' {input} \end{{array}}\right)$'.format(input=input),
            fontsize=16,
            x=0.5,
            horizontalalignment='center',
            verticalalignment='top')

        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        self.layoutMatrix_2.removeWidget(self.canvas1)
        self.canvas1 = FigureCanvas(self.initialStateDistribution)
        self.layoutMatrix_2.addWidget(self.canvas1)


        if markov_chain.get_type == "MarkovChainConventionalApproach":
            self.transitionMatrix = plt.figure()
            self.transitionMatrix.clear()

            ax = self.transitionMatrix.add_subplot(111)
            input = self.get_latexarray(markov_chain.set_transition_matrix)

            self.transitionMatrix.suptitle(r'$\left( \begin{array}' + layout + r' {input} \end{{array}}\right)$'.format(input=input),
                                 fontsize=16,
                                 x=0.5,
                                 horizontalalignment='center',
                                 verticalalignment='top')




            ax.spines["left"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["top"].set_visible(False)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)

            self.layoutMatrix.removeWidget(self.canvas)
            self.canvas = FigureCanvas(self.transitionMatrix)
            self.layoutMatrix.addWidget(self.canvas)


        elif markov_chain.get_type == "MarkovChainForwardApproach":

            self.layoutMatrix.removeWidget(self.canvas)
            self.canvas = FigureCanvas(factors)
            self.layoutMatrix.addWidget(self.canvas)


    def get_latexarray(self, a):
        """
        Method to get a latex representation of an array
        :param a: vector a
        :return: latex representation of a
        """
        if len(a.shape) > 2:
            raise ValueError('bmatrix can at most display two dimensions')
        lines = str(a).replace('[', '').replace(']', '').splitlines()
        rv = []
        rv += [' , & '.join(l.split()) + r'\\' for l in lines]
        rv = ' '.join(rv)
        return rv