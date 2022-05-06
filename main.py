import sys
from pprint import pprint
from tkinter import *


nodes = []
edges = []

class Node:
    def __init__(self, canvas):
        self.canvas = canvas
        self.index = len(nodes)
        self.RADIUS = 20
        self.INITIAL_FILL = "grey"
        self.fill = self.INITIAL_FILL
        self.INITIAL_OUTLINE = "black"
        self.outline = "black"
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
                                fill=self.INITIAL_FILL, width=self.WIDTH, outline=self.INITIAL_OUTLINE)
        self.canvas.create_text(self.center_x, self.center_y, text=str(self.index))
        nodes.append(self)

    def changeOutline(self, outline):
        #start and goal
        pass

    def changeFill(self, fill):
        pass #visiting

    def changeState(self, fill):
        pass #visiting

class Edge:
    def __init__(self, canvas, is_directed):
        self.canvas = canvas
        self.is_directed = is_directed
        self.arrow = "none"
        if is_directed == True: self.arrow = "last"
        self.ARROW_WIDTH = 5
        self.FILL = "red"
        self.WIDTH = 3
        self.start_x = -1
        self.start_y = -1
        self.end_x = -1
        self.end_y = -1
        self.start_node = nodes[0] #temp incorrect

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
                                                self.start_node.right + 15, self.start_node.bottom, fill=self.FILL,
                                                width=self.WIDTH, arrow="none")
                        self.canvas.create_line(self.start_node.right + 15, self.start_node.bottom,
                                                self.start_node.right + 15, self.start_node.top, fill=self.FILL,
                                                width=self.WIDTH, arrow="none")
                        self.canvas.create_line(self.start_node.right + 15, self.start_node.top,
                                                self.start_node.right, self.start_node.top, fill=self.FILL,
                                                width=self.WIDTH, arrow=self.arrow)
                    else:
                        self.canvas.create_line(self.start_node.center_x, self.start_node.center_y,
                                            self.end_node.center_x, self.end_node.center_y, fill=self.FILL, width = self.WIDTH,
                                            arrow=self.arrow)
                    edges.append(self)
                    self.canvas.bind("<Button-1>", app.addEdge) #TODO fix bug, app opens twice
        #TODO if it's the same start and end node

        def addWeight(self, event):
            #TODO bind number keys: https://www.tutorialspoint.com/how-to-bind-all-the-number-keys-in-tkinter
            pass

class App:
    def __init__(self):
        self.adding_nodes_state = False
        self.adding_edges_state = False
        self.is_directed = False

        self.canvas = Canvas(root, height=480, width=730, bg="white")
        self.canvas.grid(sticky=NW, padx=10, pady=10)
        self.btns_frame = Frame(root, height=250, width=250)
        self.btns_frame.grid(row=0, column=1, sticky=NW)

        self.add_nodes_btn = Button(self.btns_frame, text="Add nodes")
        self.add_nodes_btn.bind("<Button-1>", self.startAddNodes)
        self.add_nodes_btn.grid(row=0, column=0, sticky=NW, pady=15)

        self.add_directed_btn = Button(self.btns_frame, text="Add directed edges")
        self.add_directed_btn.bind("<Button-1>", self.startAddDirected)
        self.add_directed_btn.grid(row=1, column=0, sticky=NW)

        self.add_undirected_btn = Button(self.btns_frame, text="Add undirected edges")
        self.add_undirected_btn.bind("<Button-1>", self.startAddUndirected)
        self.add_undirected_btn.grid(row=2, column=0, sticky=NW)

        self.Sinstr_label = Label(self.btns_frame, text="Press \"S\" on keyboard to choose and confirm start node.")
        self.Ginstr_label = Label(self.btns_frame, text="Press \"G\" on keyboard to choose and confirm goal nodes.")
        self.Sinstr_label.grid(row=3, column=0, sticky=NW)
        self.Ginstr_label.grid(row=4, column=0, sticky=NW)

        #self.canvas.bind("<1>", self.moveArrowsfg)

    #def moveArrowsfg(self, event):
        #for edge in edges:
            #event.widget.tag_raise(edge)

    def startAddNodes(self, event):
        print("start adding nodes...")
        self.adding_nodes_state = True
        self.add_nodes_btn.configure(bg="grey")
        self.node_addID = self.canvas.bind("<Button-1>", self.addNode)
        self.add_nodes_btn.bind("<Button-1>", self.endAddNodes)

    def addNode(self, event):
        self.new_node = Node(self.canvas).drawNode(event)

        root.bind('<KeyPress-s>', self.setStart)
        root.bind('<KeyPress-g>', self.setGoals, '+')
        root.bind('<KeyPress-S>', self.setStart, '+')
        root.bind('<KeyPress-G>', self.setGoals, '+')

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

    def setStart(self, event):
        self.Snode_ID = self.canvas.bind("<Button-1>", self.chooseNode)
        print("start")
        #TODO erase this, we can use entry box to enter the start and goal nodes
        #note: we can't change the color or outline (when tracing) unless
        #we redraw, and the edges will be drawn under the nodes (we can't see them)
        #redrawing will add the node/ edge to the array again, so separate those functions!
        #also, look into states!!!

    def setGoals(self, event):
        if len(nodes) != 0:
            root.bind('<KeyPress-s>', self.setStart)
            root.bind('<KeyPress-g>', self.setGoals)
            root.bind('<KeyPress-S>', self.setStart)
            root.bind('<KeyPress-G>', self.setGoals)
        print("goals")


root = Tk()
root.geometry("1100x500")
app = App()
root.mainloop()