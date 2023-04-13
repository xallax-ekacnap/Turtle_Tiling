from math import sin, cos, pi, asin
import turtle
import time
import itertools

class CleanMove:
    def __init__(self, t):
        self.t = t

    def __enter__(self):
       self.t.penup()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.t.pendown()

class SavePosition:
    def __init__(self, t):
        self.t = t

        self.heading = t.heading()
        self.position = t.position()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with CleanMove(self.t):
            self.t.setheading(self.heading)
            self.t.setposition(self.position)


def rad(deg):
    return deg*pi/180


def deg(rad):
    return rad*180/pi

    
def shape(t, S=200, sides=3):
    degrees = (sides - 2)*180
    for i in range(sides):
        t.forward(S)
        t.left(180-(degrees/sides))


def calc(S, F, sides=3):
    int_angle = (sides - 2)*180/sides
    G = sin(rad(int_angle)) * F
    I = cos(rad(int_angle)) * F
    J = S - F - I
    D = (J**2 + G**2)**(1/2)
    A = deg(asin(G/D))
    return A, D


def lspiral(t, S, F, sides=3):
    with SavePosition(t):
        while int(S) > F:
            shape(t, S, sides=sides)
            t.forward(F)
            A, S = calc(S, F, sides=sides)
            t.left(A)


def rspiral(t, S, F, sides=3):
    angle = (sides - 2)*180 / sides
    with SavePosition(t):
        while int(S) > F:
            shape(t, S, sides=sides)
            t.forward(S - F)
            A, S = calc(S, F, sides=sides)
            t.left(180 - angle - A)

def quad_tile(t, S, F, rows=1, cols=1):
    for r in range(rows):
        for c in range(cols):
            with SavePosition(t):
                t.forward(c * S)
                if (r + c) % 2 == 0:
                    lspiral(t, S, F, sides=4)
                else:
                    rspiral(t, S, F, sides=4)
        t.setposition(t.xcor(), t.ycor() + S)


def circle(t, S=0.5):
    shape(t, S, sides=1000)


def write_drawing(screen, file_name, turtle_pos, t):
    ts = turtle.getscreen()
    ts.getcanvas().postscript(file=file_name)
    t.goto(turtle_pos)
    screen.clear()


def get_screen():
    screen = turtle.Screen()
    t = turtle.Turtle()
    turtle.tracer(n=0, delay=None)
    # t.color('black')
    with CleanMove(t):
        t.goto((-500, -500))
    screen.colormode(255)
    return t
