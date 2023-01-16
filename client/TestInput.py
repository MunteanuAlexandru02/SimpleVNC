import tkinter
from tkinter import *

def leftclick(event):
    print("left")
    print(event.x, event.y)

def middleclick(event):

    print("middle")

def rightclick(event):
    print("right")

#def moved(event):
   #print(event.x, event.y)

var = tkinter.Tk()


c= Canvas(var, width=600, height=500)
x = c.create_oval(100,100,300,300,width=7,fill="red")
c.create_arc(100,100,300,300,start=0,extent=100,width=7,fill="yellow")

#c.bind("<Motion>", moved)

c.bind("<Button-1>", leftclick)

c.bind("<Button-2>", middleclick)

c.bind("<Button-3>", rightclick)

c.pack()

var.mainloop()