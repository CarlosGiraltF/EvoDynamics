from sys import argv

def FileToEdgeList(file_path):
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