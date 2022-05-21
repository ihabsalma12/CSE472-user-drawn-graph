from tkinter import *

class SearchWindow:
    def __init__(self, title, nodes, edges, solution, visited):
        self.title = title
        self.nodes = nodes
        self.edges = edges

        self.node_tags = [len(self.nodes)]
        self.config_vis_tags = []
        self.config_sol_tags = []

        self.solution = solution
        self.visited = visited
        print("hello, init window")

    def drawWindow(self):
        self.top = Toplevel()
        self.top.title(self.title)
        self.top.geometry("1500x750")
        self.canvas = Canvas(self.top, height=700, width=1000, bg="white")
        self.canvas.grid(sticky=NW, padx=10, pady=10)
        self.drawAllNodes()
        self.drawAllEdges()
        self.top.bind("<Button-1>", self.traceNext)
        print("window set up!")

    def drawAllNodes(self):
        for node in self.nodes:
            x = self.canvas.create_oval(node.center_x - 20, node.center_y - 20, node.center_x + 20, node.center_y + 20, fill="grey",
                                    width=3, outline="black")
            self.canvas.create_text(node.center_x, node.center_y, font=("Arial", 12), text=str(node.index))
            x2 = int(node.index)
            self.node_tags.insert(x2,x)
        print("node_tags!!", self.node_tags)
        print(self.node_tags)

        #print("config vis=", self.config_vis_tags)
        #print("config sol=", self.config_sol_tags)

    def drawAllEdges(self):
        for edge in self.edges:
            if edge.start_node == edge.end_node:  # self-directed edge
                self.canvas.create_line(edge.start_node.right, edge.start_node.bottom,
                                        edge.start_node.right + 15, edge.start_node.bottom,
                                        edge.start_node.right + 15, edge.start_node.top,
                                        edge.start_node.right, edge.start_node.top, fill="red",
                                        width=3, arrow=edge.arrow)
            else:
                self.canvas.create_line(edge.start_node.center_x, edge.start_node.center_y,
                                        edge.end_node.center_x, edge.end_node.center_y, fill="red", width=3,
                                        arrow=edge.arrow)

    def traceNext(self, event):
        #now, both oval and vis/sol arrays are ordered, where the first to be traced is at index[0]
        if len(self.visited) > 0 or len(self.solution) > 0:
            if len(self.visited) > 0:
                nxt = str(self.node_tags[self.visited[0]])
                fill = 'blue'
                del self.visited[0]
            else:
                nxt = str(self.node_tags[self.solution[0]])
                fill = 'green'
                del self.solution[0]
            print("next oval to color in:", nxt, "color=", fill)
            self.canvas.itemconfig(nxt, fill=fill)