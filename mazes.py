"""
The mazes.py file is where we design the actual layout of the maze.
We define it as a grid - using characters to represent walls, pellets and power pellets.
Then we use a function to convert this grid into real screen coordinates.
X = Wall
. = Pellet
O = Power Pellet
"""

from constants import (CELL_SIZE, MAZE_GRID_ROWS, MAZE_GRID_COLUMNS,
                       MAZE_LEVEL_START_X, MAZE_LEVEL_START_Y)

# Maze level #1:
# The rows number must be equal to the grid rows number minus 2 rows for user interface
# The colums number must be identical to the grid columns number


def calculate_maze_data(maze_level):
    "Calculate maze coordinates"
    walls = []
    pellets = []
    power_pellets = []
    # for i, row in enumerate(maze_level):
    #     print(i, len(row), row)
    #Iterate over each row of the maze level
    for row in range(MAZE_GRID_ROWS):
        # Iterate over each row of the column of the maze level
         for column in range(MAZE_GRID_COLUMNS):
            # Store the coordinates of the character[row][column]
            character = maze_level[row][column]
            # row count start from 0 to 25 (26 not included)
            # column count start from 0 to 32 (33 not included)
            # The following x,y formulas consider position when starting to count from 0
            character_x = MAZE_LEVEL_START_X + CELL_SIZE * column
            character_y = MAZE_LEVEL_START_Y - CELL_SIZE * row
            # If character = "X" - wall, append the coordinate of that wall to the walls list
            if character == "X":
                walls.append((character_x, character_y))
            # If character = "." - pellet, append the coordinate of that pellet to the pellets list
            elif character == ".":
                pellets.append((character_x, character_y))
            elif character == "O":
                power_pellets.append((character_x, character_y))
    # Return the lists with all the coordinates.
    # This allows us later to get this data in other files and store it as a variable
    return walls, pellets, power_pellets