#-------------------------------------------------------------------------------------------------------------#
# Author: Carlos Giralt Fuixench
# Date: 27-8-24
# Version: alpha
# File: probComputing.py
# Description: Computes the average fixation probability of a given graph.
#-------------------------------------------------------------------------------------------------------------#

import networkx as nx
import random
import numpy as np
from sys import argv

def moran_process(G, fitness):
    """
    Simulates the Moran process on a given graph G with a specified fitness value.
    
    Parameters:
    - G: networkx Graph
    - fitness: Fitness of the mutant type

    Returns:
    - 1 if the mutant type fixates, 0 if it goes extinct
    """
    # Randomly initialize one node as mutant (state 1) and the rest as non-mutant (state 0)
    state = {node: 0 for node in G.nodes}
    mutant_node = random.choice(list(G.nodes))
    state[mutant_node] = 1

    done = False
    
    while not done:
        # Count the number of mutants
        num_mutants = sum(state.values())
        
        # If all nodes are mutants, fixation occurs
        if num_mutants == len(G):
            done = True
            continue
        
        # If no mutants left, extinction occurs
        if num_mutants == 0:
            done = True
            continue
        
        # Selection step: Choose a node to reproduce proportionally to fitness
        fitnesses = [fitness if state[node] == 1 else 1 for node in G.nodes]
        reproducer = random.choices(list(G.nodes), weights=fitnesses, k=1)[0]
        
        # Reproduction step: Choose a neighbor to replace
        neighbor = random.choice(list(G.neighbors(reproducer)))
        state[neighbor] = state[reproducer]
    
    return 1 if sum(state.values()) == len(G) else 0

def average_fixation_probability(G, fitness=1.0, num_simulations=1000):
    """
    Computes the average fixation probability for a given graph G over multiple simulations.
    
    Parameters:
    - G: networkx Graph
    - fitness: Fitness of the mutant type (default: 1.0)
    - num_simulations: Number of simulations to run (default: 1000)
    
    Returns:
    - Average fixation probability
    """
    fixation_counts = 0
    
    for _ in range(num_simulations):
        fixation_counts += moran_process(G, fitness)
    
    return fixation_counts / num_simulations

G = nx.path_graph(10, create_using = nx.DiGraph)
G.add_edge(9,9)

# Create different graph structures
graphs = {
    #"complete_graph": nx.complete_graph(10),
    #"cycle_graph": nx.cycle_graph(10),
    "line_graph": G
}

# Imput data:
# argv[1] = fitness of mutant individuals 
# argv[2] = number of simulations

#fitness = float(argv[1])
#num_simulations = int(argv[2])

fitness = 4
num_simulations = 200000

# Compute average fixation probability for each graph
for name, graph in graphs.items():
    fixation_prob = average_fixation_probability(graph, fitness, num_simulations)
    print(f"{name}: {fixation_prob}")
