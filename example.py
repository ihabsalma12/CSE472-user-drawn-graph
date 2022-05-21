
from tkinter import *

master = Tk()
master.title('Painting in Python')

canvas_width = 600
canvas_height = 450
color='white'
bg ='black'

def REDPEN():
    global color
    color='red'
    print(color)
def BLUEPEN():
    global color
    color='blue'
    print(color)
def GREENPEN():
    global color
    color='green'
    print(color)

def paint(event):
    global color
    x1,y1=(event.x-1),(event.y-1)
    x2,y2=(event.x+1),(event.y+1)
    c.create_oval(x1,y1,x2,y2,fill=color,outline=color,width=0)

RedButton = Button(master, text = "RED", command =REDPEN)
BlueButton = Button(master, text = "BLUE", command =BLUEPEN)
GreenButton = Button(master, text = "GREEN", command =GREENPEN)

RedButton.pack()
BlueButton.pack()
GreenButton.pack()


c=Canvas(master,width=canvas_width,height=canvas_height,bg=bg)

c.pack(expand=YES,fill=BOTH)
c.bind('<B1-Motion>',paint)

message=Label(master,text='Press and Drag to draw')
message.pack(side=BOTTOM)
master.mainloop()