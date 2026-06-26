"""
SNAKE -- a graphical arcade game (the Kami-2 fun project).

Built with ONLY the concepts taught in Kami-2:
  variables, strings, f-strings, if/elif/else, booleans,
  while/for loops, lists, dictionaries, functions, and the
  random module.  Plus Python's built-in 'turtle' module so
  the game has real graphics -- no classes / OOP anywhere.

HOW TO PLAY:
  Steer the snake with the ARROW KEYS.
  Eat the red food to grow and score points.
  Don't hit the walls or your own tail!
  Press SPACE to restart after a game over.
"""

import random
import turtle

# ----------------------------------------------------------------------
# SETTINGS (just numbers you can tweak)
# ----------------------------------------------------------------------

CELL = 20            # size of one grid square, in pixels
WIDTH = 600          # window width
HEIGHT = 600         # window height
START_DELAY = 0.12   # seconds between moves (smaller = faster)
SPEEDUP = 0.995      # delay multiplier each time you eat (gets faster)

# How many cells fit from the center to each edge.
HALF_X = (WIDTH // 2) - CELL
HALF_Y = (HEIGHT // 2) - CELL

# ----------------------------------------------------------------------
# GAME STATE (plain dictionaries and lists -- no classes)
# ----------------------------------------------------------------------

# The snake is a list of [x, y] points. The last item is the head.
game = {
    "snake": [[-2 * CELL, 0], [-CELL, 0], [0, 0]],
    "dx": CELL,          # current movement step in x
    "dy": 0,             # current movement step in y
    "food": [0, 0],
    "score": 0,
    "high": 0,
    "delay": START_DELAY,
    "playing": True,
    "running": True,     # False = window closing, stop the loop
}

# ----------------------------------------------------------------------
# SCREEN + DRAWING TURTLES
# ----------------------------------------------------------------------

screen = turtle.Screen()
screen.title("SNAKE  --  arrow keys to move")
screen.bgcolor("#10131a")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)        # turn off auto-animation; we update by hand

# One pen stamps every snake segment, another stamps the food.
pen = turtle.Turtle()
pen.shape("square")
pen.shapesize(stretch_wid=0.9, stretch_len=0.9)   # small gap between segments
pen.color("#7CFC00")
pen.penup()
pen.hideturtle()

food_pen = turtle.Turtle()
food_pen.shape("circle")
food_pen.color("#ff4d4d")
food_pen.penup()
food_pen.hideturtle()

writer = turtle.Turtle()
writer.color("white")
writer.penup()
writer.hideturtle()


# ----------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------

def random_food():
    """Pick a random grid-aligned spot for the food."""
    x = random.randint(-HALF_X // CELL, HALF_X // CELL) * CELL
    y = random.randint(-HALF_Y // CELL, HALF_Y // CELL) * CELL
    return [x, y]


def draw_score():
    writer.clear()
    writer.goto(0, HALF_Y - 5)
    writer.write(f"Score: {game['score']}    High: {game['high']}",
                 align="center", font=("Courier", 16, "bold"))


def draw_everything():
    """Redraw the snake, the food and the score for one frame."""
    pen.clearstamps()
    for point in game["snake"]:
        pen.goto(point[0], point[1])
        pen.stamp()
    food_pen.clearstamps()
    food_pen.goto(game["food"][0], game["food"][1])
    food_pen.stamp()
    draw_score()
    screen.update()


def show_game_over():
    writer.goto(0, 20)
    writer.write("GAME OVER", align="center", font=("Courier", 32, "bold"))
    writer.goto(0, -25)
    writer.write("press SPACE to play again",
                 align="center", font=("Courier", 14, "normal"))
    screen.update()


# ----------------------------------------------------------------------
# DIRECTION CONTROLS (can't reverse straight back on yourself)
# ----------------------------------------------------------------------

def go_up():
    if game["dy"] == 0:
        game["dx"], game["dy"] = 0, CELL


def go_down():
    if game["dy"] == 0:
        game["dx"], game["dy"] = 0, -CELL


def go_left():
    if game["dx"] == 0:
        game["dx"], game["dy"] = -CELL, 0


def go_right():
    if game["dx"] == 0:
        game["dx"], game["dy"] = CELL, 0


def restart():
    """Reset everything to start a fresh run."""
    if game["playing"]:
        return            # only allowed after a game over
    game["snake"] = [[-2 * CELL, 0], [-CELL, 0], [0, 0]]
    game["dx"], game["dy"] = CELL, 0
    game["food"] = random_food()
    game["score"] = 0
    game["delay"] = START_DELAY
    game["playing"] = True


def quit_game():
    game["running"] = False


# ----------------------------------------------------------------------
# ONE STEP OF THE GAME
# ----------------------------------------------------------------------

def step():
    head = game["snake"][-1]
    new_head = [head[0] + game["dx"], head[1] + game["dy"]]

    # Hit a wall?
    if (new_head[0] > HALF_X or new_head[0] < -HALF_X or
            new_head[1] > HALF_Y or new_head[1] < -HALF_Y):
        game["playing"] = False
        show_game_over()
        return

    # Hit yourself?
    if new_head in game["snake"]:
        game["playing"] = False
        show_game_over()
        return

    # Move: add the new head.
    game["snake"].append(new_head)

    # Did we eat the food?
    if new_head == game["food"]:
        game["score"] += 1
        if game["score"] > game["high"]:
            game["high"] = game["score"]
        game["delay"] *= SPEEDUP
        # Put food somewhere that isn't on the snake.
        food = random_food()
        while food in game["snake"]:
            food = random_food()
        game["food"] = food
    else:
        # Didn't eat -> drop the tail so length stays the same.
        del game["snake"][0]

    draw_everything()


# ----------------------------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------------------------

def tick():
    """Run one frame, then ask the turtle clock to call us again.

    Using screen.ontimer (instead of a while + time.sleep loop) keeps
    the keyboard responsive, because turtle stays free to handle key
    presses between frames.
    """
    if not game["running"]:
        return
    if game["playing"]:
        step()
    screen.ontimer(tick, int(game["delay"] * 1000))


def main():
    # Hook up the keys.
    screen.listen()
    screen.onkey(go_up, "Up")
    screen.onkey(go_down, "Down")
    screen.onkey(go_left, "Left")
    screen.onkey(go_right, "Right")
    screen.onkey(restart, "space")
    screen.onkey(quit_game, "q")

    game["food"] = random_food()
    draw_everything()

    tick()              # start the loop
    screen.mainloop()   # hand control to turtle's event loop


if __name__ == "__main__":
    try:
        main()
    except turtle.Terminator:
        pass   # window was closed -- exit quietly
