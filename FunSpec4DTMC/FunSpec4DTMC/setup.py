
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

from Cython.Build import cythonize
from distutils.core import setup
import numpy

setup(
      ext_modules=cythonize("./FunSpec4DTMC/model/markov_chain_simulator/forward_algorithm_cython_implementation/ForwardAlgorithm.pyx"),
      include_dirs=[numpy.get_include()],
      requires=['Cython', 'matplotlib', 'numpy']
     )
