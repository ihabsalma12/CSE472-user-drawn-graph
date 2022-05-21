'''
    This let you create more windows,
    but you cannot open the same one
    more than once.
'''

'''
import tkinter as tk


class Win1:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x300")
        self.show_widgets()

    def show_widgets(self):
        self.frame = tk.Frame(self.master)
        self.master.title("Window n.1")
        self.create_button("Click to open Window 2", Win2)
        self.create_button("Click to open Window 3", Win3)
        self.frame.pack()

    def create_button(self, text, _class):
        "Button that creates a new window"
        tk.Button(
            self.frame, text=text,
            command=lambda: self.new_window(_class)).pack()

    def new_window(self, _class):
            global win2, win3

            try:
                if _class == Win2:
                    if win2.state() == "normal":
                        win2.focus()
            except:
                win2 = tk.Toplevel(self.master)
                _class(win2)

            try:
                if _class == Win3:
                    if win3.state() == "normal":
                        win3.focus()
            except:
                win3 = tk.Toplevel(self.master)
                _class(win3)

    def close_window(self):
        self.master.destroy()

class Win2(Win1):

    def show_widgets(self):
        "A frame with a button to quit the window"
        self.master.title("Window 2")
        self.frame = tk.Frame(self.master, bg="red")
        self.quit_button = tk.Button(
            self.frame, text=f"Quit this window n. 2",
            command=self.close_window)
        self.quit_button.pack()
        self.create_button("Open window 3 from window 2", Win3)
        self.frame.pack()



class Win3(Win2):

    def show_widgets(self):
        self.master.title("Window 3")
        self.frame = tk.Frame(self.master, bg="green")
        self.quit_button = tk.Button(
            self.frame, text=f"Quit this window n. 3",
            command=self.close_window)
        self.label = tk.Label(
            self.frame, text="THIS IS ONLY IN THE THIRD WINDOW")
        self.label.pack()
        self.frame.pack()



root = tk.Tk()
app = Win1(root)
root.mainloop()'''

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
            y = self.canvas.create_oval(node.center_x - 20, node.center_y - 20, node.center_x + 20, node.center_y + 20, fill="grey",
                                    width=3, outline="black", tags=str(node.index))
            print("tag oval as:", str(node.index))
            self.canvas.create_text(node.center_x, node.center_y, font=("Arial", 12), text=str(node.index))

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
        print("len vsis=",len(self.visited), "len sol=", len(self.solution))
        lv = len(self.visited)
        ls = len(self.solution)
        if lv > 0:
            print("itemconfig visited tagorID=", str(self.visited[0]))
            #self.canvas.itemconfig(str(self.visited[0]), fill="blue")
            del self.visited[0]
            print("now vis=", self.visited)
            return
        if ls > 0:
            print("itemconfig solution tagorID=", str(self.visited[0]))
            #self.canvas.itemconfig(str(self.solution[0]), fill="green")
            print("now sol=", self.solution)
            del self.solution[0]


    def printInfo(self):
        print("hello, info")
