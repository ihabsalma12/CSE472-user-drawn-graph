import sys
from pprint import pprint
from tkinter import *
import tkinter
from tkinter import messagebox

nodes = []
edges = []

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
                                fill="grey", width=3, outline="black")
        self.canvas.create_text(self.center_x, self.center_y, font=("Arial", 12), text=str(self.index))


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
                                                width=3, arrow=self.arrow)
                    else:
                        self.canvas.create_line(self.start_node.center_x, self.start_node.center_y,
                                            self.end_node.center_x, self.end_node.center_y, fill="red", width = 3,
                                            arrow=self.arrow)
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

        self.checkbox_frame = Frame(self.side_frame, pady=10)
        self.checkbox_frame.grid(row=3, column=0)
        self.c1var = IntVar()
        self.c2var = IntVar()
        self.c3var = IntVar()
        self.c4var = IntVar()
        self.c5var = IntVar()
        self.c6var = IntVar()
        c1 = Checkbutton(self.checkbox_frame, text="BFS", onvalue = 1, offvalue = 0, variable=self.c1var).grid(row=0, column=0, sticky=NW)
        c2 = Checkbutton(self.checkbox_frame, text="DFS", onvalue = 1, offvalue = 0, variable=self.c2var).grid(row=1, column=0, sticky=NW)
        c3 = Checkbutton(self.checkbox_frame, text="Uniform Cost", onvalue = 1, offvalue = 0, variable=self.c3var).grid(row=2, column=0, sticky=NW)
        c4 = Checkbutton(self.checkbox_frame, text="Iterative Deepening", onvalue = 1, offvalue = 0, variable=self.c4var).grid(row=2, column=0, sticky=NW)
        c5 = Checkbutton(self.checkbox_frame, text="Greedy", onvalue = 1, offvalue = 0, variable=self.c5var).grid(row=0, column=1, sticky=NW)
        c6 = Checkbutton(self.checkbox_frame, text="A*", onvalue = 1, offvalue = 0, variable=self.c6var).grid(row=1, column=1, sticky=NW)
        self.search_btn = Button(self.checkbox_frame, text="Search")
        self.search_btn.grid(pady=10, sticky=NW)
        self.search_btn.bind("<Button-1>", self.checkHeuristic)
        #TODO finish checkboxes and link up with backend

    def changeHeuristic(self, event):
        nodes[int(self.heur_node.get())].heuristic = int(self.heur_val.get())
        for node in nodes:
            print("node #", node.index, " heuristic = ", node.heuristic)

    def checkHeuristic(self, event):
        if (self.c5var.get() == 1 or self.c6var.get () == 1) and len(nodes):
            for node in nodes:
                if node.heuristic == -1:
                    messagebox.showerror("Incomplete Heuristics","Cannot perform informed search")
                    self.search_btn.lift()
                    break
        self.startSearchWindow(event)

    def startSearchWindow(self, event):
        pass
        #TODO

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
                    self.canvas.create_rectangle(weight_x-10, weight_y-10, weight_x+10, weight_y+10, fill="yellow", outline="red")
                    self.canvas.create_text(weight_x, weight_y, font=("Arial", 10), text=str(self.weight_val.get()))
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



root = Tk()
root.geometry("1500x750")
#root.attributes('-fullscreen', True)
app = App()
root.mainloop()