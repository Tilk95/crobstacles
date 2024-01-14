import turtle


def canvas_builder(title, canvas_width, canvas_height, square_length):
    CANVAS_COLOR = "red"
    PEN_COLOR = "black"
    scr = turtle.Screen()
    turtle.speed(6)
    turtle.resizemode("auto")

    scr.screensize(canvas_width, canvas_height)
    scr.title(title)
    scr.bgcolor(CANVAS_COLOR)
    turtle.setworldcoordinates(-canvas_width*2, -canvas_height*2, canvas_width, canvas_height)
    t = turtle.Turtle()
    t.color(PEN_COLOR)
    t.begin_fill()
    t.hideturtle()
    for i in range(4):
        t.forward(square_length)
        t.left(90)
    t.end_fill()
    t.showturtle()
    turtle.done()


canvas_builder("Test", 500, 500, 200)
