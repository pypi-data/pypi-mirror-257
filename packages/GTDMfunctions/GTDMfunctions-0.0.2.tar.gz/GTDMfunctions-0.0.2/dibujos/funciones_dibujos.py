from turtle import *
import time

def rectangulo(num, long, ang=0, inc=0.0, cuadrado=True, long1=0, tspeed=10, sleep=60,  multicolor=False, tcolor="black"):
    if multicolor:
        colors = [
            "#880000",
            "#884400",
            "#888800",
            "#008800",
            "#008888",
            "#000088",
            "#440088",
            "#880088"
        ]
    else:
        colors = [tcolor]

    for i in range(num):
        speed(tspeed)
        color(colors[i % len(colors)])  # Use modulo to cycle through colors
        if cuadrado:
            for a in range(4):
                forward(long)
                right(90)
            right(ang)
            long += inc
        else:
            for a in range(2):
                forward(long)
                right(90)
                forward(long1)
                right(90)
            right(ang)
            long += inc
            long1 += inc

    time.sleep(sleep)