# Python3 Program to print BFS traversal
# from a given source vertex. BFS(int s)
# traverses vertices reachable from s.
"""from collections import defaultdict


# This class represents a directed graph
# using adjacency list representation
class Graph:

    # Constructor
    def __init__(self):

        # default dictionary to store graph
        self.graph = defaultdict(list)

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # Function to print a BFS of graph
    def BFS(self, s):

        # Mark all the vertices as not visited
        visited = [False] * (len(self.graph))

        # Create a queue for BFS
        queue = []

        # Mark the source node as
        # visited and enqueue it
        queue.append(s)
        visited[s] = True

        while queue:

            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            print(s, end=" ")

            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True


# Driver code

# Create a graph given in
# the above diagram
g = Graph()
print("Enter number of edges")
a = int(input())
print("Enter edges")
#for i in range(a)
#    g.addEdge(int(input()), int(input())
#g.addEdge(0, 1)
#g.addEdge(0, 2)
#g.addEdge(1, 2)
#g.addEdge(2, 0)
#g.addEdge(2, 3)
#g.addEdge(3, 3)

print("Following is Breadth First Traversal"
      " (starting from vertex 2)")
g.BFS(2)

# This code is contributed by Neelam Yadav"""

# Using a Python dictionary to act as an adjacency list
"""graph = {
  '5' : ['3','7'],
  '3' : ['2', '4'],
  '7' : ['8'],
  '2' : [],
  '4' : ['8'],
  '8' : []
}

visited = set() # Set to keep track of visited nodes of graph.

def dfs(visited, graph, node):  #function for dfs
    if node not in visited:
        print ("not in visited:" node " ")
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

# Driver Code
print("Following is the Depth-First Search")
dfs(visited, graph, 4)"""


# adjacency list representation
adj_list = {}
mylist = []


def add_node(node):
    if node not in mylist:
        mylist.append(node)
    else:
        print("Node ", node, " already exists!")


def add_edge(node1, node2, weight):
    temp = []
    if node1 in mylist and node2 in mylist:
        if node1 not in adj_list:
            temp.append([node2, weight])
            adj_list[node1] = temp

        elif node1 in adj_list:
            temp.extend(adj_list[node1])
            temp.append([node2, weight])
            adj_list[node1] = temp

    else:
        print("Nodes don't exist!")


def graph():
    for node in adj_list:
        print(node, " ---> ", [i for i in adj_list[node]])


# Adding nodes
add_node(0)
add_node(1)
add_node(2)
add_node(3)
add_node(4)
# Adding edges
add_edge(0, 1, 2)
add_edge(1, 2, 2)
add_edge(2, 3, 4)
add_edge(3, 0, 5)
add_edge(3, 4, 3)
add_edge(4, 0, 1)

# Printing the graph
graph()

# Printing the adjacency list
print(adj_list)