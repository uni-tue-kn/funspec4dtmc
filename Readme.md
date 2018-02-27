# FunSpec4DTMC <br/> A Tool for Modelling Discrete-Time Markov Chains (DTMCs) Using Functional Specification

We present a tool for the analysis of finite discrete-time Markov chains (DTMCs).
As a novelty, the tool offers functional specification of DTMCs and implements forward algorithms to compute the stationary state distribution <img src="https://latex.codecogs.com/gif.latex?x_s" />  of the DTMC or 
derive its transition matrix .
In addition, we implement nine direct and iterative algorithms to compute various metrics of DTMCs based on <img src="https://latex.codecogs.com/gif.latex?P" />  including an algorithm to determine the period of the DTMC.

![GUI of FunSpec4DTMC](http://atlas.informatik.uni-tuebingen.de/git/hauserf/2017-Markov-Chains/raw/master/poster/figures/MainWindow.PNG)

## Motivation
The tool is intended for production purposes as well as a platform for teaching the functional specification of DTMCs.

- Status quo: analysis tools and libraries for teaching that utilize <img src="https://latex.codecogs.com/gif.latex?P" /> 
- Gap: Library to apply the functional specification of DTMCs

For this reason FunSpec4DTMC offers the following specification types:
### Conventional Specification of DTMCs

- Conventional Specification of DTMCs
   - States <img src="https://latex.codecogs.com/gif.latex?X" /> 
   - Stochastic transition matrix <img src="https://latex.codecogs.com/gif.latex?P" />  holding transition probabilities
- Computation of consecutive state distributions <img src="https://latex.codecogs.com/gif.latex?x_{n+1}=x_n\cdot\hspace{0.1cm}P" />
- Computation of the stationary state distribution <img src="https://latex.codecogs.com/gif.latex?x_s=x_s\cdot\hspace{0.1cm}P" /> 
   - Initial state distribution <img src="https://latex.codecogs.com/gif.latex?x_0" /> 
   - Consecutive state distributions <img src="https://latex.codecogs.com/gif.latex?x_{n+1}=x_n\cdot\hspace{0.1cm}P" /> 

### Functional Specification of DTMCs

-   Functional specification
    -   States <img src="https://latex.codecogs.com/gif.latex?\mathcal{X}" /> 
        -   Initial state distribution <img src="https://latex.codecogs.com/gif.latex?x_0" /> 
    -   Factors <img src="https://latex.codecogs.com/gif.latex?\mathcal{Y}" /> 
        -   Factor distribution <img src="https://latex.codecogs.com/gif.latex?y" /> 
    -   State distribution function 
        -   <img src="https://latex.codecogs.com/gif.latex?f:(\mathcal{X},\mathcal{Y})\rightarrow\mathcal{X}" />
        -   Stochastic recursive equation    
-   Computation of consecutive states 
    <img src="https://latex.codecogs.com/gif.latex?X_{n+1}=f(X_n,Y)" /> 
- Computation of consecutive state distributions 
    - Forward algorithms
        - Input: <img src="https://latex.codecogs.com/gif.latex?\mathcal{X}" /> 
        - Output: 
            -  Consecutive state distribution <img src="https://latex.codecogs.com/gif.latex?x_{n+1}" /> 
                - Additional input <img src="https://latex.codecogs.com/gif.latex?x_n" /> 
                - State transition matrix <img src="https://latex.codecogs.com/gif.latex?P" />  not needed
            -  State transition matrix <img src="https://latex.codecogs.com/gif.latex?P" /> 
-   Advantages over conventional specification
    -   Intuitive modelling of complex systems with a possibly
        multidimensional state and factor space
    -   Simplified derivation of the transition matrix <img src="https://latex.codecogs.com/gif.latex?P" /> 
    -   Memory-efficient computation of consecutive state distributions


## The tool FunSpec4DTMC

- Python 3 library published under GPLv3
  - Simulation library 
  - Intuitive GUI for simplified use
  - 
  

- Multiple project tabs, analysis dialogues, and means for visualization
- Four phases of FunSpec4DTMC’s analysis process for DTMCs

![Analysis process](http://atlas.informatik.uni-tuebingen.de/git/hauserf/2017-Markov-Chains/raw/master/figures/structure.PNG)

### Computation Methods for the stationary state distribution

- Direct algorithms to calculate the stationary state distribution <img src="https://latex.codecogs.com/gif.latex?x_s" /> 
- Iterative algorithms to calculate the stationary state distribution  <img src="https://latex.codecogs.com/gif.latex?x_s" /> 
  - DTMC random walk 
      - simulation
  - Calculation of the limiting distribution  
      - <img src="https://latex.codecogs.com/gif.latex?$(\lim\limits_{n\rightarrow\infty}{x_n})$" />  
      - applicable to aperiodic DTMCs
  - Matrix powering 
      -  <img src="https://latex.codecogs.com/gif.latex?$(\lim\limits_{n\rightarrow\infty}{P^n})$" />  
      -  applicable to aperiodic DTMCs and to DTMCs with a period of  <img src="https://latex.codecogs.com/gif.latex?2^n,n\in\mathbb{N}_0" /> 
  - Calculation of the Cesaro limit 
      - <img src="https://latex.codecogs.com/gif.latex?$(\lim\limits_{n\rightarrow\infty}{1/(n+1)}\cdot\sum_{i=0}^{n}x_i})" /> 
  - Modified calculation of the Cesaro limit
      -  <img src="https://latex.codecogs.com/gif.latex?$(\lim\limits_{n\rightarrow\infty}{1/p\cdot\sum_{n\leq\text{}i\text{}n+p}x_i})" /> 
      -  analysis of transition structures to compute the period  <img src="https://latex.codecogs.com/gif.latex?P" /> 
    
## Implementation

- Object-oriented class hierarchy that leverages many design patterns
  - e. g.: model-view-controller, observer pattern, strategy pattern
- Minimum dependence on external libraries
  - NumPy for matrix multiplication and memory mapping
  - SciPy to use common distributions
  - Cython for runtime optimization
  - Matplotlib for figure plotting
  - NetworkX for graph visualization
  - PyQt5 for GUI programming

    


  