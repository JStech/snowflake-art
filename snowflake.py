#!/usr/bin/env python3
from tkinter import *

scale = 5
offset = 300
def t(x): return scale*x + offset

drawn = set()
def draw_point(x, y):
    if (x, y) in drawn:
        print("redrawn:", x, y)
    drawn.add((x, y))
    w.create_oval(t(x)+3, t(-y)+3, t(x)-3, t(-y)-3)

def draw_cell(i, j):
    if j<2*i-1: return
    draw_point(j+(i%2)/2, 3**0.5/2*i)
    if i>0: draw_point(j+(i%2)/2, -3**0.5/2*i)
    if j>0:
        draw_point(-j-(i%2)/2, 3**0.5/2*i)
        if i>0: draw_point(-j-(i%2)/2, -3**0.5/2*i)

master = Tk()

w = Canvas(master, width=600, height=600)
w.pack()

cells = [[0]*10 for _ in range(5)]
cells[0][0] = 1
cells[0][1] = 1
cells[0][2] = 1
cells[1][1] = 1
cells[1][2] = 1
cells[1][3] = 1

for i, r in enumerate(cells):
    for j, c in enumerate(r):
        if c: draw_cell(i, j)

mainloop()
