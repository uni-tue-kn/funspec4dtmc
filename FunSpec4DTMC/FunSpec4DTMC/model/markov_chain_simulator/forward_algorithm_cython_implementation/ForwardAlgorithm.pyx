
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
cimport numpy as np
import importlib

cdef list create_transition_function_from_file_path(str file_path):
        cdef tf
        cpdef tf2
        TransitionFunction = importlib.import_module(file_path)

        transition_functions = []
        index = 1
        while hasattr(TransitionFunction
                , 'transition_function{index}'.format(index=index)):
            try:
                tf = getattr(TransitionFunction, 'transition_function{index}'.format(index=index))
                transition_functions.append(tf)
            except:
                tf2 = getattr(TransitionFunction, 'transition_function{index}'.format(index=index))
                transition_functions.append(tf2)


            index += 1
        return transition_functions

cpdef forward_algorithm(list states_list, np.ndarray initial_state_distribution, factor_list, list factor_distributions, str functions):
    """
    Method for calculating the stationary state distribution
    :param simulation_steps: number of iteration steps
    :param alpha: value used for the alpha relaxation
    :return stationary state distribution
    """
    cdef list transition_functions
    transition_functions = create_transition_function_from_file_path(functions)
    cdef int index = 0
    cdef int state_index
    cdef int j
    cdef int number_of_states = len(states_list[0])
    cdef int number_of_functions = len(transition_functions)
    cdef double[:] new_dist
    cdef np.ndarray curr_states
    cdef dict map
    cdef int i
    cdef double[:] old
    old = initial_state_distribution[:]
    for index in range(number_of_functions):
        new_dist = np.zeros(number_of_states)
        curr_states = states_list[index]
        map = {}
        for state_index in range(len(curr_states)):
            try:
                map[str(float(curr_states[state_index]))] = int(state_index)
            except:
                map[str(tuple(curr_states[state_index]))] = int(state_index)
        for j in range(number_of_states):
            if old[j] != 0.0:
                curr_factors = factor_list[index]
                curr_factor_distribution = factor_distributions[index]
                l = len(curr_factors)
                for k in range(l):
                    i = map[str(adjust_input_type(transition_functions[index](curr_states[j], curr_factors[k])))]
                    new_dist[i] += old[j] * curr_factor_distribution[k]
        old = new_dist
    xs = old
    return np.asarray(xs)

cpdef transition_matrix(list states_list, list factor_list, list factor_distributions, list transition_functions):
    """
    Calculates the transition matrix by applying the forwarding algorithm.
    :return: transition matrix
    """
    cdef int number_of_states = len(states_list[0])
    cdef int number_of_functions = len(transition_functions)
    cdef np.ndarray new_transition_matrix
    cdef np.ndarray curr_states
    cdef dict map
    cdef np.ndarray transition_matrix =  np.eye(number_of_states)
    for index in range(number_of_functions):
        new_transition_matrix = np.zeros((number_of_states, number_of_states))
        curr_states = states_list[index]
        map = {}
        for state_index in range(len(curr_states)):
            try:
                map[str(float(curr_states[state_index]))] = int(state_index)
            except:
                map[str(tuple(curr_states[state_index]))] = int(state_index)
        for j in range(len(curr_states)):
            curr_factors = factor_list[index]
            curr_factor_distribution = factor_distributions[index]
            l = len(curr_factors)
            for k in range(l):
              new_transition_matrix[map[str(adjust_input_type(curr_states[j]))],
                                            map[str(adjust_input_type(transition_functions[index](curr_states[j], curr_factors[k])))]] \
                            += curr_factor_distribution[k]
        transition_matrix = np.dot(transition_matrix, new_transition_matrix)
    return transition_matrix


cdef object adjust_input_type(input):
    if type(input) in [list, tuple, np.ndarray]:
        return tuple([round(float(value), 13) for value  in input])
    else:
        return round(float(input), 13)