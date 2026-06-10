"""
Pac-Man in Python

The main.py file is the starting point of the game.
It's where everything gets set up and launched
"""

import turtle
import random
import winsound
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ENEMY_NUMBER
from renderer import Wall, Pellet, PowerPellet, UiPen
from actors import Player, Enemy

def init_screen():
    "Initialize main screen, and returns it when called"
    # Create the game screen and store it in a variable screen
    screen = turtle.Screen()
    # Disable auto screen update
    screen.tracer(0)
    screen.title("Pac-Man in Python")
    screen.setup(SCREEN_WIDTH + 10, SCREEN_HEIGHT +10)
    screen.bgcolor("black")
    return screen


def bind_controls(screen, player, level):
    "Keyboard & mouse bindings"
    # Tell the screen to be aware for keyboard or mouse clicks
    screen.listen()
    # Bind controls
    screen.onkeypress(lambda: move(player, level, "R"), "Right")
    screen.onkeypress(lambda: move(player, level, "L"), "Left")
    screen.onkeypress(lambda: move(player, level, "U"), "Up")
    screen.onkeypress(lambda: move(player, level, "D"), "Down")

def move(player, level, direction):
    row, col = player.get_maze_index()
    if direction == "R":
        # print(level[row][col+1], row, col)
        if col + 1 < len(level[row]) and level[row][col+1] != "X":
            player.turn_right()
    elif direction == "L":
        # print(level[row][col-1], row, col)
        if col - 1 >= 0 and level[row][col-1] != "X":
            player.turn_left()
    elif direction == "U":
        # print(level[row-1][col], row, col)
        if row - 1 >= 0 and level[row-1][col] != "X":
            player.turn_up()
    elif direction == "D":
        # print(level[row+1][col], row, col)
        if row + 1 < len(level) and level[row+1][col] != "X":
            player.turn_down()

def game_loop(screen, player, score_pen, lives_pen, pellet_pen, power_pen, player_start_x, player_start_y, enemies):
    """
    This is the game engine.
    Keeps everything moving, updating and reacting in real time.
    """
    # Write UI on screen
    score_pen.write_score(player.score, player.lives, pellet_pen.stamps, power_pen.stamps)
    lives_pen.write_lives(player.lives, pellet_pen.stamps, power_pen.stamps)
    # Pellets check
    for (px, py), stamp_id in list(pellet_pen.stamps.items()):
        if player.distance(px, py) < CELL_SIZE / 2 and (px, py) != (player_start_x, player_start_y):
            winsound.PlaySound("eat.wav", winsound.SND_ASYNC)
            pellet_pen.clearstamp(stamp_id)
            del pellet_pen.stamps[(px, py)]
            player.score += 2
        # Skip points on game start from first pellet
        elif player.distance(px, py) < CELL_SIZE / 2 and (px, py) == (player_start_x, player_start_y):
            pellet_pen.clearstamp(stamp_id)
            del pellet_pen.stamps[(px, py)]

    # Power pellets check
    for (px, py), stamp_id in list(power_pen.stamps.items()):
        if player.distance(px, py) < CELL_SIZE / 2:
            winsound.PlaySound("eat.wav", winsound.SND_ASYNC)
            power_pen.clearstamp(stamp_id)
            del power_pen.stamps[(px, py)]
            player.score += 50
            # Speed boost
            player.move_speed += 3
            screen.ontimer(player.reset_speed, 3000)

    player.move()
    player.check_wall_collision()
    # Update enemies
    for enemy in enemies:
        enemy.move()
        enemy.check_wall_collision()
        enemy.go_after_player()
        # Check collision with player
        if enemy.distance(player) < CELL_SIZE / 2:
            winsound.PlaySound("death.wav", winsound.SND_ASYNC)
            # Ensure player does not spawn near enemy
            safe_spots = []
            for pellet in pellet_pen.pellets:
                if all(enemy.distance(pellet) > CELL_SIZE * 5 for enemy in enemies):
                    safe_spots.append(pellet)
            player.goto(random.choice(safe_spots))
            player.lives -= 1
            player.state = "stop"
    # Win game - stop everything and close the game
    if len(power_pen.stamps) == 0 and len(pellet_pen.stamps) == 0:
            player.state = "stop"
            for enemy in enemies:
                enemy.hideturtle()
                enemy.state = "stop"
            screen.ontimer(screen.bye, 3000)
    # Game over - stop everything and close the game
    if player.lives == 0:
        player.state= "stop"
        player.hideturtle()
        for enemy in enemies:
            enemy.state = "stop"
        screen.ontimer(screen.bye, 3000)
    # Update screen
    screen.update()
    screen.ontimer(lambda: game_loop(screen, player, score_pen, lives_pen, pellet_pen, power_pen, player_start_x, player_start_y, enemies),1000//60)


def main():
    """
    This function starts the game, it sets everything up - the screen, the players and levels.
    After setting up, it kicks off the game loop where things move and interact.
    """
    # Call the screen initiation function
    screen = init_screen()
    screen.register_shape("pac.gif")
    screen.register_shape("up.gif")
    screen.register_shape("down.gif")
    screen.register_shape("left.gif")
    screen.register_shape("right.gif")
    screen.register_shape("ghost1.gif")
    screen.register_shape("ghost2.gif")
    screen.register_shape("ghost3.gif")
    screen.register_shape("ghost4.gif")
    screen.register_shape("wall.gif")
    # Create rendering instances
    wall_pen = Wall()
    pellet_pen = Pellet()
    power_pen = PowerPellet()
    ui_pen = UiPen()
    score_pen = UiPen()
    lives_pen = UiPen()

    # Call the instance functions
    wall_pen.draw()
    walls = wall_pen.walls
    pellet_pen.draw()
    pellets = pellet_pen.pellets
    power_pen.draw()
    level = wall_pen.get_current_level()
    ui_pen.draw_ui_area()

     # Player starting position (on random pellet)
    player_start_coor = random.choice(pellet_pen.pellets)
    player_start_x = player_start_coor[0]
    player_start_y = player_start_coor[1]
    # Create Pac-Man
    player = Player(walls)
    player.goto(player_start_x, player_start_y)
    # Create Enemies
    enemy_colours = ["ghost1.gif", "ghost2.gif", "ghost3.gif", "ghost4.gif"]
    enemies = []
    for  _ in range(ENEMY_NUMBER):
        safe_spots = []
        for pellet in pellets:
            if player.distance(pellet) > CELL_SIZE * 5:
                safe_spots.append(pellet)
        enemy_start_x, enemy_start_y = random.choice(safe_spots)
        enemy = Enemy(enemy_start_x, enemy_start_y, walls, player)
        enemy.shape(random.choice(enemy_colours))
        enemies.append(enemy)
    # Start of the game settings
    winsound.PlaySound("start_up.wav", winsound.SND_ASYNC)
    screen.ontimer(lambda: bind_controls(screen, player, level), 2500)
    for enemy in enemies:
        screen.ontimer(enemy.start_move, 2500)
    # Game loop - moving things(Real time update)
    game_loop(screen, player, score_pen, lives_pen, pellet_pen, 
              power_pen, player_start_x, player_start_y, enemies)
    # Keeps the main screen open
    screen.mainloop()


# This makes sure the game only starts when we run this file directly-
# not if it's being imported as a module in another file.
if __name__ == "__main__":
    main()