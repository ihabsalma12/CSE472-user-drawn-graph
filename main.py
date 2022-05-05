from tkinter import *

ROOT_DIMENSIONS = "1000x500"
CANVAS_BG_COLOR = "white"
CANVAS_HEIGHT = "500"
CANVAS_WIDTH = "750"
CANVAS_GRID_STICKY = NW
BUTTON_STICKY = NW
NODE_INIT_POS = (10,10)
NODE_RAD = 40

def addNode(event):
    canvas.create_oval(NODE_INIT_POS[0],NODE_INIT_POS[1],NODE_RAD+NODE_INIT_POS[0],NODE_RAD+NODE_INIT_POS[0])

root = Tk()
root.geometry(ROOT_DIMENSIONS)

canvas = Canvas(root, background=CANVAS_BG_COLOR, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.grid(sticky=CANVAS_GRID_STICKY)

add_node_btn = Button(root, text="Add node")
add_node_btn.grid(row=0, column=1, sticky=BUTTON_STICKY)
add_node_btn.bind('<Button-1>', addNode)


root.mainloop()