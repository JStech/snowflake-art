#!/usr/bin/env python3
from tkinter import *
from dxfwrite import DXFEngine as dxf
from random import random, randrange, randint
import os

N = 30
iterations = 40
dxf_scale = 1/12

shape="star"
#shape="hexagon"

base_rules = [
    # freezing probability
    {
      0:0.0,  13:0.1,
      1:1.0,  15:0.0,
      3:0.2,  21:0.1,
      5:0.1,  23:0.1,
      7:0.0,  27:1.0,
      9:0.2,  31:1.0,
      11:0.1,  63:0.0
      },
    # not-thawing probabilities
    {
      0:1-0.0,  13:1-0.0,
      1:1-0.0,  15:1-0.3,
      3:1-0.7,  21:1-0.5,
      5:1-0.5,  23:1-0.0,
      7:1-0.5,  27:1-0.1,
      9:1-0.0,  31:1-0.2,
      11:1-0.0,  63:1-0.3
      }
    ]

#base_rules = [
#    {x: random() for x in [0, 1, 3, 5, 7, 9, 11, 13, 15, 21, 23, 27, 31, 63]},
#    {x: random() for x in [0, 1, 3, 5, 7, 9, 11, 13, 15, 21, 23, 27, 31, 63]}]


scale = 5
offset = 400

r3 = 3**0.5

#           05  15  25  35  45  55
#         04  14  24  34  44  45
#       03  13  23  33  34  35
#     02  12  22  23  24  25
#   01  11  12  13  14  15
# 00  01  02  03  04  05

def neighbors(i, j):
  """iterate over neighbors (addresses) of (i, j)"""
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

# drawing functions
def t(x):
  """scale x for tkinter display"""
  return scale*x + offset

def draw_point(x, y):
  """Draw a small blue circle at location (x, y)"""
  w.create_oval(t(x)+scale/3, t(-y)+scale/3, t(x)-scale/3, t(-y)-scale/3,
      outline="#aaaaff", fill="#aaaaff")

def draw_cell(i, j):
  """Translate cell (i, j) to (x, y) position, and draw blue circle"""
  draw_point(j + i/2, i*r3/2)

def draw_cells(i, j):
  """Draw cell (i, j) in all 12 symmetric locations"""
  if i>j: return
  for (ii, jj) in ((i, j), (j, i), (-i-j, i)):
    for xm in (-1, 1):
      for ym in (-1, 1):
        draw_point(xm*(jj+ii/2), ym*ii*r3/2)

def draw_edge(edge):
  """Draw the edge from vertex (i1, i2, 0) to vertex (i2, j2, 1)"""
  ((i1, j1), (i2, j2)) = edge
  w.create_line(t(j1 + i1/2 + 1/2), t((i1-1/3)*r3/2),
      t(j2 + i2/2 + 1/2), t((i2+1/3)*r3/2))

def draw_border(i1, j1, i2, j2):
  """Draw line separating cell (i1, j1) from cell (i2, j2)"""
  for (ii1, jj1, ii2, jj2) in ((i1, j1, i2, j2), (j1, i1, j2, i2), (-i1-j1, i1, -i2-j2, i2)):
    for xm in (-1, 1):
      for ym in (-1, 1):
        x1, y1 = xm*(jj1 + ii1/2), ym*ii1*r3/2
        x2, y2 = xm*(jj2 + ii2/2), ym*ii2*r3/2
        w.create_line(
            t((x1+x2+(y2-y1)/r3)/2), t((y1+y2+(x1-x2)/r3)/2),
            t((x1+x2-(y2-y1)/r3)/2), t((y1+y2-(x1-x2)/r3)/2))

# output
def save_dxf():
  """Write current flake stored in flake_edges to snowflake.dxf"""
  flake_borders = [[]]
  while len(flake_edges) > 0:
    if flake_borders[-1] == []:
      start = flake_edges.pop()
      flake_borders[-1].append((start[0][0], start[0][1], 0))
      flake_borders[-1].append((start[1][0], start[1][1], 1))
      state = 1

    next_edge = tuple(filter(lambda x: x[state] == flake_borders[-1][-1][:2], flake_edges))
    if len(next_edge) != 1:
      print("Wrong number of edges:", next_edge, len(flake_border))
      print(flake_edges)
      print(flake_border)
      print(next_edge)
      exit(1)
    next_edge = next_edge[0]
    flake_borders[-1].append((next_edge[1-state][0], next_edge[1-state][1], 1-state))
    flake_edges.remove(next_edge)
    state = 1-state
    if flake_borders[-1][-1] == flake_borders[-1][0]:
      flake_borders.append([])

  for i in range(1, 100):
    if not os.path.exists("flake{:02d}.dxf".format(i)):
      filename = "flake{:02d}.dxf".format(i)
      break

  drawing = dxf.drawing(filename)
  block = dxf.block(name='flake')
  for flake_border in flake_borders[:-1]:
    points = []
    for p in flake_border:
      points.append((dxf_scale*t(p[1] + p[0]/2 + 1/2), dxf_scale*t((p[0]-(1-2*p[2])/3)*r3/2)))
      state = -state
    block.add(dxf.polyline(points))
  drawing.blocks.add(block)
  drawing.add(dxf.insert('flake', insert=(0, 0)))
  drawing.save()
  print("Wrote", filename)

def tk_init():
  global w
  global cells
  global next_cells
  def keypress(event):
    if event.char==' ':
      growth_iter()
      draw_flake()
    if event.char=='r':
      for i in range(N):
        for j in range(N):
          cells[i][j] = 0;
      cells[0][0] = 1
      draw_flake()
    if event.char=='s':
      save_dxf()
    if event.char=='q':
      master.quit()

  def click(event):
    w.focus_set()

  master = Tk()
  w = Canvas(master, width=2*offset, height=2*offset)
  w.bind("<Button-1>", click)
  w.bind("<Key>", keypress)
  w.pack()

tk_init()

def get_neighbor_state(cells, i, j):
  """Return integer containing a neighbor's value in each bit level"""
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

def grow(cells, i, j):
  """Find connected component of snowflake"""
  if cells[i][j] == 0: return ({}, 0)
  flake = set()
  boundary = {(i, j)}
  size = 0

  while len(boundary) > 0:
    (i, j) = boundary.pop()
    if (i, j) in flake: continue

    flake.add((i, j))
    if (i, j) == (0, 0): size += 1
    elif i == 0: size += 6
    elif i == j: size += 6
    else: size += 12

    for (ni, nj) in neighbors(i, j):
      if cells[ni][nj] > 0 and (ni, nj) not in flake:
        boundary.add((ni, nj))

  return (flake, size)

def create_rules():
  """Generate freeze/thaw rules"""
  global rules
  rules = [[None]*64, [None]*64] # (current_state, sum_neighbor_states): prob
  for i in range(64):
    if rules[0][i] is not None: continue

    #  . .    . .    o .    . o    o o    . .    o .
    # .   .  o   .  o   .  o   .  o   .  o   o  o   o
    #  . .    . .    . .    . .    . .    . .    . .
    #   0      1      3      5      7      9      11
    #   1      6      6      6      6      3       6
    #
    #  . o    o o    . o    o o    o .    o o    o o
    # o   o  o   o  o   .  o   .  o   o  o   o  o   o
    #  . .    . .    . o    . o    . o    . o    o o
    #   13     15     21     23     27     31     63
    #    6      6      2      6      3      6      1

    ii = i
    for _ in range(6):
      rules[0][ii] = base_rules[0][i]
      ii = (ii>>1) + ((ii&1)<<5)
    for _ in range(6):
      rules[1][ii] = base_rules[1][i]
      ii = (ii>>1) + ((ii&1)<<5)

def draw_flake():
  w.delete("all")
  # find largest connected component
  max_size = 0
  max_flake = None
  total_c = sum(map(sum, cells))
  while max_size < total_c:
    j = randrange(N)
    i = randint(0,j)
    (flake, size) = grow(cells, i, j)
    if size > max_size:
      max_flake = flake
      max_size = size

  full_flake = set()
  for (i, j) in flake:
    draw_cells(i, j)
    full_flake.add((i, j))
    full_flake.add((-i, -j))
    full_flake.add((-j-i, i))
    full_flake.add((j+i, -i))
    full_flake.add((j, -j-i))
    full_flake.add((-j, j+i))
    full_flake.add((j, i))
    full_flake.add((-j, -i))
    full_flake.add((-i-j, j))
    full_flake.add((i+j, -j))
    full_flake.add((i, -i-j))
    full_flake.add((-i, i+j))

  global flake_edges
  flake_edges = set()
  for (i, j) in full_flake:
    for (ni, nj) in ((i, j+1), (i, j-1), (i+1, j), (i-1, j), (i+1, j-1),
        (i-1, j+1)):
      if (ni, nj) in full_flake: continue
      if (ni - i, nj - j) == (0, 1):
        flake_edges.add(((i, j), (i, j)))
      if (ni - i, nj - j) == (1, 0):
        flake_edges.add(((i+1, j-1), (i, j)))
      if (ni - i, nj - j) == (1, -1):
        flake_edges.add(((i+1, j-1), (i, j-1)))
      if (ni - i, nj - j) == (0, -1):
        flake_edges.add(((i, j-1), (i, j-1)))
      if (ni - i, nj - j) == (-1, 0):
        flake_edges.add(((i, j-1), (i-1, j)))
      if (ni - i, nj - j) == (-1, 1):
        flake_edges.add(((i, j), (i-1, j)))

  for edge in flake_edges:
    draw_edge(edge)

def growth_iter():
  """Grow the snowflake"""
  global cells
  global next_cells
  # grow snowflake
  for i, r in enumerate(cells[:-1]):
    for j, c in enumerate(r[:-1]):
      next_cells[i][j] = 0
      if shape=="hexagon" and i+j>=N/2: continue
      if random() < rules[cells[i][j]][get_neighbor_state(cells, i,j)]:
        next_cells[i][j] = 1
  cells, next_cells = next_cells, cells

def main():
  global cells
  global next_cells

  cells = [[0]*N for _ in range(N)]
  next_cells = [[0]*N for _ in range(N)]
  cells[0][0] = 1

  create_rules()

  draw_flake()

  print("Press SPACE to grow flake, 's' to save to .dxf file, and 'r' to reset")
  mainloop()

main()
