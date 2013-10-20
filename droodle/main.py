# -*- encoding: utf-8 -*-
from functools import reduce

__author__ = 'pahaz'

from tkinter import Tk, Canvas, Button, ALL
from random import randrange, shuffle, choice, randint
from time import sleep
from datetime import datetime
import string
import math

def broodle_name():
    return ''.join([choice(string.ascii_letters) for x in range(10)])

class Художник():
    def нарисуй_точку(self, холст, x, y, r=10):
        холст.create_oval(x-r,y-r,x+r,y+r, width=3, outline='blue', fill='white')

    def нарисуй_друдл(self, convas):
        convas.delete(ALL)
        points = [(x*100, y*100) for x in range(5) for y in range(5) if (y+x)*100 not in [0, 100, 300, 600, 700]]
        # for x,y in points:
        #     self.нарисуй_точку(холст, x, y)

        shuffle(points)
        count = choice([2,2,3,3,3,4,4,4,4,5,5,6])
        print(count)
        cool = points[:count]
        cool_larallel = [(400-x[0], x[1]) for x in cool]

        x1, y1 = sum([a[0] for a in cool]) / len(cool), \
                 sum([a[1] for a in cool]) / len(cool)
        x2, y2 = sum([a[0] for a in cool_larallel]) / len(cool), \
                 sum([a[1] for a in cool_larallel]) / len(cool)

        distance = int(((math.sqrt((x1 - x2)**2 + (y1-y2)**2)) - 10) / 2)
        r = randint(20, distance) if distance > 20 else distance
        r = randint(10, 150) if distance < 2 else distance

        convas.create_line(*cool, width=3, fill='blue')
        convas.create_line(*cool_larallel, width=3, fill='blue')
        self.нарисуй_точку(convas,  x1, y1, r)
        self.нарисуй_точку(convas,  x2, y2, r)
        #convas.postscript(file=broodle_name()+".eps")

архип = Художник()
окно = Tk()
окно.title('Друдлы')
окно.geometry('800x600')

холст = Canvas(окно, bg='white', width=395, height=395)
холст.pack()

def cледующий(событие):
    архип.нарисуй_друдл(холст)

кнопка = Button(окно, text="Друдл!")
кнопка.bind("<Button-1>", cледующий)
кнопка.pack()

окно.mainloop()
