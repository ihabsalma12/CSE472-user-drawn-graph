from tkinter import *

class SearchWindow:
    def __init__(self, title, nodes, edges, solution, visited):
        self.title = title
        self.nodes = nodes
        self.edges = edges

        #should've done this the first time
        self.config_nodes = [[]]

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
                                    width=3, outline="black", tags=str(node.index))
            print("tag oval item", x, "as:", str(node.index))
            x = self.canvas.create_text(node.center_x, node.center_y, font=("Arial", 12), text=str(node.index), tags="do_not_visit")
            print("tag text", x, "as", "do_not_visit")

    def drawAllEdges(self):
        for edge in self.edges:
            if edge.start_node == edge.end_node:  # self-directed edge
                y = self.canvas.create_line(edge.start_node.right, edge.start_node.bottom,
                                        edge.start_node.right + 15, edge.start_node.bottom,
                                        edge.start_node.right + 15, edge.start_node.top,
                                        edge.start_node.right, edge.start_node.top, fill="red",
                                        width=3, arrow=edge.arrow, tags="do_not_visit")
            else:
                y = self.canvas.create_line(edge.start_node.center_x, edge.start_node.center_y,
                                        edge.end_node.center_x, edge.end_node.center_y, fill="red", width=3,
                                        arrow=edge.arrow, tags="do_not_visit")
            print("tags for edge item", y, "as tags=\"do_not_visit\"")

    def traceNext(self, event):
        if len(self.solution) > 0 or len(self.visited) > 0:
            if len(self.visited) > 0:
                #print("itemconfig visited tagorID=")#, str(self.visited[0]))
                nxt = str(self.visited[0])
                fill = 'green'
                del self.visited[0]
            else:
                nxt = str(self.solution[0])
                fill = 'blue'
                del self.solution[0]
            print("now sol=", self.solution)
            print("now vis=", self.visited)
            print("config tag is", nxt, "and fill is", fill)
            self.canvas.itemconfig(str(nxt), fill=fill)
        else:
            return



    def printInfo(self):
        print("hello, info")
