import pygame
import math
from sys import exit
from pygame.locals import *

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
screen.fill("grey")
pygame.display.set_caption("CSE472 AI PROJECT")

graph = pygame.Surface((500,480))
graph.fill("white")

nodes = []
edges = [[]]



#clicking = False

while True:
    add_node_btn = Button(screen, "light grey", 600, 50, 100, 30, text='Add node')
    add_node_btn.draw_button("dark grey")

    directed_btn = Button(screen, "light grey", 750, 50, 150, 30, text='Toggle directed')
    directed_btn.draw_button("dark grey")

    mouse_pos = pygame.mouse.get_pos()

    #current_node_surf = pygame.Surface((20,20))
    #current_node_surf.fill("white")
    #current_node = Node(surf=current_node_surf, color="black", center_x=200, center_y=200, radius=20)
    #current_node_rect = current_node_surf.get_rect()

    #rot = 0
    #loc = [mouse_pos[0], mouse_pos[1]]
    #if clicking:
        #rot -= 90
    #screen.blit(pygame.transform.rotate(current_node.surface, rot), (loc[0], loc[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if add_node_btn.isOver(mouse_pos):
                    print("mouse button is down on Add Node btn")
                    background = screen
                    screen.blit(background, (0, 0))
                    current_node_surf = pygame.transform.scale(pygame.image.load('R.png'), (40,40))
                    current_node_rect = current_node_surf.get_rect()
                    #current_node_surf = pygame.Surface((40,40))
                    #current_node_surf.fill("yellow")
                    #current_node_rect = pygame.draw.circle(surface=current_node_surf, color="green", center=(200,200), radius=20, width=3)
                    graph.blit(current_node_surf, (200,200), current_node_rect)
                    pygame.display.update()
                    #current_node = Node(screen=graph, color="black", center_x=200, center_y=200, radius=20)
                    #nodes.append(current_node)
                if mouse_pos[0] > 200 and mouse_pos[1] > 200:
                    for x in range(100):
                        screen.blit(background, current_node_rect)  # erase
                        position = (pygame.mouse.get_pos()[0] - 20, pygame.mouse.get_pos()[1] - 20) # move player
                        graph.blit(current_node_surf, position, current_node_rect)  # draw new player
                        pygame.display.update()  # and show it all
                        #pygame.time.delay(100)  # stop the program for 1/10 second
                    print("mouse button down on current node")
                    #clicking = True

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                #clicking = False
                print("mouse button is up")

    #graph.blit(current_node_surf, (200,200))
    screen.blit(graph, (10,10))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()