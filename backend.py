#description: callSearchFunction returns 1 if solution exists, -1 if no solution exists, and +ve integer of depth only when IDDFS
#to get solution and visited list, call getter functions

from array import *
h_values = []

class SearchNode:
    def __init__(self, id, parent=None, path_cost=0, heu=0):
        self.id = id
        self.is_expanded = False
        self.parent = parent
        if self.parent == None:
            self.is_root = True
        else:
            self.is_root = False
        self.path_cost = path_cost
        self.heu = heu

class Tree:
    def __init__(self):
        self.nodes = []

    def create_node(self, SearchNode):
        self.nodes.append(SearchNode)

    def measureDepth(self, leaf, depth=0):
        if leaf.parent != None:
            depth += 1
            return self.measureDepth(leaf.parent, depth)
        return depth


solution = []
def findSolution(search_tree, goal):
    solution.insert(0, goal.id)
    if(goal.parent != None):
        findSolution(search_tree, goal.parent)

closed = []
def graphSearch(search_tag, graph, start, goal, depthLimit=99999):
    fringe = []
    search_tree = Tree()
    snode = SearchNode(id=start)
    search_tree.create_node(snode)
    fringe.append(snode)
    while True:
        if len(fringe) == 0: #no nodes to expand
            return -1

        if search_tag == 1: #change tag to choose the search alg
            node = BFS(fringe)
        elif search_tag == 2 or search_tag == 4: #DFS, depthlimited
            node = DFS(fringe)
        elif search_tag == 3:
            node = UCS(fringe)
        elif search_tag == 6:
            node = Greedy(fringe)
        elif search_tag == 7:
            node = Astar(fringe)
        else:
            return -1
        if node.id in goal: #goal found, print tree & fringe & findSolution & return '1' = solution found
            print("\nsearch_tree:")
            for i in range(len(search_tree.nodes)):
                nprint = search_tree.nodes[i]
                print("id=", nprint.id, "parent.id=", nprint.parent, "path_cost=", nprint.path_cost, "visited=",nprint.is_expanded)
            print("fringe:", fringe)

            findSolution(search_tree, node)
            return 1
        if node.id not in closed:
            # print("depth is now at:", search_tree.measureDepth(node))
            if search_tree.measureDepth(node) < int(depthLimit):
                closed.append(node.id)
                print("visited", node.id)
                node.is_expanded = True
                for child_node in graph[node.id]:
                    print("appending to fringe and tree", child_node[0])
                    cnode = SearchNode(id=child_node[0], parent=node, path_cost=child_node[1]+node.path_cost)
                    if(len(h_values) > 0):
                        cnode.heu=h_values[child_node[0]]
                    search_tree.create_node(cnode)
                    fringe.append(cnode)
        else:
            print("haha skipped:", node.id)
        fringe.remove(node)

def BFS(fringe):
    return fringe[0]

def DFS(fringe):
    return fringe[-1]

def UCS(fringe):
    min_pc_node = None
    min_pc = 99999
    for i in range(len(fringe)):
        if fringe[i].path_cost < min_pc:
            min_pc = fringe[i].path_cost
            min_pc_node = fringe[i]
    print("\nUCS returns node =", min_pc_node.id," & pc =", min_pc, "\n")
    return min_pc_node

def IDDFS(graph, start, goal):
    rows = cols = len(graph)
    IDDFS_solutions = [[0 for i in range(rows)] for j in range(cols)]
    for d in range(0,len(graph)):
        solution.clear()
        closed.clear()
        print("new iterative depth =", d)
        x = graphSearch(search_tag=2, graph=graph, start=start, goal=goal, depthLimit=d)
        if(x != -1):
            IDDFS_solutions[d] = solution.copy()
            print("finally, IDDFS solutions array")
            for i in IDDFS_solutions:
                print(i)
            return d
        else:
            IDDFS_solutions[d].clear()

def inputHeuristic(hList):
    for h in hList:
        h_values.append(h)

def Greedy(fringe):
    min_h_node = None
    min_h = 99999
    for i in range(len(fringe)):
        if fringe[i].heu < min_h:
            min_h = fringe[i].heu
            min_h_node = fringe[i]
    print("\nGreedy returns node =", min_h_node.id, " & heu =", min_h, "\n")
    return min_h_node

def Astar(fringe):
    min_f_node = None
    min_f = 99999
    for i in range(len(fringe)):
        temp_f = fringe[i].heu + fringe[i].path_cost
        if temp_f < min_f:
            min_f = temp_f
            min_f_node = fringe[i]
    print("\nA* returns node =", min_f_node.id, " & f =", min_f, "\n")
    return min_f_node


#graph = {
#    'S':[('A', 5), ('B', 9), ('D', 6)],
#    'A':[('B', 3), ('G1', 9)],
#    'B':[('A', 2), ('C', 1)],
#    'C':[('G2', 5), ('F', 7)],
#    'D':[('C', 2), ('E', 2)],
#    'E':[('G3', 7)],
#    'F':[('D', 2), ('G3', 8)],
#    'G1':[],
 #   'G2':[],
 #   'G3':[]
#}


def callSearch(search_tag, graph, start, goal, depthLimit=None, hList=None):
    solution.clear()
    closed.clear()
    if search_tag == 1 or search_tag == 2 or search_tag == 3: #BFS, DFS, UCS
        retval = graphSearch(search_tag, graph, start, goal)
    if search_tag == 4: #DLS
        retval = graphSearch(search_tag, graph, start, goal, depthLimit)
    if search_tag == 5: #IDDFS
        retval = IDDFS(graph, start, goal)
    if search_tag == 6 or search_tag == 7: #Greedy and A*
        inputHeuristic(hList)
        retval = graphSearch(search_tag, graph, start, goal)
    return retval

def getSolution():
    print("solution=", solution)
    return solution

def getVisited():
    print("visited=", closed)
    return closed

#graph = {
#0: [(1, 2), (2, 3), (4, 5)],
#1: [(3, 4)],
#2: [(4, 4)],
#3: [(4, 1), (5, 2)],
#4: [(5, 5)],
#5: []
#}


#EXAMPLE
"""graph = {
    0:[(1, 5), (2, 9), (4, 6)],
    1:[(2, 3), (7, 9)],
    2:[(1, 2), (3, 1)],
    3:[(8, 5), (6, 7), (0, 6)],
    4:[(3, 2), (5, 2), (0, 1)],
    5:[(9, 7)],
    6:[(4, 2), (9, 8)],
    7:[],
    8:[],
    9:[]
}
start=0
goal = set()
goal.add(7)
goal.add(8)
goal.add(9)
hList = [13, 8, 10, 19, 14, 100, 18, 0, 100, 100]
"""

"""EXAMPLE cont."""
#final test callSearch
#x = callSearch(search_tag=1or2or3, graph=graph, start=start, goal=goal)
#x = callSearch(search_tag=4, graph=graph, start=start, goal=goal, depthLimit=1)
#x = callSearch(search_tag=5, graph=graph, start=start, goal=goal)
#print("ans at depth=", x)
#x = callSearch(search_tag=6or7, graph=graph, start=start, goal=goal, hList=hList)
#print("solution exists? ans=", x)
#print("solution=",getSolution())
#print("visited=",getVisited())