#-------------------------------------------------------------------------------------------------------------#
# Author: Carlos Giralt Fuixench
# Date: 16-11-24
# Version: release
# File: probComputing.py
# Description: Computes the average fixation probability of a given graph and plots results.
#-------------------------------------------------------------------------------------------------------------#

import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import sys

numSimulations = 100000

def fixSupressorGraph(size):
    K = nx.complete_graph(size, create_using=nx.DiGraph)
    C = nx.cycle_graph(size, create_using=nx.DiGraph)
    # Step 2: Combine the graphs
    G = nx.disjoint_union(C, K)

    # Step 3: Add a single edge connecting the two graphs
    G.add_edge(0, size)  # Connect a node from K (e.g., node 0) to a node in C (e.g., node n)

    #nx.draw(G)
    #plt.show()

    return G 

def galanisGraph():
    # Define the weight matrix
    W = [
        [0, 1/4, 3/4],
        [1/4, 0, 3/4],
        [1/2, 1/2, 0]
    ]

    # Create a directed graph
    G = nx.DiGraph()

    # Add weighted edges based on the weight matrix
    for i in range(len(W)):
        for j in range(len(W[i])):
            if W[i][j] != 0:  # Only add an edge if the weight is non-zero
                G.add_edge(i, j, weight=W[i][j])

    return G



def generateGraphs(size):
    # Define different graph structures
    lineG = nx.path_graph(size, create_using=nx.DiGraph)
    lineG.add_edge(int(size) - 1, int(size) - 1)

    supressorG = fixSupressorGraph(size)
    
    

    graphs = {
    "complete_graph": nx.complete_graph(size),
    "cycle_graph": nx.cycle_graph(size),
    "line_graph": lineG,
    "star_graph": nx.star_graph(size),
    "fixation_supressor": supressorG,
    "galanis_graph": galanisGraph()
    }

    return graphs


def plotByFitness(size, minF, maxF, step):
    graphs = generateGraphs(size)
    fitness_values = np.arange(minF, maxF, step)
    for name, graph in graphs.items():
        fixation_probs = []
        for fitness in fitness_values:
            fixation_prob = average_fixation_probability(graph, fitness, numSimulations)
            fixation_probs.append(fixation_prob)
            #print(f"Graph: {name}, Fitness: {fitness}, Fixation Probability: {fixation_prob}")
    
        # Plot fixation probability as a function of fitness
        plt.figure()
        plt.plot(fitness_values, fixation_probs, marker='o', linestyle='-', color='b')
        plt.xlabel("Fitness")
        plt.ylabel("Fixation Probability")
        plt.ylim(0, 1)
        plt.grid(True)
        plt.savefig(f"{name}_fixation_probability.png")  # Save each plot as a PNG file
        plt.show()


def plotByPopulationSize(minSize, maxSize, step, fitness):
    """
    Plots fixation probability as a function of population size for various graph types.
    
    Parameters:
    - minSize: Minimum size of the graph (integer)
    - maxSize: Maximum size of the graph (integer, exclusive in range)
    - step: Step size to increase the graph size (integer)
    - fitness: Fitness of the mutant type (float)
    """
    population_sizes = np.arange(minSize, maxSize, step)
    
    # Dictionary to store fixation probabilities for each graph type across sizes
    fixation_probs_by_graph = {name: [] for name in ["complete_graph", "cycle_graph", "line_graph", "star_graph", "fixation_supressor"]}
    
    for size in population_sizes:
        # Generate graphs for the current size
        graphs = generateGraphs(size)
        
        for name, graph in graphs.items():
            if name != "galanis_graph":
                # Compute fixation probability for the current graph, size, and fitness
                fixation_prob = average_fixation_probability(graph, fitness, numSimulations)
                fixation_probs_by_graph[name].append(fixation_prob)
                #print(f"Graph: {name}, Size: {size}, Fitness: {fitness}, Fixation Probability: {fixation_prob}")
    
    # Plot fixation probability as a function of population size for each graph type
    for name, fixation_probs in fixation_probs_by_graph.items():
        plt.figure()
        plt.plot(population_sizes, fixation_probs, marker='o', linestyle='-', color='b')
        plt.xlabel("Population Size")
        plt.ylabel("Fixation Probability")
        #plt.title(f"{name} (Fitness: {fitness})")
        plt.grid(True)
        plt.savefig(f"{name}_population_size_fixation_probability.png")  # Save each plot as a PNG file
        plt.show()


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

    # to avoid infinite loops or computational costs that are extremely high
    # this can be deleted if the computer used has a fast CPU or you don't have
    # a time limitation to simulate the whole process
    iter = 0
    
    while not done and iter < 50**4:
        # Count the number of mutants
        num_mutants = sum(state.values())
        
        # If all nodes are mutants, fixation occurs
        if num_mutants == len(G):
            done = True
            continue
        
        # If no mutants left, extinction occurs
        elif num_mutants == 0:
            done = True
            continue
        
        # Selection step: Choose a node to reproduce proportionally to fitness
        fitnesses = [fitness if state[node] == 1 else 1 for node in G.nodes]
        reproducer = random.choices(list(G.nodes), weights=fitnesses, k=1)[0]
        
        neighbors = list(G.neighbors(reproducer))
        weights = [G[reproducer][neighbor].get('weight', 1/len(G.nodes)) for neighbor in neighbors]
        replaced = random.choices(neighbors, weights=weights, k=1)[0]
        state[replaced] = state[reproducer]
        iter += 1
    
    return 1 if sum(state.values()) == len(G) else 0

# it runs 1000 iterations by default, but this value can be modified
# the macro numSimulations is stablished at the begining of the file and 
# is equal to 100000
def average_fixation_probability(G, fitness=1.0, num_simulations=1000):
    """
    Computes the average fixation probability for a given graph G over multiple simulations.
    
    Parameters:
    - G: networkx Graph
    - fitness: Fitness of the mutant type (default: 1.0)
    - num_simulations: Number of simulations to run (default: 100000)
    
    Returns:
    - Average fixation probability
    """
    fixation_counts = 0
    
    for _ in range(num_simulations):
        fixation_counts += moran_process(G, fitness)
    
    return fixation_counts / num_simulations

if __name__ == '__main__':
    if (sys.argv[1] == '-fitnessPlot'):
        size = int(sys.argv[2])
        minF = float(sys.argv[3])
        maxF = float(sys.argv[4])
        step = float(sys.argv[5])
        plotByFitness(size, minF, maxF, step)
    
    elif (sys.argv[1] == '-sizePlot'):
        minSize = int(sys.argv[2])
        maxSize = int(sys.argv[3])
        step = int(sys.argv[4])
        fitness = float(sys.argv[5])
        plotByPopulationSize(minSize, maxSize, step, fitness)
    
    elif (sys.argv[1] == '-counterExampleProb'):
        fitness = int(sys.argv[2])
        G = galanisGraph()
        avg_fix_prob = average_fixation_probability(G, fitness, numSimulations)
        print(f"The average fixation probability of the graph is {avg_fix_prob}")

    elif (sys.argv[1] == '-sup'):
        size = int(sys.argv[2])
        fitness = float(sys.argv[3])
        G = fixSupressorGraph(size)
        avg_fix_prob = average_fixation_probability(G, fitness, numSimulations)
        print(f"The average fixation probability of the graph is {avg_fix_prob}")

        

