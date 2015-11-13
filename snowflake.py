#!/usr/bin/env python3
from tkinter import *
from random import random

N = 80
iterations = 80

scale = 4
offset = 400
def t(x):
    return scale*x + offset

def cube_to_hex(c):
    return (c[0], c[1])

def hex_to_cube(h):
    return (h[0], h[1], -h[1]-h[0])

def draw_point(x, y):
    w.create_oval(t(x)+scale/2, t(-y)+scale/2, t(x)-scale/2, t(-y)-scale/2)

def draw_cell(i, j):
    if i>j: return
    draw_point(j+i/2, i*3**0.5/2)
    draw_point(i+j/2, j*3**0.5/2)
    draw_point(j+i/2, -i*3**0.5/2)
    draw_point(i+j/2, -j*3**0.5/2)
    draw_point(-j-i/2, i*3**0.5/2)
    draw_point(-i-j/2, j*3**0.5/2)
    draw_point(-j-i/2, -i*3**0.5/2)
    draw_point(-i-j/2, -j*3**0.5/2)
    i, j = -i-j, i
    draw_point(j+i/2, i*3**0.5/2)
    draw_point(j+i/2, -i*3**0.5/2)
    draw_point(-j-i/2, i*3**0.5/2)
    draw_point(-j-i/2, -i*3**0.5/2)

master = Tk()

w = Canvas(master, width=2*offset, height=2*offset)
w.pack()

cells = [[0]*N for _ in range(N)]
next_cells = [[0]*N for _ in range(N)]
cells[0][0] = 1

def get_neighbor_sum(i, j):
    s = 0
    if i==0 and j==0:
        return cells[0][1]*6
    if i==0 and j==1:
        return cells[0][0] + 2*cells[0][1] + 2*cells[1][1] + cells[2][0]
    if i==0:
        return cells[0][j-1] + 2*cells[1][j-1] + 2*cells[1][j] + cells[0][j+1]
    if i==j:
        return 2*(cells[i-1][j] + cells[i-1][j+1] + cells[i][j+1])
    if i==j-1:
        return (cells[i][j] + cells[i][j-1] + cells[i-1][j] +
                cells[i-1][j+1] + cells[i][j+1] + cells[i+1][j])
    return (cells[i][j-1] + cells[i-1][j] + cells[i-1][j+1] +
            cells[i][j+1] + cells[i+1][j] + cells[i+1][j-1])

# (current_state, sum_neighbor_states): prob
rules = {
        (0,0): 0.0, (1,0): 1.0,
        (0,1): random(), (1,1): random(),
        (0,2): random(), (1,2): random(),
        (0,3): random(), (1,3): random(),
        (0,4): random(), (1,4): random(),
        (0,5): random(), (1,5): random(),
        (0,6): random(), (1,6): random()}

print(rules)

for _ in range(iterations):
    for i, r in enumerate(cells[:-1]):
        for j, c in enumerate(r[:-1]):
            next_cells[i][j] = 0
            if random() < rules[(cells[i][j], get_neighbor_sum(i,j))]:
                next_cells[i][j] = 1
    cells, next_cells = next_cells, cells

for i, r in enumerate(cells):
    for j, c in enumerate(r):
        if c: draw_cell(i, j)

mainloop()
