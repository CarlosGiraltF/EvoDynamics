#-------------------------------------------------------------------------------------------------------------#
# Author: Carlos Giralt Fuixench
# Date: 30-3-24
# Version: alpha
# File: FileParser.py
# Description: implements a variety of functions to deal with different input file formats
#-------------------------------------------------------------------------------------------------------------#
from sys import argv

def EdgesFileParser(file_path):
    with open(file_path, "r") as f:
        line = f.readline()
        edges = []
        while line:
            line = line[:-1]
            values = [int(_) for _ in line.split(" ")]
            edge = (values[0], values[1], values[2])
            edges.append(edge)
            line = f.readline()
    return edges


def AdjMatrixParser(file_path):
    with open(file_path, "r") as f:
        row = f.readline()
        edges = []
        while row:
            row = row[:-1]
            