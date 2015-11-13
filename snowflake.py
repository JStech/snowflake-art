#!/usr/bin/env python3
from tkinter import *
from random import random

N = 80
iterations = 40

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


#           05  15  25  35  45  55
#         04  14  24  34  44  45
#       03  13  23  33  34  35
#     02  12  22  23 -24- 25
#   01  11  12  13  14  15
# 00  01  02  03  04  05

def get_neighbors(i, j):
    s = 0
    if (i, j) == (0, 0):
        return [0, 63][cells[0][1]]
    if (i, j) == (0, 1):
        return 32*cells[0][0] + 17*cells[0][1] + 10*cells[1][1] + 4*cells[0][2]
    if i==0:
        return 32*cells[0][j-1] + 17*cells[1][j-1] + 10*cells[1][j] + 4*cells[0][j+1]
    if i==j:
        return 33*cells[i-1][j] + 18*cells[i-1][j+1] + 12*cells[i][j+1]
    if i==j-1:
        return (32*cells[i][j-1] + 16*cells[i][j] + 8*cells[i+1][j] +
                4*cells[i][j+1] + 2*cells[i-1][j+1] + cells[i-1][j])
    return (32*cells[i][j-1] + 16*cells[i-1][j-1] + 8*cells[i-1][j] +
            4*cells[i][j+1] + 2*cells[i-1][j+1] + cells[i-1][j])

# (current_state, sum_neighbor_states): prob
rules = [[None]*64, [None]*64]
for i in range(64):
    if rules[0][i] is not None: continue
    r = random()
    for _ in range(6):
        rules[0][i] = r**2
        i = (i>>1) + ((i&1)<<5)
    r = random()
    for _ in range(6):
        rules[1][i] = r**0.5
        i = (i>>1) + ((i&1)<<5)

rules[0][0] = 0
rules[1][0] = 1

print(rules)

for _ in range(iterations):
    for i, r in enumerate(cells[:-1]):
        for j, c in enumerate(r[:-1]):
            next_cells[i][j] = 0
            if random() < rules[cells[i][j]][get_neighbors(i,j)]:
                next_cells[i][j] = 1
    cells, next_cells = next_cells, cells

for i, r in enumerate(cells):
    for j, c in enumerate(r):
        if c: draw_cell(i, j)

mainloop()
