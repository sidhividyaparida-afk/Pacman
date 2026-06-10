"""
Pac-Man in Python | @TheWannabeCoder

The renderer.py file is where all the drawing of static objects happens.
We use Turtle Graphics to create pens that draw walls, pellets, power pellets -
using the coordinates from our maze layout, and to draw the user interface on screen.
"""

import turtle 
from mazes import calculate_maze_data
from levels import Levels
from constants import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Pen(turtle.Turtle):
    "General pen"

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("silver")
        self.speed(0)
        self.level=Levels().maze_level_4()
        # Get all coordinates from the maze level
        self.walls, self.pellets, self.power_pellets = calculate_maze_data(self.level)

    def get_current_level(self):
        return self.level
        

class Wall(Pen):
    "Maze wall"

    def __init__(self):
        super().__init__()
        self.shape("wall.gif")
        # self.shapesize(0.8)
        # self.pencolor("white")
        # self.fillcolor("dodger blue")

    def draw(self):
        "Draw the wall on screen"
        # walls is a list of tuples, each tuple contains the x, y coordinates of a wall center
        # Iterate over each wall coordinate inside the walls list
        for x, y in self.walls:
            self.goto(x, y)
            # stamp the wall
            self.stamp()


class Pellet(Pen):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(0.35, 0.35)
        self.pencolor("white")
        self.fillcolor("gold")
        self.stamps = {}

    def draw(self):
        "Draw the pellet on screen"
        for x, y in self.pellets:
            self.goto(x, y)
            # stamp the pellet and save the stamp id of the coordinate in a variable
            stamp_id = self.stamp()
            # Add the coordinate to the dictionary and map it to the saved stamp_id
            self.stamps[(x, y)] = stamp_id

class PowerPellet(Pen):
    "Power pellet for Pac-Man to eat"

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(0.8, 0.8)
        self.pencolor("white")
        self.fillcolor("chartreuse")
        self.stamps = {}

    def draw(self):
        "Draw the pellet on screen"
        for x, y in self.power_pellets:
            self.goto(x, y)
             # stamp the pellet and save the stamp id of the coordinate in a variable
            stamp_id = self.stamp()
            # Add the coordinate to the dictionary and map it to the saved stamp_id
            self.stamps[(x, y)] = stamp_id


class UiPen(Pen):
    "UI pen for score and lives"

    def __init__(self):
        super().__init__()
        self.font = ("Courier", 20, "normal")

    def draw_ui_area(self):
        "UI Drawing"
        self.pensize(2)
        x = 0.9 * SCREEN_WIDTH / 2
        top_y = 0.98 * SCREEN_HEIGHT / 2
        bottom_y = top_y - 2 * CELL_SIZE
        self.goto(x, top_y)
        self.pendown()
        self.goto(-x, top_y)
        self.goto(-x, bottom_y)
        self.goto(x, bottom_y)
        self.goto(x, top_y)

    def write_score(self, score, lives, pellet_stamps, power_stamps):
        "Write score on screen"
        self.clear()
        msg = f"Score: {score}"
        self.goto(-0.7 * SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 2 * CELL_SIZE)
        self.write(msg, False, "left", self.font)
        # Game over
        if lives <= 0:
            self.clear()
            self.color("red")
            self.write(
                f"Game Over! Final Score: {score}", False, "left", self.font)
        # Game won
        if len(pellet_stamps) == 0 and len(power_stamps) == 0:
            self.clear()
            self.color("yellow")
            self.write(
                f"You Won! Final Score: {score}", False, "left", self.font)
    def write_lives(self, lives, pellet_stamps, power_stamps):
        "Write lives on screen"
        self.clear()
        msg = f"Lives: {lives}"
        self.goto(0.7 * SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 2 * CELL_SIZE)
        self.write(msg, False, "right", self.font)
        # Remove lives from screen
        if lives == 0 or (len(pellet_stamps) == 0 and len(power_stamps) == 0):
            self.reset()