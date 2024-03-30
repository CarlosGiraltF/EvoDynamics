#-------------------------------------------------------------------------------------------------------------#
# Author: Carlos Giralt Fuixench
# Date: 29-3-24
# Version: alpha
# File: trial.py
# Description: First time using networkx 
#-------------------------------------------------------------------------------------------------------------#

import networkx as nx
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation
from sys import argv

def initialize_graph(N):
    G = nx.path_graph(N, create_using = nx.DiGraph)
    G.add_edge(N-1,N-1)
    pos = [(i,0) for i in range(N)]
    return G, pos

def color_init(G):
    node_colors = ['blue']*len(G.nodes())
    return node_colors

def evolution_simulation(G, node_colors):
    reproducing_node = random.choice(list(G.nodes()))
    if reproducing_node < len(G.nodes()) - 1:
        node_colors[reproducing_node+1] = node_colors[reproducing_node]

def mutation(G, node_colors, mutation_rate):
    reproducing_node = random.choice(list(G.nodes()))
    mutant = random.random() < mutation_rate
    if mutant:
        node_colors[reproducing_node] = 'red'



def update(frame):
    ax.clear()
    evolution_simulation(line_graph, node_colors)
    mutation(line_graph, node_colors, mutation_rate)
    nx.draw(line_graph, pos=pos, node_color = node_colors, ax=ax)
    ax.text(0.1, 0.9, f'Step: {frame}', transform=ax.transAxes, fontsize=12)
    if all(color == 'red' for color in node_colors):
        ani.event_source.stop()


N = int(argv[1])
mutation_rate = float(argv[2]) 
num_frames = 200

line_graph, pos = initialize_graph(N)
node_colors = color_init(line_graph)

fig, ax = plt.subplots()
ax.axis('off')

ani = FuncAnimation(fig, update, frames=num_frames, interval = 1000, repeat = False)

plt.show()

