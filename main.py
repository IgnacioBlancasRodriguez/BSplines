import pygame as pg
from BSplines import *
import math

pg.init()

# Constants
WIDTH, HEIGHT = 600, 600
BLACK = pg.Color((0, 0, 0))
RADIUS = 6

w = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("B-Splines")

def main():
    inApp = True
    clock = pg.time.Clock()
    clock.tick(120)

    points = [(100, 200), (100, 300), (200, 300), (200, 400), (250, 450)]

    areDragged = [False for _ in points]
    
    while inApp:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                inApp = False
        if pg.mouse.get_pressed()[0]:
            mouse_pos = pg.mouse.get_pos()
            for i in range(0, len(points)):
                if (areDragged[i] == False and
                    math.sqrt((mouse_pos[0] - points[i][0])**2 +
                              (mouse_pos[1] - points[i][1])**2) <= RADIUS):
                    areDragged[i] = True
                if (areDragged[i] == True):
                    points[i] = mouse_pos
        else:
            areDragged = [False for _ in points]
        
        w.fill(BLACK)
        for i in range(0, len(points) - 1):
            pg.draw.line(w, pg.Color((255, 255, 255)), points[i], points[i + 1])
        for i in range(0, len(points)):
            pg.draw.circle(w, pg.Color((255, 255, 255)), points[i], RADIUS)
        draw_b_spline(w, points, pg.Color((255, 0, 255)))
        draw_derivative_vectors(w, points, pg.Color((255, 0, 0)))
        pg.display.update()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        quit()