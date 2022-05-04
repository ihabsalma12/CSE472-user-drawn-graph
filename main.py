import pygame
import math
from sys import exit
from pygame.locals import *

#TODO Graph class
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

#TODO Arrow class (with weights and direction)
class Edge: #TODO Rect obj!!!
    def __init__(self, start_node, end_node, weight): #edge between two circles, and bool directed or not
        self.weight = weight
        self.start_node = start_node
        self.end_node = end_node
        self.start_rect = start_node.get_rect()
        self.end_rect = end_node.get_rect()
        self.draw_edge()

    def draw_edge(self):
        if directed:
            self.draw_directed()
        else: self.draw_undirected()

    def draw_directed(self):
        arrow = pygame.transform.scale(pygame.image.load('arrow.png'),
                               (abs(self.start_rect.center[0] - self.end_rect.center[0]),
                                abs(self.start_rect.center[1] - self.end_rect.center[1])))
        screen.blit(arrow, (20,20))
        if self.weight == '':
            font = pygame.font.SysFont("Calibri", 20)
            text_surface = font.render('1', True, "black")
            screen.blit(text_surface, (90,90))

    #arrow = pygame.draw.polygon(screen, (0, 0, 0),
        #((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))

    def draw_undirected(self):
        pygame.draw.line(screen, "dark grey", self.start_rect.center, self.end_rect.center, width = 10)

#TODO finish node
class Node:
    def __init__(self, surf, color, center_x, center_y, radius):
        self.screen = screen
        self.color = color
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

        self.surf = surf
        self.rect = pygame.draw.circle(self.surf, self.color, center=(self.center_x, self.center_y), radius=self.radius)

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
screen.fill("white")
pygame.display.set_caption("CSE472 AI PROJECT")

nodes = []
edges = [[]]
adding_nodes_state = False
drawing_edge_state = True
directed = False


while True:
    add_node_btn = Button(screen, "light grey", 750, 10, 100, 30, text='Add node')
    add_node_btn.draw_button("dark grey")

    directed_btn = Button(screen, "light grey", 750, 90, 150, 30, text='Toggle directed')
    directed_btn.draw_button("dark grey")

    undirected_btn = Button(screen, "light grey", 750, 140, 170, 30, text='Toggle undirected')
    undirected_btn.draw_button("dark grey")

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if add_node_btn.isOver(mouse_pos):
                    print("mouse button is down on Add Node btn")
                    nodes.append(pygame.transform.scale(pygame.image.load('R.png'), (40,40)))
                    adding_nodes_state = not adding_nodes_state

                if directed_btn.isOver(mouse_pos):
                    print("mouse over toggle directed")
                    directed = True
                    drawing_edge_state = True

                if undirected_btn.isOver(mouse_pos):
                    print("mouse over toggle undirected")
                    directed = False
                    drawing_edge_state = True

                if mouse_pos[0] < 700 and mouse_pos[1] < 500 and len(nodes) and adding_nodes_state:
                    screen.blit(nodes[-1], (mouse_pos[0]-20, mouse_pos[1]-20))
                    print("mouse button down on current node")
                    print(len(nodes))
                    adding_nodes_state = False

                if len(nodes) >= 2 and drawing_edge_state:
                    edge = Edge(nodes[0], nodes[1], 5)

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                print("mouse button is up")

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()