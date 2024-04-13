#-------------------------------------------------------------------------------------------------------------#
# Author: Carlos Giralt Fuixench
# Date: 29-3-24
# Version: alpha
# File: trial.py
# Description: Evolutionay dynamics on a burst graph
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


def evolution_simulation(G, node_colors):
    reproducing_node = random.choice(list(G.nodes()))
    if reproducing_node == 0:
        child_node = random.choice(list(G.neighbors(reproducing_node)))
        node_colors[child_node] = node_colors[reproducing_node]
    return reproducing_node


def mutation(G, node_colors, mutation_rate):
    mutation_node = random.choice(list(G.nodes()))
    mutant = random.random() <= mutation_rate
    if mutant and node_colors[mutation_node] != 'red':
        node_colors[mutation_node] = 'red'
        return mutation_node
    return None


def update(frame):
    if int(frame) != 0:
        ax.clear()
        r_node = evolution_simulation(graph, node_colors)
        if r_node != None:
            ax.text(0.80, 1.0, f'Node {r_node} reproduces', transform=ax.transAxes, fontsize=12)
        node = mutation(graph, node_colors, mutation_rate)
        if node != None:
            ax.text(0.40, 1.0, f'Node {node} becomes mutant', transform=ax.transAxes, fontsize=12)
        nx.draw(graph, pos=pos, node_color = node_colors, ax=ax)
        ax.text(0.1, 1.0, f'Step: {frame}', transform=ax.transAxes, fontsize=12)
        if all(color == 'red' for color in node_colors):
            ani.event_source.stop()
    else:
        nx.draw(graph, pos=pos, node_color = node_colors, ax=ax)

N = int(argv[1])
mutation_rate = float(argv[2])
num_frames = 200

graph, pos = initialize_graph(N)
node_colors = ['blue']*len(graph.nodes())

fig, ax = plt.subplots()

ax.axis('off')

ani = FuncAnimation(fig, update, frames = num_frames, interval = 1.5*10**3, repeat = False)

plt.tight_layout(pad=4.0)
plt.show()