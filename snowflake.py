#!/usr/bin/env python3
from tkinter import *
from random import random

N = 200
iterations = 40

#shape="star"
shape="hexagon"

scale = 4
offset = 400

r3 = 3**0.5


#           05  15  25  35  45  55
#         04  14  24  34  44  45
#       03  13  23  33  34  35
#     02  12  22  23  24  25
#   01  11  12  13  14  15
# 00  01  02  03  04  05

def neighbors(i, j):
  if i>j: return
  if (i, j) == (0, 0):
    for _ in range(6): yield (0, 1)
    return
  if (i, j) == (0, 1):
    for r in ((0, 2), (1, 1), (0, 1), (0, 0), (0, 1), (1, 1)):
      yield r
    return
  if i == 0:
    for r in ((0, j+1), (1, j), (1, j-1), (0, j-1), (1, j-1), (1, j)):
      yield r
    return
  if i == j:
    for r in ((i, j+1), (i, j+1), (i-1, j+1), (i-1, j), (i-1, j), (i-1, j+1)):
      yield r
    return
  if i == j-1:
    for r in ((i, j+1), (i+1, j), (i, j), (i, j-1), (i-1, j), (i-1, j+1)):
      yield r
    return
  for r in ((i, j+1), (i+1, j), (i+1, j-1), (i, j-1), (i-1, j), (i-1, j+1)):
    yield r

  if i+1 <= j:   yield (i+1, j)
  if i+1 <= j-1: yield (i+1, j-1)
  if i <= j-1:   yield (i, j-1)
  if i-1 <= j:   yield (i-1, j)
  if i-1 <= j+1: yield (i-1, j+1)
  if i <= j+1:   yield (i, j+1)

def t(x):
  return scale*x + offset

def cube_to_hex(c):
  return (c[0], c[1])

def hex_to_cube(h):
  return (h[0], h[1], -h[1]-h[0])

def draw_point(x, y):
  w.create_oval(t(x)+scale/3, t(-y)+scale/3, t(x)-scale/3, t(-y)-scale/3,
      outline="white", fill="#aaaaff")

def draw_cell(i, j):
  if i>j: return
  for (ii, jj) in ((i, j), (j, i), (-i-j, i)):
    for xm in (-1, 1):
      for ym in (-1, 1):
        draw_point(xm*(jj+ii/2), ym*ii*r3/2)

def draw_border(i1, j1, i2, j2):
  for (ii1, jj1, ii2, jj2) in ((i1, j1, i2, j2), (j1, i1, j2, i2), (-i1-j1, i1, -i2-j2, i2)):
    for xm in (-1, 1):
      for ym in (-1, 1):
        x1, y1 = xm*(jj1 + ii1/2), ym*ii1*r3/2
        x2, y2 = xm*(jj2 + ii2/2), ym*ii2*r3/2
        w.create_line(
            t((x1+x2+(y2-y1)/r3)/2), t((y1+y2+(x1-x2)/r3)/2),
            t((x1+x2-(y2-y1)/r3)/2), t((y1+y2-(x1-x2)/r3)/2))

master = Tk()

w = Canvas(master, width=2*offset, height=2*offset)
w.pack()

cells = [[0]*N for _ in range(N)]
next_cells = [[0]*N for _ in range(N)]
cells[0][0] = 1

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

  #  . .    . .    o .    . o    o o    . .    o .
  # .   .  o   .  o   .  o   .  o   .  o   o  o   o
  #  . .    . .    . .    . .    . .    . .    . .
  #   0      1      3      5      7      9      11
  #
  #  . o    o o    . o    o o    o .    o o    o o
  # o   o  o   o  o   .  o   .  o   o  o   o  o   o
  #  . .    . .    . o    . o    . o    . o    o o
  #   13     15     21     23     27     31     63

  # freezing probability

  r = {
       0:0.0,  13:0.1,
       1:1.0,  15:0.0,
       3:0.4,  21:0.1,
       5:0.1,  23:0.4,
       7:0.0,  27:0.7,
       9:0.6,  31:0.9,
      11:0.1,  63:0.4
      }
  ii = i
  for _ in range(6):
    rules[0][ii] = r[i]
    ii = (ii>>1) + ((ii&1)<<5)
  # not-thawing probabilities
  r = {
       0:1.0,  13:1.0,
       1:1.0,  15:0.7,
       3:0.3,  21:0.5,
       5:0.4,  23:0.7,
       7:0.2,  27:0.8,
       9:1.0,  31:0.3,
      11:1.0,  63:0.7
      }
  for _ in range(6):
    rules[1][ii] = r[i]
    ii = (ii>>1) + ((ii&1)<<5)

for _ in range(iterations):
  for i, r in enumerate(cells[:-1]):
    for j, c in enumerate(r[:-1]):
      next_cells[i][j] = 0
      if shape=="hexagon" and i+j>=N/4: continue
      if random() < rules[cells[i][j]][get_neighbors(i,j)]:
        next_cells[i][j] = 1
  cells, next_cells = next_cells, cells

for i, r in enumerate(cells):
  for j, c in enumerate(r):
    for ni, nj in neighbors(i, j):
      if c:
        if not cells[ni][nj]:
          draw_border(i, j, ni, nj)


mainloop()
