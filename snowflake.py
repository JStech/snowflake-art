#!/usr/bin/env python3
from tkinter import *

scale = 300
offset = 150
def t(x): return scale*x + offset

master = Tk()

w = Canvas(master, width=600, height=600)
w.pack()

snowflake = [(0.,0.), (1.,0.), (.5,3**.5/2)]

for _ in range(6):
    for i in range(len(snowflake), 0, -1):
        p1 = snowflake[i-1]
        p2 = snowflake[i-2]
        snowflake.insert(i-1, (p1[0]*2/3 + p2[0]*1/3, p1[1]*2/3 + p2[1]*1/3))
        midpoint = (p1[0]*1/2 + p2[0]*1/2, p1[1]*1/2 + p2[1]*1/2)
        perp = (p1[1] - p2[1], p2[0] - p1[0])
        snowflake.insert(i-1, (midpoint[0] + perp[0] * 3**0.5/6,
                midpoint[1] + perp[1] * 3**0.5/6))
        snowflake.insert(i-1, (p1[0]*1/3 + p2[0]*2/3, p1[1]*1/3 + p2[1]*2/3))

for i in range(len(snowflake)):
    w.create_line(t(snowflake[i-1][0]), t(snowflake[i-1][1]),
            t(snowflake[i][0]), t(snowflake[i][1]))

mainloop()
