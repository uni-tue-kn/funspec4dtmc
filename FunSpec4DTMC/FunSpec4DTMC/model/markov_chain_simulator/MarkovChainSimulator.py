
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

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import importlib
from FunSpec4DTMC.model.markov_chain.MarkovChainConventionalApproach import MarkovChainConventionalApproach
from FunSpec4DTMC.model.markov_chain.MarkovChainForwardApproach import MarkovChainForwardApproach

class MarkovChainSimulator(object):
    global succ
    number_of_simulators = 0

    def __init__(self,
                 markov_chain: (MarkovChainForwardApproach or MarkovChainConventionalApproach),
                 identification: str=None):
        """
        Constructor MarkovChainSimulator
        :param markov_chain:  MarkovChainForwardApproach or MarkovChainConventionalApproach
        :param identification: designation of the simulator
        """
        self.number_of_simulators += 1
        self._markov_chain = markov_chain

        if identification is None:
            self._identification = 'Simulator {number}'.format(number=self.number_of_simulators)
        else:
            self.identification = identification

        self._simulator_type = "markov_chain_simulator"
        self._calculation_precision = 10e-16
        self._calculation_listeners = []

    def __str__(self):
        """
        Computes a nicely printable string representation of the Markov chain simulator
        """
        return '{MarkovChainSimulator._type}: {MarkovChainSimulator._identification}' \
            .format(MarkovChainSimulator=self)

    def calculate_stationary_state_distribution(self, simulation_steps: int, alpha: float = 1, specified_period:int=1):
        """
        Interface method for calculating the stationary state distribution
        :param simulation_steps: number of iteration steps
        :param alpha: value used for the alpha relaxation
        :param specified_period: specified value for period
        """
        raise NotImplementedError

    def calculate_subsequent_state_distribution(self, state_distribution: np.ndarray):
        """
        Interface function for calculating the successor state distribution
        :param state_distribution: current state distribution
        """
        raise NotImplementedError

    def get_graph_plot(self, graph_layout: str, mark_closures: bool):
        """
        Function for displaying the Markov chain as a graph
        :param graph_layout: layout directive of the graph
        :param mark_closures:  Possibility to highlight closures in the graph
        :return: Plot of the Markov chain graph
        """
        figure = plt.figure()
        colors = ["red","green","blue",
                  "#FF9400","#71F8FF", "#80E868",
                  "#FFB400", "E93FFF", "#DFFF47"]

        graph = self.get_markov_chain().get_graph()

        if graph is None:
            (V, E) = self.calculate_graph()
            self.get_markov_chain().set_graph((V, E))
        else:
            (V, E) = graph
        closures = self.get_markov_chain().get_closures()
        for closure in closures:
            colors.append("#000000")
        if not closures:
            closures = self.closures((V, E))
            self.get_markov_chain().set_closures(closures)
        G = nx.DiGraph()
        E = [(str(e[0]), str(e[1])) for e in list(E)]
        G.add_edges_from(E)
        color_map = []
        num_closures = len(closures)
        for node in G:
            color = "#000000"
            if mark_closures:
                for index in range(num_closures):
                    if node in [str(v) for v in closures[index]]:
                        color = colors[index]
            color_map.append(color)

        if graph_layout == "Spring layout":
            pos = nx.spring_layout(G, scale=2)
        elif graph_layout == "Circular layout":
            pos = nx.circular_layout(G, scale=2)
        elif graph_layout == "Spectral layout":
            pos = nx.spectral_layout(G, scale=2)
        else:
            pos = nx.random_layout(G)

        nodes = nx.draw_networkx_nodes(G, pos, node_color="w",
                                       node_size=600)
        nodes.set_edgecolor(color_map)
        nx.draw_networkx_labels(G, pos, color=color_map)
        nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20)
        return figure


    def calculate_graph(self):
        """
        Method for determining the graph from the Markov chain specification
        :return: Graph (V, E) of the Markov chain
        """
        if self.get_markov_chain().get_type() == "MarkovChainForwardApproach":
            (V, E) = self.calculate_graph_from_functional_definition()
        elif self.get_markov_chain().get_type() == "MarkovChainConventionalApproach":
            (V, E) = self.calculate_graph_from_conventional_definition()
        else:
            raise NotImplementedError
        return (V, E)

    def calculate_mc_period(self):
        """
        Method for determining the period of the Markov chain.
        :return: Period p of the Markov chain
        """
        period = self.get_markov_chain().get_period()
        if period == 0:

            graph = self.get_markov_chain().get_graph()

            if graph is None:

                (V, E) = self.calculate_graph()
                self.get_markov_chain().set_graph((V, E))
            else:
                (V, E) = graph
            if self.get_markov_chain().get_type() == "MarkovChainForwardApproach":
                N = len(self.get_markov_chain().get_transition_functions())
                return self.period((V, E))
            elif self.get_markov_chain().get_type() == "MarkovChainConventionalApproach":
                return self.period((V, E))
            else:
                raise NotImplementedError
        else:
            return period

    def calculate_graph_from_functional_definition(self):
        """
        Method for determining the graph from the functional Markov chain specification
        :return: Graph (V, E) of the Markov chain
        """
        V = set()
        E = set()

        states = self.get_markov_chain().get_states()
        factors = self.get_markov_chain().get_factors()
        factor_distributions = self.get_markov_chain().get_factor_distributions()
        transition_functions = self.create_transition_function_from_file_path(
            self.get_markov_chain().get_transition_functions())
        transition_function = transition_functions[0]

        for element in states[0]:
            V.add(self.round_vedge(element))

        for state in states[0]:
            for factor_index in range(len(factors[0])):
                if (factor_distributions[0])[factor_index] > 0:
                    E.add((self.round_vedge(state), self.round_vedge((transition_function)(state, (factors[0])[factor_index]))))
        for index in range(1, len(transition_functions)):
            Enew = set()
            for e in E:
                for factor_index in range(len(factors[index])):
                    if (factor_distributions[index])[factor_index] > 0:
                        Enew.add((self.round_vedge(e[0]), self.round_vedge((transition_functions[index])(e[1], (factors[index])[factor_index]))))
            E = Enew
        return (V, E)

    def round_vedge(self, v):
        if type(v) in [list, np.ndarray, tuple]:
            return tuple([round(float(value), 13) for value in v])
        else:
            return round(float(v), 13)


    def calculate_graph_from_conventional_definition(self):
        """
        Method for determining the graph from the conventional Markov chain specification
        :return: Graph (V, E) of the Markov chain
        """
        V = set()
        E = set()
        matrix = self.get_markov_chain().get_transition_matrix()
        number_of_states = len(matrix)
        for state in range(number_of_states):
            V.add(state)
            for next_state in range(number_of_states):
                if matrix[state][next_state] > 0:
                    E.add((state, next_state))
        return (V, E)

    def depth_first_search(self, graph):
        """
        Method that performs a depth search on a graph.
        :param graph: Graph that is being examined.
        :return: Vord: Search order of the depth first search
        :return: cc: connected components of graph
        """
        self.calculate_successors(graph)
        (V, E) = graph
        color = {}
        cc = []
        Vord = []
        for v in V:
            color[v] = "white"
        for v in V:

            if color[v] == "white":
                finished = []
                color, finished = self.depth_first_search_visit(v,
                                                    color,
                                                    finished)
                Vord += finished
                cc.append(finished)
        return Vord, cc

    def depth_first_search_visit(self, v, color, finished):
        """
        Auxiliary function that enables the depth search
        :param v: current vertex
        :param color: Colors of the individual vertices that indicate the visit status of each vertices
        :param finished: Contains all vertices that have been fully investigated in an ordered list.
        :return: color, finished
        """
        color[v] = "gray"

        for s in succ[v]:

            if color[s] == "white":
                color, finished \
                    = self.depth_first_search_visit(s, color, finished)

        color[v] = "black"
        finished.append(v)

        return color, finished

    def reverse_graph(self, graph):
        """
        Method for determining the reverse graph
        :param graph: Graph to be inverted
        :return: (V, revE): reversed graph
        """
        (V, E) = graph
        revE = set()
        for e in E:
            revE.add(tuple(reversed(e)))
        return V, revE

    def scc(self, graph):
        """
        Method for calculating all strongly connected components.
        :param graph: Graph that is being analyzed
        :return: scc: stringly connected components of the graph
        """

        (V, E) = graph
        revGraph = self.reverse_graph(graph)
        expansion_finishing_order, connected_components = self.depth_first_search(revGraph)
        expansion_finishing_order.reverse()
        expansion_finishing_order, connected_components = self.depth_first_search((expansion_finishing_order, E))
        scc = connected_components
        return scc

    def closures(self, graph):
        """
        Method for calculating all closures of the graph
        :param graph: Graph that is being analyzed
        :return: closures: closures of the graph
        """
        (V, E) = graph
        sccs = self.scc(graph)
        for scc in sccs:
            for u in scc:
                for v in succ[u]:
                    if v not in scc:
                            scc.clear()
        return [scc for scc in sccs if scc]

    def cycle_length(self, graph, closure):
        """
        Calculation of the minimum cycle length by means of a deep first search
        :param graph: Graph to be analyzed
        :param closure: closure to be analysed
        :return: cycle_lenth: minimum cycle length
        """
        color = {}
        depth = {}
        for v in closure:
            color[v] = "white"
            depth[v] = 0
        v = closure[0]
        cycle_length = float('inf')
        cycle_length = self.dfs_cycle_length(v, graph, closure, color, depth, cycle_length)
        return cycle_length

    def dfs_cycle_length(self, v, graph, closure, color, depth, cycle_length):
        """
        Auxiliary function for determining the minimum cycle length. This method enables the depth first search.
        :param v: current vertex
        :param graph: graph to be analyzed
        :param closure: closure to be analyzed
        :param color: colors indicating the visiting status
        :param depth: current depth of the vertex
        :param cycle_length: currently smallest found cycles length
        :return: cycle_length: smallest found cycles length
        """
        (V, E) = graph

        for u in succ[v]:
            if u in closure:
                if color[u] == "white":

                    depth[u] = depth[v] + 1
                    color[u] = "gray"
                    cycle_length = min(cycle_length,
                                       self.dfs_cycle_length(u, graph, closure, color, depth, cycle_length))
                else:
                    cycle_length = min(cycle_length, abs(depth[v] - depth[u]) + 1)
        color[v] = "black"
        return cycle_length

    def dfs_period_devisor(self, v, closure, graph, pc, color, partition):
        """
        Function for verifying the partition-specific of a possible period candidate
        :param v: currently considered vertex
        :param closure: closure to be analyzed
        :param graph: graph to be analyzed
        :param pc: possible candidate
        :param color: colors indicating the visiting status
        :param partition: list holding the partition numbers
        :return: color, partition, is_period_devisor
        """
        (V, E) = graph
        is_period_devisor = True
        for u in succ[v]:
            if u in closure:

                if color[u] == "white":
                    color[u] = "gray"
                    partition[u] = (partition[v] + 1) % pc
                    color, partition, is_period_devisor = self.dfs_period_devisor(u, closure, graph, pc, color,
                                                                                  partition)
                    color[u] = "black"
                elif ((abs((partition[u] - partition[v])) + 1) % pc) != 0:
                    is_period_devisor = False

        return color, partition, is_period_devisor

    def dfs_period(self, graph, closure):
        """
        Function for determining the period of a closure
        :param closure: closure to be analyzed
        :param graph: graph to be analyzed
        :return: period: period of the closure
        """
        (V, E) = graph
        color = {}
        partition = {}

        cycle_length = self.cycle_length(graph, closure)

        pc = 1
        pgcd = 1
        while pc <= cycle_length:
            pc = pc + 1
            if (pc % pgcd == 0) and (cycle_length % pc == 0):
                for v in closure:
                    color[v] = "white"
                v = closure[0]
                partition[v] = 0
                color[v] = "gray"
                color, partition, is_period_devisor = self.dfs_period_devisor(v, closure, graph, pc, color, partition)
                if is_period_devisor:
                    pgcd = pc
        period = pgcd
        return period


    def gcd(self, numbers: list):
        """
        Method calculating the greatest common divider of a list of numbers
        :param numbers: list of numbers
        :return: gcd: gratest common divider
        """
        gcd = numbers[0]
        for i in range(0, len(numbers)):
            gcd = self.gcd2(gcd, numbers[i])
        return gcd

    def lcm(self, numbers: list):
        """
        Method calculating the least common multiple of a list of numbers
        :param numbers: list of numbers
        :return: least common multiple
        """
        lcm = numbers[0]
        for i in range(0, len(numbers)):
            lcm = (lcm * numbers[i]) / self.gcd2(numbers[i], lcm)
        return lcm

    def gcd2(self, a: int, b: int):
        """
        Method calculating the greatest common divider of tho numbers
        :param a: first number
        :param b: second number
        :return: gcd: gratest common divider
        """
        while b is not 0:
            h = a % b
            a = int(b)
            b = int(h)
        return a

    def calculate_successors(self, graph):
        """
        Method for calculation of the successor vertices of all vertices of a graph
        :param graph:graph to be analyzed
        """
        global succ
        succ  = {}
        (V, E) = graph
        for v in V:
            succ[v] = []
            for e in E:
                if e[0] == v:
                    succ[v].append(e[1])

    def period(self, graph):
        """
        Method for calculating the period of a graph
        :param graph: graph to be analyzed
        :return: period: period of the graph
        """
        closures = self.closures(graph)
        periods = []
        for closure in closures:
            periods.append(self.dfs_period(graph, closure))
        period = int(self.lcm(periods))
        return period

    def plot_stationary_state_distribution(self, simulation_steps: int, alpha: float = 1, specified_period:int=1,
                                           figure = None, label=None):
        """
        Plots the stationary state distribution
        :param simulation_steps: iteration steps of the stationary state distribution calculation
        :param alpha: value used for alpha relaxation
        :param specified_period: specified value for period
        :param figure: figure into which the plot is integrated
        :param label: possible labels of the markov Chains
        :return plot of the stationary state distribution
        """
        if figure is None:
            figure = plt.figure()
            figure.clear()
        try:
            if self.get_markov_chain().get_stationary_state_distribution() is None or simulation_steps > 0:
                ssd = self.calculate_stationary_state_distribution(simulation_steps, alpha, specified_period)
                self.get_markov_chain().set_stationary_state_distribution(ssd)
            y_values = self.get_markov_chain().get_stationary_state_distribution()
            x_values = range(len(y_values))
        except:
            raise InterruptedError
        ax1 = figure.add_subplot(111)
        if label is None:
            ax1.plot(x_values, y_values, 'o')
        else:
            ax1.plot(x_values, y_values, 'o')
        ax1.set_ylabel('State Probability')
        ax1.set_xlabel('State')
        if label is not None:
            ax1.legend(loc='best')
        if self._markov_chain.get_state_designations() is not None:
            if len(self._markov_chain.get_state_designations()) < 30:
                ax1.set_xticks(x_values)
                ax1.set_xticklabels(self._markov_chain.get_state_designations(), rotation=90)
        else:
            if len(self._markov_chain.get_states()[0]) < 30:
                ax1.set_xticks(x_values)
                ax1.set_xticklabels(self._markov_chain.get_states()[0], rotation=90)
        return figure

    def plot_cumulative_stationary_state_distribution(self, simulation_steps: int, alpha: float=1, specified_period:int=1, figure = None, label=None):
        """
        Plots the cumulative stationary state distribution
        :param simulation_steps: iteration steps of the stationary state distribution calculation
        :param alpha: value used for alpha relaxation
        :param specified_period: specified value for period
        :param figure: figure into which the plot is integrated
        :param label: possible labels of the markov Chains
        :return plot of the cumulative stationary state distribution
        """
        if figure is None:
            figure = plt.figure()
            figure.clear()
        try:
            if self.get_markov_chain().get_stationary_state_distribution() is None or simulation_steps > 0:
                self.get_markov_chain().set_stationary_state_distribution(self.calculate_stationary_state_distribution(
                    simulation_steps, alpha, specified_period))
            y_values = self.get_markov_chain().get_stationary_state_distribution()
            y_values = np.insert(y_values, 0, 0., axis=0)
            y_values = np.cumsum(y_values)
            x_values = range(len(y_values))
        except:
            raise InterruptedError

        ax1 = figure.add_subplot(111)
        if label is None:
            ax1.step(x_values, y_values, where='pre')
        else:
            ax1.step(x_values, y_values, where='pre', label=label)
        axes = plt.gca()
        axes.set_ylim([10 ** -5, 1.1])
        ax1.set_ylabel('State Probability')
        ax1.set_xlabel('State')
        if label is not None:
            ax1.legend(loc='best')
        if self._markov_chain.get_state_designations() is not None:
            if len(self._markov_chain.get_state_designations()) < 30:
                ax1.set_xticks(x_values)
                ax1.set_xticklabels(self._markov_chain.get_state_designations(), rotation=90)
        else:
            if len(self._markov_chain.get_states()[0])< 30:
                ax1.set_xticks(x_values)
                ax1.set_xticklabels(self._markov_chain.get_states()[0], rotation=90)
        return figure

    def plot_complementary_cumulative_stationary_state_distribution(self, simulation_steps: int,
                                                                    alpha: float=1,
                                                                    specified_period: int=1,
                                                                    figure = None,
                                                                    label = None):
        """
        Plots the complementary cumulative stationary state distribution
        :param simulation_steps: iteration steps of the stationary state distribution calculation
        :param alpha: value used for alpha relaxation
        :param specified_period: specified value for period
        :param figure: figure into which the plot is integrated
        :param label: possible labels of the markov Chains
        :return plot of the complementary cumulative stationary state distribution
        """
        if figure is None:
            figure = plt.figure()
            figure.clear()
        try:
            if self.get_markov_chain().get_stationary_state_distribution() is None or simulation_steps > 0:
                self.get_markov_chain().set_stationary_state_distribution(
                    self.calculate_stationary_state_distribution(simulation_steps, alpha, specified_period))
            y_values = self.get_markov_chain().get_stationary_state_distribution()
            y_values = 1 - np.insert(np.cumsum(y_values), 0, 0., axis=0)
            x_values = range(len(y_values))
        except:
            raise InterruptedError
        ax1 = figure.add_subplot(111)
        if label is None:
            ax1.step(x_values, y_values, where="pre")
        else:
            ax1.step(x_values, y_values, where="pre", label=label)
        axes = plt.gca()
        axes.set_ylim([10 ** -5, 1.1])
        ax1.set_ylabel('State Probability')
        ax1.set_xlabel('State')
        if label is not None:
            ax1.legend(loc='best')

        if self._markov_chain.get_state_designations() is not None:
            if len(self._markov_chain.get_state_designations()) < 30:
                ax1.set_xticks(x_values)
                ax1.set_xticklabels(self._markov_chain.get_state_designations(), rotation=90)
        else:
            if len(self._markov_chain.get_states()[0]) < 30:
                ax1.set_xticks(x_values)
                ax1.set_xticklabels(self._markov_chain.get_states()[0], rotation=90)
        return figure


    @property
    def simulator_type(self)-> str:
        """
        Returns simulator_type
        :return: simulator_type: str
        """
        return self._simulator_type


    def get_markov_chain(self):
        """
        Returns markov_chain
        :return: markov_chain
        """
        return self._markov_chain


    def set_markov_chain(self, markov_chain: MarkovChainForwardApproach or MarkovChainConventionalApproach):
        """
        Sets Markov_chain
        :param markov_chain: MarkovChainForwardApproach of MarkovChainConventionalApproach
        """
        self._markov_chain = markov_chain

    def get_identification(self)->str:
        """
        Returns identification of the simulator
        :return: identification
        """
        return self._identification


    def set_identification(self, identification: str):
        """
        Sets indentication
        :param identification: designation of the simulator
        """
        self._identification = identification

    def set_calculation_precision(self, precision):
        """
        Method for adjusting the calculation accuracy
        :param precision: Precision of the calculation
        """
        self._calculation_precision = precision

    def get_calculation_precision(self):
        """
        Method to read the calculation accuracy
        :return precision: Precision of the calculation
        """
        return self._calculation_precision

    def notify_calculation_listeners(self, step: int, norm=None):
        """
        Function that informs all registered listeners about the calculation status
        :param step: current step
        :param norm: current accuracy of the calculation
        """
        for function in self._calculation_listeners:
            try:
                function(step, norm)
            except:
                raise InterruptedError

    def add_calculation_listener(self, listener: object):
        """
        Function to register as a calculation listener
        :param listener: listener  that will be registered
        """
        self._calculation_listeners.append(listener)

    @staticmethod
    def norm(x: np.ndarray, xpred: np.ndarray):
        """
        method for determining the infinite norm of two vectors
        :param x: current state vector
        :param xpred: predecessor state vector
        :return: ||x, xpred||
        """
        return max([abs(diff) for diff in x-xpred])


    def create_transition_function_from_file_path(self, file_path):
        TransitionFunction = importlib.import_module(file_path)
        transition_functions = []
        index = 1
        while hasattr(TransitionFunction
                , 'transition_function{index}'.format(index=index)):
            transition_functions.append(
                getattr(TransitionFunction, 'transition_function{index}'.format(index=index)))
            index += 1
        return transition_functions
