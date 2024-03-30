#-------------------------------------------------------------------------------------------------------------#
# Author: Carlos Giralt Fuixench
# Date: 29-3-24
# Version: alpha
# File: trial.py
# Description: First time using networkx 
#-------------------------------------------------------------------------------------------------------------#

import networkx as nx
import matplotlib.pyplot as plt

from FileParser import EdgesFileParser


def generateGraphFromFile(file_path):
    edges = EdgesFileParser(file_path)
    DG = nx.DiGraph()
    DG.add_weighted_edges_from(edges)
    return DG


graph = generateGraphFromFile("line.txt")
print(graph.edges())
pos = {0:[0,2],1:[1,2],2:[2,2],3:[3,2],4:[4,2]}
nx.draw(graph, pos = pos)
print("hellooo")

# Show the plot in the center of the screen
plt.gca().set_position([0.1, 0.1, 0.8, 0.8])  # Adjust the position based on your preference

plt.plot()
plt.show()





