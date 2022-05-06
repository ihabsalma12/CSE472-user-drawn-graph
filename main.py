import sys
from pprint import pprint
from tkinter import *

import main

nodes = []
edges = []

class Node:
    def __init__(self, canvas):
        self.canvas = canvas
        self.index = len(nodes)
        self.RADIUS = 20
        self.INITIAL_FILL = "grey"
        self.WIDTH = 3
        self.visited = False
        #self.state = "normal" #TODO look this up: https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html?highlight=create_circle
        self.center_x = -1
        self.center_y = -1
        self.top = -1
        self.bottom = -1
        self.left = -1
        self.right = -1


    def drawNode(self, event):
        self.index = len(nodes)
        self.center_x = event.x
        self.center_y = event.y
        self.top = self.center_y - self.RADIUS
        self.bottom = self.center_y + self.RADIUS
        self.left = self.center_x - self.RADIUS
        self.right = self.center_x + self.RADIUS
        self.canvas.create_oval(event.x - self.RADIUS, event.y - self.RADIUS, event.x + self.RADIUS, event.y + self.RADIUS,
                                fill=self.INITIAL_FILL, width=self.WIDTH)
        nodes.append(self)
        print("node #" , self.index, " center=(", self.center_x, ",",
        self.center_y, ")", " top=", self.top, " bottom=", self.bottom,
        " left=", self.left," right=",self.right)

class Edge:
    def __init__(self, canvas, is_directed):
        self.canvas = canvas
        self.is_directed = is_directed
        self.start_x = -1
        self.start_y = -1
        self.end_x = -1
        self.end_y = -1

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
                    self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y, fill="red")
                    edges.append(self)
                    self.canvas.bind("<Button-1>", app.addEdge) #TODO fix bug, app opens twice
        #TODO if it's the same start and end node

        def addWeight(self, event):
            pass

class App:
    def __init__(self):
        self.adding_nodes_state = False
        self.adding_edges_state = False
        self.is_directed = False

        self.canvas = Canvas(root, height=480, width=730, bg="white")
        self.canvas.grid(sticky=NW, padx=10, pady=10)
        self.btns_frame = Frame(root, height=250, width=250)

        self.add_nodes_btn = Button(self.btns_frame, text="Add nodes")
        self.add_nodes_btn.bind("<Button-1>", self.startAddNodes)
        self.add_nodes_btn.grid(row=0, column=0, sticky=NW, pady=15)

        self.add_directed_btn = Button(self.btns_frame, text="Add directed edges")
        self.add_directed_btn.bind("<Button-1>", self.startAddDirected)
        self.add_directed_btn.grid(row=1, column=0, sticky=NW)

        self.add_undirected_btn = Button(self.btns_frame, text="Add undirected edges")
        self.add_undirected_btn.bind("<Button-1>", self.startAddUndirected)
        self.add_undirected_btn.grid(row=2, column=0, sticky=NW)

        self.btns_frame.grid(row=0, column=1, sticky=NW)

    def startAddNodes(self, event):
        print("start adding nodes...")
        self.adding_nodes_state = True
        self.add_nodes_btn.configure(bg="grey")
        self.node_addID = self.canvas.bind("<Button-1>", self.addNode)
        self.add_nodes_btn.bind("<Button-1>", self.endAddNodes)

    def addNode(self, event):
        self.new_node = Node(self.canvas).drawNode(event)

    def endAddNodes(self, event):
        print("end nodes!")
        self.adding_nodes_state = False
        self.add_nodes_btn.configure(bg='SystemButtonFace')
        self.canvas.unbind("<Button-1>", self.node_addID)
        self.add_nodes_btn.bind("<Button-1>", self.startAddNodes)

    def startAddDirected(self, event):
        print("start adding directed...")
        self.adding_edges_state = True
        self.add_directed_btn.configure(bg="grey")
        if len(edges) == 0:
            self.is_directed = True
            self.node1_edge_addID = self.canvas.bind("<Button-1>", self.addEdge)
        self.add_directed_btn.bind("<Button-1>", self.endAddDirected)

    def addEdge(self, event):
        self.new_di_edge = Edge(self.canvas, self.is_directed).drawEdgeFrom(event)
        #when we draw one edge, then set is_directed = True and do not allow to startAddUndirected

    def endAddDirected(self, event):
        print("end directed edges!")
        self.adding_nodes_state = False
        self.canvas.unbind("<Button-1>", '')
        self.add_directed_btn.configure(bg='SystemButtonFace')
        self.add_directed_btn.bind("<Button-1>", self.startAddDirected)
        print("len(edges) = ", len(edges))
        for edge in edges:
            print("(", edge.start_node.center_x,"," ,edge.start_node.center_y, ") -> ",
                  "(", edge.end_node.center_x,"," ,edge.end_node.center_y, ")", edge.is_directed)

    def startAddUndirected(self, event):
        pass

    def endAddUndirected(self, event):
        pass


root = Tk()
root.geometry("1000x500")
app = App()
root.mainloop()