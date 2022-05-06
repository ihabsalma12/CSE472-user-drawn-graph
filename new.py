import pygame
import math
from sys import exit
from pygame.locals import *
from tkinter import *

#TODO graph class
class Graph:
    def __init__(self):
        self.adj_matrix = []
        self.node_to_be_moved = Rect()


class Button:
    def __init__(self, screen, colour, x, y, width, height, text = ''):
        self.screen = screen
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text


    def draw_button(self, outline = None):
        if outline:
            pygame.draw.rect(self.screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont("Calibri", 20)
            text_surface = font.render(self.text, True, "black")
            self.screen.blit(text_surface, (self.x + (self.width / 2 - text_surface.get_width() / 2), self.y + (self.height / 2 - text_surface.get_height() / 2)))


    def isOver(self, pos): #pos is (x,y) tuple
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


#TODO finish arrow
class Arrow: #TODO Rect obj!!!
    def __init__(self, start_node, end_node, directed): #edge between two circles, and bool directed or not
        self.start_node = start_node
        self.end_node = end_node
        self.directed = directed

    #def draw_arrow(self):
        #pygame.draw.polygon(screen, (0, 0, 0),
        #                    ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))


#TODO finish node
class Node:
    def __init__(self, screen, color, center_x, center_y, radius):
        self.screen = screen
        self.color = color
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

        self.surface = pygame.Surface((radius*2, radius*2))
        self.surface.fill("yellow")
        self.rect = pygame.draw.circle(self.screen, self.color, center=(self.center_x, self.center_y), radius=self.radius)
        #print(self.rect)

    def move_node(self):
        print("mouse clicked on node")
        #if event.type == MOUSEBUTTONDOWN:
            #new_mouse_pos =
        #self.screen.blit(pygame.transform.rotate(self.surface, 0), (10,10))

    def isOver(self, pos):
        if pos[0] > self.rect.midleft[0] and pos[0] < self.rect.midright[0]:
            if pos[1] < self.rect.midbottom[1] and pos[1] > self.rect.midtop[1]:
                return True
        return False


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000,500))
screen.fill("grey")
pygame.display.set_caption("CSE472 AI PROJECT")

graph = pygame.Surface((500,480))
graph.fill("white")

nodes = []
edges = [[]]

clicking = False

while True:
    add_node_btn = Button(screen, "light grey", 600, 50, 100, 30, text='Add node')
    add_node_btn.draw_button("dark grey")

    directed_btn = Button(screen, "light grey", 750, 50, 150, 30, text='Toggle directed')
    directed_btn.draw_button("dark grey")

    mouse_pos = pygame.mouse.get_pos()
    current_node = Node(screen=graph, color="black", center_x=200, center_y=200, radius=20)

    rot = 0
    loc = [mouse_pos[0], mouse_pos[1]]
    if clicking:
        rot -= 90
    screen.blit(pygame.transform.rotate(current_node.surface, rot), (loc[0], loc[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if add_node_btn.isOver(mouse_pos):
                    current_node = Node(screen=graph, color="black", center_x=200, center_y=200, radius=20)
                    nodes.append(current_node)
                if current_node.isOver(mouse_pos):
                    clicking = True

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False

    screen.blit(graph, (10,10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()

"""
    pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if add_node_btn.isOver(pos):
            node = pygame.draw.circle(surface=graph, color="grey", center=(200, 200), radius=20)
            nodes.append(node)

    #print(nodes)

    screen.blit(graph, (10,10))

    start_node = pygame.draw.circle(surface=graph, color="grey", center=(200, 200), radius=20) #example start
    end_node = pygame.draw.circle(surface=graph, color="grey", center=(100, 100), radius=20) #example end
    s = start_node.center #start_node.center
    e = end_node.center
    #pygame.draw.polygon(screen, (0, 0, 0), #s=(0,150) e=(300,150)
                        #((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))
    #pygame.draw.line(screen, "black", s, e, 10)

    arrow_surface = pygame.Surface((300,300))
    arrow_surface.fill("red")
    #pygame.draw.polygon(arrow_surface, (0,0,0),
    #                    ((s[0], s[1]-5), (s[0], s[1]+5), (e[0]-10, e[1]+5), (e[0]-10, e[1]+15), #tip=
    #                    (e[0], e[1]), (e[0]-10, e[1]-15), (e[0]-10, e[1]-5))) #polygon points go anticlockwise if arrow points to right
    pygame.draw.polygon(arrow_surface, (0, 0, 0), #s=(0,150) e=(300,150)
                        ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))
    screen.blit(arrow_surface, (10, 10))
    arrow2 = pygame.transform.flip(arrow_surface, flip_x=1, flip_y=1)
    arrow2.fill("yellow")
    screen.blit(arrow2, (10,10))

    #pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
"""




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
import tkinter

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
# adj_list = {}
# mylist = []
#
#
# def add_node(node):
#     if node not in mylist:
#         mylist.append(node)
#     else:
#         print("Nodes ", node, " already exists!")
#
#
# def add_edge(node1, node2, weight):
#     temp = []
#     if node1 in mylist and node2 in mylist:
#         if node1 not in adj_list:
#             temp.append([node2, weight])
#             adj_list[node1] = temp
#
#         elif node1 in adj_list:
#             temp.extend(adj_list[node1])
#             temp.append([node2, weight])
#             adj_list[node1] = temp
#
#     else:
#         print("Nodes don't exist!")
#
#
# def graph():
#     for node in adj_list:
#         print(node, " ---> ", [i for i in adj_list[node]])
#
#
# # Adding nodes
# add_node(0)
# add_node(1)
# add_node(2)
# add_node(3)
# add_node(4)
# # Adding edges
# add_edge(0, 1, 2)
# add_edge(1, 2, 2)
# add_edge(2, 3, 4)
# add_edge(3, 0, 5)
# add_edge(3, 4, 3)
# add_edge(4, 0, 1)
#
# # Printing the graph
# graph()
#
# # Printing the adjacency list
# print(adj_list)

# !/usr/bin/env python
# -*- coding: utf-8 -*-


"""
#Drawing circle
# canvas = Canvas(root, width=200, height=200, borderwidth=0, highlightthickness=0,
#                    bg="white")
# canvas.grid()
#
# def _create_circle(self, x, y, r, **kwargs):
#     return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
# Canvas.create_circle = _create_circle
#
# def _create_circle_arc(self, x, y, r, **kwargs):
#     if "start" in kwargs and "end" in kwargs:
#         kwargs["extent"] = kwargs["end"] - kwargs["start"]
#         del kwargs["end"]
#     return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
# Canvas.create_circle_arc = _create_circle_arc
#
# #canvas.create_circle(100, 120, 50, fill="blue", outline="#DDD", width=4)
# #canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=45, end=140)
# #canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=275, end=305)
# #canvas.create_circle_arc(100, 120, 45, style="arc", outline="white", width=6,
# #                         start=270-25, end=270+25)
# canvas.create_circle(150, 40, 20, fill="black", outline="")
#
# root.title("Circles and Arcs")
#"""

#current tkinter code
"""root = Tk()
root.title('CSE472 AI PROJECT')
root.geometry("1000x500")
root.configure(background="grey")

canvas = Canvas(root, width=500, height=500, borderwidth=0, highlightthickness=0, bg="white")
canvas.pack(pady=20)

nodes=[]

def drawNode(event):
    node = canvas.create_oval(175, 100, 100, 175, width=3, fill = "orange")
    node.bind("<B1-Motion>", dragNode)
    nodes.append(node)

def dragNode(event):
    event.widget.place(x=event.x_root, y=event.y_root, anchor=CENTER)

card = Canvas(root, width=74, height=97, bg='blue')
card.place(x=300, y=600,anchor=CENTER)
card.bind("<B1-Motion>", dragNode)

another_card = Canvas(root, width=74, height=97, bg='red')
another_card.place(x=600, y=600,anchor=CENTER)
another_card.bind("<B1-Motion>", dragNode)


add_node_btn = Button(root, text="Add node")
add_node_btn.bind('<Button-1>', drawNode)
add_node_btn.pack()


root.attributes ('-fullscreen', True)
root.mainloop()"""

#old code
# def genClick():
#     if(v.get().isnumeric()):
#         label_2 = Label(frame_1, text="Accepted")
#         label_2.grid()
#     else:
#         label_2 = Label(frame_1, text="Not Accepted")
#         label_2.grid()
#
#
# frame_1 = LabelFrame(root, padx=5, pady=5)
# frame_1.grid(row=0, column=0, padx=10, pady=10, sticky=NW)
#
# node_instr = Label(frame_1, text="1) Enter your number of nodes: ")
# node_instr.grid(row=0, column=0, sticky=W)
#
# v = StringVar()
# node_entry = Entry(frame_1, width=20, borderwidth=2, textvariable=v)
# node_entry.grid(row=0, column=1, padx=10)
#
# node_btn = Button(frame_1, text="Generate nodes", command=genClick)
# node_btn.grid(row=1, column=1)
#
# edge_instr = Label(frame_1, text="2) Select (directed/ undirected) edge, then click on two nodes to connect.")
# edge_instr.grid(row=2, column=0, sticky=W)
#
# d_edge_btn = Button(frame_1, text="Directed")
# ud_edge_btn = Button(frame_1, text="Undirected")
# d_edge_btn.grid(row=3, column=0, sticky=W, padx=5)
# ud_edge_btn.grid(row=4, column=0, sticky=W, padx=5)
#
# frame_2 = LabelFrame(root, padx=5, pady=5)
# frame_2.grid(row=0, column=1, padx=10, pady=10)
#
# graph_canvas = Canvas(frame_2, width=750, height=750, bg="green", borderwidth=0, highlightthickness=0,)
# graph_canvas.grid(row=0, column=1, sticky=E)