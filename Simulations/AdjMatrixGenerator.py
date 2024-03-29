from sys import argv

def lineGraph(n):
    with open("line.txt", "w") as f:
        for i in range(n):
            if i != n - 1:
                f.write(f"{i} {i+1} 1\n")
            else:
                f.write(f"{i} {i} 1\n")



if argv[1] == "line":
    lineGraph(int(argv[2]))
else:
    print("menudo gilipollas")