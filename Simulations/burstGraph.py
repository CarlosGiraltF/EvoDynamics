#-------------------------------------------------------------------------------------------------------------#
# Author: Carlos Giralt Fuixench
# Date: 29-3-24
# Version: release
# File: burstGraph.py
# Description: Evolutionary dynamics on a burst graph
# Notes: While networkx offers a graph constructor to create star-shaped graphs,
# this constructor doesn't offer the option of it being a directed graph, so 
# we'll have to create the graph manually
#-------------------------------------------------------------------------------------------------------------#

import networkx as nx
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation
from sys import argv
import numpy as np

def initialize_graph(N):
    G = nx.DiGraph()
    # central node
    G.add_node(0)

    # other nodes and edges
    for i in range(1, N):
        G.add_node(i)
        G.add_edge(0, i)
    
    # Position arrangement to make it look like a star
    positions = {0: (0, 0)}
    for i in range(1, N):
        angle = 2 * np.pi * i / (N-1)
        x = np.cos(angle)
        y = np.sin(angle)
        positions[i] = (x, y)
    
    return G, positions

def color_init(G, mutant_on_first):
    """
    Initializes the colors for nodes.
    Places the mutant ('red') at the first node or a random node.
    """
    node_colors = ['blue'] * len(G.nodes())
    mutant_node = 0 if mutant_on_first else random.choice(list(G.nodes()))
    node_colors[mutant_node] = 'red'
    # Initialize the state: 1 for mutant, 0 for normal
    state = {node: 1 if node == mutant_node else 0 for node in G.nodes()}
    return node_colors, state

def evolution_simulation(G, node_colors, state, mutation_rate):
    """
    Simulates reproduction dynamics based on fitness.
    Mutants have a fitness advantage specified by mutation_rate.
    """
    # Fitness: mutants (state=1) use mutation_rate, normals (state=0) use 1
    fitness = [mutation_rate if state[node] == 1 else 1 for node in G.nodes()]
    reproducing_node = random.choices(list(G.nodes()), weights=fitness, k=1)[0]

    neighbors = list(G.neighbors(reproducing_node))
    if not neighbors:  # Handle the case when there are no neighbors
        return reproducing_node

    dying_node = random.choice(neighbors)
    node_colors[dying_node] = node_colors[reproducing_node]
    state[dying_node] = state[reproducing_node]  # Update state
    return reproducing_node

def update(frame):
    """Updates the plot for each frame in the animation."""
    if int(frame) != 0:
        ax.clear()
        r_node = evolution_simulation(line_graph, node_colors, state, mutation_rate)
        nx.draw(line_graph, pos=pos, node_color=node_colors, ax=ax)
        
        # Add text above the graph
        ax.set_title(f'Step: {frame}', fontsize=14, pad=20)  # Display the step number in the title
        if r_node is not None:
            ax.text(0, 1.1, f'Node {r_node} reproduces', fontsize=12, transform=ax.transAxes, ha='center')
        
        # Stop the animation if convergence is reached
        if all(color == 'red' for color in node_colors) or all(color == 'blue' for color in node_colors):
            ani.event_source.stop()
    else:
        nx.draw(line_graph, pos=pos, node_color=node_colors, ax=ax)
        ax.set_title("Initial State", fontsize=14, pad=20)


if __name__ == '__main__':
    # Command-line arguments
    N = int(argv[1])  # Number of nodes
    mutation_rate = float(argv[2])  # Fitness value for mutants
    mutant_on_first = argv[3].lower() == 'true'  # True if mutant appears on the first node
    num_frames = 200

    # Initialize graph, colors, and state
    line_graph, pos = initialize_graph(N)
    node_colors, state = color_init(line_graph, mutant_on_first)

    # Set up the plot
    fig, ax = plt.subplots()
    ax.axis('off')

    ani = FuncAnimation(fig, update, frames=num_frames, interval=300, repeat=False)

    plt.show()
