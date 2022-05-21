from backend import *
from tkinter import messagebox
from tkinter import ttk
from new import *


nodes = []
edges = []
heurist = []
i = 0


class Node:
    def __init__(self, canvas):
        self.canvas = canvas
        self.index = len(nodes)
        #TODO look this up: https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html?highlight=create_circle
        self.center_x = -1
        self.center_y = -1
        self.top = -1
        self.bottom = -1
        self.left = -1
        self.right = -1
        self.heuristic = -1 #flag

    def createNode(self, event):
        self.index = len(nodes)
        self.center_x = event.x
        self.center_y = event.y
        self.top = self.center_y - 20
        self.bottom = self.center_y + 20
        self.left = self.center_x - 20
        self.right = self.center_x + 20
        nodes.append(self)

    def drawNode(self):
        self.canvas.create_oval(self.center_x - 20, self.center_y - 20, self.center_x + 20,
                                self.center_y + 20,
                                fill="grey", width=3, outline="black", tags=str(self.index))
        self.canvas.create_text(self.center_x, self.center_y, font=("Arial", 12), text=str(self.index), tags="do_not_visit")


class Edge:
    def __init__(self, canvas, is_directed):
        self.canvas = canvas
        self.is_directed = is_directed
        self.arrow = "none"
        if is_directed == True: self.arrow = "last"
        self.start_x = -1
        self.start_y = -1
        self.end_x = -1
        self.end_y = -1
        self.start_node = nodes[0] #temp incorrect
        self.end_node = nodes[0]
        self.weight = 1

    def drawEdgeFrom(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if len(nodes) > 0:
            for node in nodes:
                if self.start_x >= node.left and self.start_x <= node.right and self.start_y >= node.top and self.start_y <= node.bottom:
                    print("valid, start edge from here, node @ ", node.index)
                    self.start_node = node
                    self.canvas.bind("<Button-1>", self.drawEdgeTo)

    def drawEdgeTo(self, event):
        self.end_x = event.x
        self.end_y = event.y
        if len(nodes) > 0:
            for node in nodes:
                if self.end_x >= node.left and self.end_x <= node.right and self.end_y >= node.top and self.end_y <= node.bottom:
                    print("valid, end edge here, node @ ", node.index)
                    self.end_node = node
                    if self.start_node == self.end_node: #bottomright to topright
                        self.canvas.create_line(self.start_node.right, self.start_node.bottom,
                                                self.start_node.right + 15, self.start_node.bottom,
                                                self.start_node.right + 15, self.start_node.top,
                                                self.start_node.right, self.start_node.top, fill="red",
                                                width=3, arrow=self.arrow, tags="do_not_visit")
                    else:
                        self.canvas.create_line(self.start_node.center_x, self.start_node.center_y,
                                            self.end_node.center_x, self.end_node.center_y, fill="red", width = 3,
                                            arrow=self.arrow, tags="do_not_visit")
                    self.createEdge()
                    self.canvas.bind("<Button-1>", app.addEdge)

    def createEdge(self):
        edges.append(self)
        if self.is_directed == False and self.start_node != self.end_node:
            undi_edge = Edge(self.canvas, False)
            undi_edge.start_x = self.end_x
            undi_edge.start_y = self.end_y
            undi_edge.end_x = self.start_x
            undi_edge.end_y = self.start_y
            undi_edge.start_node = self.end_node
            undi_edge.end_node = self.start_node
            undi_edge.weight = self.weight
            edges.append(undi_edge)


class AdjList:
    def __init__(self):
        self.graph = {}
        self.numOfV = 0

    def addVertexToList(self, vertex):
        self.numOfV = self.numOfV + 1
        self.graph[vertex] = []

    def addEdgeToList(self, vertex1, vertex2, weight):
        if vertex1 not in self.graph:
            print(vertex1, " doesn't exist")
        elif vertex2 not in self.graph:
            print(vertex2, " doesn't exist")
        else:
            temp = [vertex2, weight]
            self.graph[vertex1].append(temp)
            print("directed edge added")

    def printGraph(self):
        for v in self.graph:
            for e in self.graph[v]:
                print(v, " -> ", e[0], " edge weight: ", e[1])


    def createAdjList(self):
        for node in nodes:
            self.addVertexToList(node.index)
        for edge in edges:
            self.addEdgeToList(edge.start_node.index, edge.end_node.index, edge.weight)


class App:
    def __init__(self):
        self.adding_nodes_state = False
        self.adding_edges_state = False
        self.is_directed = False
        self.start_node = -1
        self.goal_nodes = set()

        self.canvas = Canvas(root, height=700, width=1000, bg="white")
        self.canvas.grid(sticky=NW, padx=10, pady=10)
        self.side_frame = Frame(root)
        self.side_frame.grid(row=0, column=1, sticky=NW)

        self.btns_frame = Frame(self.side_frame)
        self.btns_frame.grid(row=0, column=0, sticky=NW)
        self.add_nodes_btn = Button(self.btns_frame, text="Add nodes")
        self.add_nodes_btn.bind("<Button-1>", self.startAddNodes)
        self.add_nodes_btn.grid(row=0, column=0, sticky=NW, pady=15)
        self.add_directed_btn = Button(self.btns_frame, text="Add directed edges")
        self.add_directed_btn.bind("<Button-1>", self.startAddDirected)
        self.add_directed_btn.grid(row=1, column=0, sticky=NW)
        self.add_undirected_btn = Button(self.btns_frame, text="Add undirected edges")
        self.add_undirected_btn.bind("<Button-1>", self.startAddUndirected)
        self.add_undirected_btn.grid(row=2, column=0, sticky=NW)

        self.btns_frame2 = Frame(self.side_frame, pady=10)
        self.btns_frame2.grid(row=0, column=1, sticky = NW)
        self.start_node_btn = Button(self.btns_frame2, text="Select start node")
        self.goal_nodes_btn = Button(self.btns_frame2, text="Select goal nodes")
        self.start_node_btn.bind("<Button-1>", self.setStart)
        self.goal_nodes_btn.bind("<Button-1>", self.setGoals)
        self.start_node_btn.grid(row=0, column=0)
        self.goal_nodes_btn.grid(row=0, column=1)

        self.weight_frame = Frame(self.side_frame, pady=50)
        self.weight_frame.grid(row=1,column=0,sticky=NW)
        self.weight_instr1 = Label(self.weight_frame, text="Weight From:", pady=5)
        self.weight_instr1.grid(row=0, column=0, sticky=NE)
        self.weight_instr2 = Label(self.weight_frame, text="To:", pady=5)
        self.weight_instr2.grid(row=1, column=0, sticky=NE)
        self.weight_instr3 = Label(self.weight_frame, text="Value:", pady=5)
        self.weight_instr3.grid(row=2, column=0, sticky=NE)
        self.weight_from = Entry(self.weight_frame, borderwidth=3, width=5)
        self.weight_to = Entry(self.weight_frame, borderwidth=3, width=5)
        self.weight_val = Entry(self.weight_frame, borderwidth=3, width=10)
        self.weight_from.grid(row=0, column =1, sticky=NW)
        self.weight_to.grid(row = 1, column =1,sticky=NW)
        self.weight_val.grid(row=2,column=1, sticky=NW)
        self.add_weight_btn = Button(self.weight_frame, text="Add weight")
        self.add_weight_btn.bind("<Button-1>", self.addWeight)
        self.add_weight_btn.grid(row=4, column=1, sticky=NW)

        self.heur_frame = Frame(self.side_frame, pady=50)
        self.heur_frame.grid(row=1, column=1, sticky=NE)
        self.heur_instr = Label(self.heur_frame, text="Node:", pady=5)
        self.heur_instr.grid(row=0, column=0, sticky=NE)
        self.heur_node = Entry(self.heur_frame, borderwidth=3, width=5)
        self.heur_node.grid(row=0, column=1, sticky=NW)
        self.heur_instr = Label(self.heur_frame, text="Heuristic:", pady=5)
        self.heur_instr.grid(row=1, column=0, sticky=NE)
        self.heur_val = Entry(self.heur_frame, borderwidth=3, width=5)
        self.heur_val.grid(row=1, column=1, sticky=NW)
        self.add_heur_btn = Button(self.heur_frame, text="Add heuristic")
        self.add_heur_btn.bind("<Button-1>", self.changeHeuristic)
        self.add_heur_btn.grid(row=2, column=1, sticky=NE)

        self.combobox_frame = Frame(self.side_frame, pady=10)
        self.combobox_frame.grid(row=3, column=0)
        self.search_algs_options = [
            "Choose search algorithm", "BFS", "DFS", "UCS", "DLS", "IDDFS", "Greedy", "A*"
        ]
        self.search_algs_combobox = ttk.Combobox(self.combobox_frame, width=30, values=self.search_algs_options)
        self.search_algs_combobox.current(0)
        self.search_algs_combobox.grid(row=0, column=0, sticky=NE)
        self.depthLimit_instr = Label(self.combobox_frame, text="DLS depth limit:")
        self.depthLimit_instr.grid(row=1, column=0, sticky=NW, pady=10)
        self.depthLimit = Entry(self.combobox_frame, borderwidth=3, width=15)
        self.depthLimit.grid(row=1, column=0, sticky=NE, pady=10)
        self.search_btn = Button(self.combobox_frame, text="Search")
        self.search_btn.grid(pady=10, sticky=NW)
        self.search_btn.bind("<Button-1>", self.handleErrors)

    def changeHeuristic(self, event):
        nodes[int(self.heur_node.get())].heuristic = int(self.heur_val.get())
        for node in nodes:
            print("node #", node.index, " heuristic = ", node.heuristic)

    def handleErrors(self, event):
        if self.start_node == -1 or len(self.goal_nodes) == 0:
            messagebox.showerror("Missing Start or Goal Nodes", "Please select start/goal nodes")
            return
        if (self.search_algs_combobox.get() == "Greedy" or self.search_algs_combobox.get() == "A*") and len(nodes) > 0:
            for node in nodes:
                if node.heuristic < 0:
                    messagebox.showerror("Incomplete/False Heuristics","Cannot perform informed search")
                    return
        if self.search_algs_combobox.get() == "DLS":
            try:
                int(self.depthLimit.get())
            except:
                messagebox.showerror("Missing Depth limit", "Please enter valid depth limit")
                return
        if self.search_algs_combobox.get() == "Choose search algorithm":
            messagebox.showerror("Unknown Search Algorithm", "Please select an algorithm to use for graph search")
            return
        print("launching search window...")
        self.startSearchWindow(event)

    def setStart(self, event):
        print("start")
        self.start_node_btn.configure(bg="blue")
        self.setStartID = self.canvas.bind("<Button-1>", self.chooseStart)
        self.start_node_btn.bind("<Button-1>", self.endSetStart)

    def chooseStart(self, event):
        for node in nodes:
            if event.x >= node.left and event.x <= node.right and event.y >= node.top and event.y <= node.bottom:
                self.start_node = node.index
        print(self.start_node)

    def endSetStart(self,event):
        self.start_node_btn.configure(bg="SystemButtonFace")
        self.canvas.unbind("<Button-1>", self.setStartID)
        self.start_node_btn.bind("<Button-1>", self.setStart)

    def setGoals(self, event):
        print("goals")
        self.goal_nodes.clear()
        self.goal_nodes_btn.configure(bg="green")
        self.setGoalsID = self.canvas.bind("<Button-1>", self.chooseGoals)
        self.goal_nodes_btn.bind("<Button-1>", self.endSetGoals)

    def chooseGoals(self, event):
        for node in nodes:
            if event.x >= node.left and event.x <= node.right and event.y >= node.top and event.y <= node.bottom:
                self.goal_nodes.add(node.index)
        print (self.goal_nodes)

    def endSetGoals(self,event):
        self.goal_nodes_btn.configure(bg="SystemButtonFace")
        self.canvas.unbind("<Button-1>", self.setGoalsID)
        self.goal_nodes_btn.bind("<Button-1>", self.setGoals)

    def addWeight(self, event):
        if self.weight_from.get().isnumeric() and self.weight_to.get().isnumeric() and self.weight_val.get().isnumeric():
            print("ok")
            for edge in edges:
                if self.is_directed == False and edge.start_node != edge.end_node:
                    if edge.start_node.index == int(self.weight_to.get()) and edge.end_node.index == int(self.weight_from.get()):
                        edge.weight = int(self.weight_val.get())
                if edge.start_node.index == int(self.weight_from.get()) and edge.end_node.index == int(self.weight_to.get()):
                    edge.weight = int(self.weight_val.get())
                    if edge.start_node == edge.end_node: #self-directed edge weight
                        weight_x = edge.start_node.right + 15
                        weight_y = (edge.start_node.top + edge.start_node.bottom) / 2
                    else:
                        weight_x = (edge.start_node.center_x + edge.end_node.center_x)/2
                        weight_y = (edge.start_node.center_y + edge.end_node.center_y)/2
                    self.canvas.create_rectangle(weight_x-10, weight_y-10, weight_x+10, weight_y+10, fill="yellow", outline="red",
                                                 tags="do_not_visit")
                    self.canvas.create_text(weight_x, weight_y, font=("Arial", 10), text=str(self.weight_val.get()), tags="do_not_visit")
                    print("weight drawn")
                print("edge weight = ", edge.weight)

    def startAddNodes(self, event):
        print("start adding nodes...")
        self.adding_nodes_state = True
        self.add_nodes_btn.configure(bg="grey")
        self.node_addID = self.canvas.bind("<Button-1>", self.addNode)
        self.add_nodes_btn.bind("<Button-1>", self.endAddNodes)

    def addNode(self, event):
        self.new_node = Node(self.canvas)
        self.new_node.createNode(event)
        self.new_node.drawNode()

    def endAddNodes(self, event):
        print("end nodes!")
        self.adding_nodes_state = False
        self.add_nodes_btn.configure(bg='SystemButtonFace')
        self.canvas.unbind("<Button-1>", self.node_addID)
        self.add_nodes_btn.bind("<Button-1>", self.startAddNodes)
        for node in nodes:
            print("node #", node.index, " center=(", node.center_x, ",",
              node.center_y, ")", " top=", node.top, " bottom=", node.bottom,
              " left=", node.left, " right=", node.right)

    def startAddDirected(self, event):
        print("start adding directed...")
        self.adding_edges_state = True
        self.add_directed_btn.configure(bg="grey")
        if len(edges) != 0 and self.is_directed == False:
            pass
        else:
            self.is_directed = True
            self.node1_edge_addID = self.canvas.bind("<Button-1>", self.addEdge)
        self.add_directed_btn.bind("<Button-1>", self.endAddDirected)

    def addEdge(self, event):
        self.new_di_edge = Edge(self.canvas, self.is_directed).drawEdgeFrom(event)
        #when we draw one edge, then set is_directed = True and do not allow to startAddUndirected

    def endAddDirected(self, event):
        print("end directed edges!")
        self.adding_edges_state = False
        self.canvas.unbind("<Button-1>", '')
        self.add_directed_btn.configure(bg='SystemButtonFace')
        self.add_directed_btn.bind("<Button-1>", self.startAddDirected)
        print("len(edges) = ", len(edges))
        for edge in edges:
            print("(", edge.start_node.center_x,"," ,edge.start_node.center_y, ") -> ",
                  "(", edge.end_node.center_x,"," ,edge.end_node.center_y, ")", edge.is_directed)

    def startAddUndirected(self, event):
        print("start adding undirected...")
        self.adding_edges_state = True
        self.add_undirected_btn.configure(bg="grey")
        if len(edges) != 0 and self.is_directed == True:
            pass
        else:
            self.is_directed = False
            self.node1_edge_addID = self.canvas.bind("<Button-1>", self.addEdge)
        self.add_undirected_btn.bind("<Button-1>", self.endAddUndirected)

    def endAddUndirected(self, event):
        print("end directed edges!")
        self.adding_edges_state = False
        self.canvas.unbind("<Button-1>", '')
        self.add_undirected_btn.configure(bg='SystemButtonFace')
        self.add_undirected_btn.bind("<Button-1>", self.startAddUndirected)
        print("len(edges) = ", len(edges))
        for edge in edges:
            print("(", edge.start_node.center_x, ",", edge.start_node.center_y, ") -> ",
                  "(", edge.end_node.center_x, ",", edge.end_node.center_y, ")", edge.is_directed)

    def createHeuristicList(self):
        for node in nodes:
            heurist.append(node.heuristic)

    #old output code
    """
    def turnBlue(self, canvas, visitedNodes, visited, counter, step):
        if step < counter:
            canvas.itemconfig(visitedNodes[visited[step]], fill='blue')
            canvas.after(500, self.turnBlue, canvas, visitedNodes, visited, counter, step + 1)

    def turnGreen(self, canvas, solutionNodes, solution, counter, step):
        if step < counter:
            canvas.itemconfig(solutionNodes[solution[step]], fill='green')
            canvas.after(500, self.turnGreen, canvas, solutionNodes, solution, counter, step + 1)

    def displayResults(self, searchType, visited, solution):
        counterVis = 0
        counterSol = 0
        top = Toplevel()
        top.title(searchType)
        top.geometry("1500x750")
        visitedNodes = []
        solutionNodes = []
        canvas = Canvas(top, height=700, width=1000, bg="white")
        for node in nodes:
            x = canvas.create_oval(node.center_x - 20, node.center_y - 20, node.center_x + 20, node.center_y + 20, fill="grey", width=3, outline="black")
            canvas.create_text(node.center_x, node.center_y, font=("Arial", 12), text=str(node.index))
            if node.index in visited:
                visitedNodes.append(x)
                counterVis += 1
            if node.index in solution:
                solutionNodes.append(x)
                counterSol += 1
        for edge in edges:
            if edge.start_node == edge.end_node:  # bottomright to topright
                edge.canvas.create_line(edge.start_node.right, edge.start_node.bottom,
                                        edge.start_node.right + 15, edge.start_node.bottom,
                                        edge.start_node.right + 15, edge.start_node.top,
                                        edge.start_node.right, edge.start_node.top, fill="red",
                                        width=3, arrow=edge.arrow)
            else:
                edge.canvas.create_line(edge.start_node.center_x, edge.start_node.center_y,
                                        edge.end_node.center_x, edge.end_node.center_y, fill="red", width=3,
                                        arrow=edge.arrow)
        canvas.grid(sticky=NW, padx=10, pady=10)
        startButton = Button(top, text="Start Search")
        startButton.bind("<Button-1>", self.turnBlue(canvas, visitedNodes, visited, counterVis, 0))
        startButton.bind("<Button-1>", self.turnGreen(canvas, solutionNodes, solution, counterSol, 0), '+')
        startButton.grid(row=1, column=1,sticky=NW)

    def checkCheckBoxes(self):
        #if app.c1var.get() == 1: #BFS
         #   x = callSearch(1, app.list.graph, app.start_node, app.goal_nodes)
          #  if x == 1:
           #     title_window = "BFS"
            #    self.displayResults(title_window, getVisited(), getSolution())
        #if app.c2var.get() == 1: #DFS
         #   x = callSearch(2, app.list.graph, app.start_node, app.goal_nodes)
          #  if x == 1:
           #     title_window = "DFS"
            #    self.displayResults(title_window, getVisited(), getSolution())
        #if app.c3var.get() == 1: #UCS
            #x = callSearch(3, app.list.graph, app.start_node, app.goal_nodes)
           # if x == 1:
              #  title_window = "UCS"
             #   self.displayResults(title_window, getVisited(), getSolution())
        if app.c4var.get() == 1: # iterative deepening
            x = callSearch(5, app.list.graph, app.start_node, app.goal_nodes)
            if x == 1:
                title_window = "IDDFS"
                self.displayResults(title_window, getVisited(), getSolution())
        if app.c5var.get() == 1: #Greedy
            x = callSearch(6, app.list.graph, app.start_node, app.goal_nodes, hList=heurist)
            if x == 1:
                title_window = "Greedy"
                self.displayResults(title_window, getVisited(), getSolution())
        if app.c6var.get() == 1: #Astar
            x = callSearch(7, app.list.graph, app.start_node, app.goal_nodes, hList=heurist)
            if x == 1:
                title_window = "A*"
                self.displayResults(title_window, getVisited(), getSolution())
        if app.c7var.get() == 1: #depth limited
            if app.depthLimit.get().isnumeric() == False:
                messagebox.showerror("Missing Depth limit", "Please enter depth limit")
            x = callSearch(4, app.list.graph, app.start_node, app.goal_nodes, int(app.depthLimit.get()))
            if x == 1:
                title_window = "DLS"
                self.displayResults(title_window, getVisited(), getSolution())

    

    def startSearchWindow(self, event):
        self.list = AdjList()
        self.list.createAdjList()
        #self.list.printGraph()
        self.createHeuristicList()
        for h in heurist:
            print(h)

        if self.start_node == -1 or len(self.goal_nodes) == 0:
            messagebox.showerror("Missing Start or Goal Nodes", "Please select start/goal nodes")
        else:
            self.checkCheckBoxes()
    """

    def startSearchWindow(self, event):
        self.adjList = AdjList()
        self.adjList.createAdjList()
        self.createHeuristicList()

        #calc solution and visited
        self.search_option = self.search_algs_combobox.current()
        #print("search_tag!!!", self.search_option)
        if self.search_algs_combobox.get() == "BFS" or self.search_algs_combobox.get() == "DFS" or self.search_algs_combobox.get() == "UCS" or self.search_algs_combobox.get() == "IDDFS":
            x = callSearch(self.search_option, self.adjList.graph, self.start_node, self.goal_nodes)
        elif self.search_algs_combobox.get() == "DLS":
            x = callSearch(self.search_option, self.adjList.graph, self.start_node, self.goal_nodes, int(self.depthLimit.get()))
        else:#elif self.search_algs_combobox.get() == "Greedy" or self.search_algs_combobox.get() == "A*":
            x = callSearch(self.search_option, self.adjList.graph, self.start_node, self.goal_nodes, hList=heurist)

        #call window to draw the solution and visited
        if x > 0: #meaning, solution exists/ depth returned from IDDFS
            self.output_win = SearchWindow(title=self.search_algs_combobox.get(), nodes=nodes,
                                edges=edges, solution=getSolution(), visited=getVisited())
            self.output_win.drawWindow()


if __name__ == "__main__":
    root = Tk()
    root.geometry("1500x750")
    #root.attributes('-fullscreen', True)
    app = App()
    root.mainloop()