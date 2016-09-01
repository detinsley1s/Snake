#!/usr/bin/env python3

"""Snake
Programmed by Daniel Tinsley
Copyright 2016

The classic snake game.
"""

import random
import sge


# dimensions of window
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

# dimensions of snake segments
SNAKE_HEIGHT = 20
SNAKE_WIDTH = 20


class Game(sge.dsp.Game):
    """This class handles most of the game which work globally.

    Subclass of sge.dsp.Game

    Methods:
    event_close
    event_key_press
    """

    def event_key_press(self, key, char):
        """Detect when a key is pressed on the keyboard.

        Overrides method from superclass sge.dsp.Game

        Parameters:
        key -- the identifier string of the key that was pressed
        char -- the Unicode character associated with the key press
        """
        if key == 'escape':
            self.event_close()
        elif key in ('up', 'down', 'left', 'right'):
            self.move_snake(key)

    def event_close(self):
        """Close the application."""
        self.end()

    def move_snake(self, direction):
        """Move the snake in the specified direction.

        Parameter:
        direction -- the direction to move the snake
        """
        if direction == 'up':
            snake.y -= 10
        elif direction == 'down':
            snake.y += 10
        elif direction == 'left':
            snake.x -= 10
        else:
            snake.x += 10


class Room(sge.dsp.Room):
    """This class stores the settings and objects found in a level.

    Subclass of sge.dsp.Room

    Method:
    event_step
    """

    def event_step(self, time_passed, delta_mult):
        """Do level processing once each frame.

        Overrides method from superclass sge.dsp.Room

        Parameters:
        time_passed -- the total milliseconds that have passed during
                       the last frame
        delta_mult -- what speed and movement should be multiplied by
                      this frame due to delta timing
        """
        # Display the game board
        sge.game.project_sprite(snake.sprite, 0, snake.x, snake.y)
        #print(sge.mouse.get_x(), sge.mouse.get_y())


class Snake(sge.dsp.Object):
    """This class is responsible for the snake.

    Subclass of sge.dsp.Object
    """

    def __init__(self, x=WINDOW_WIDTH//2, y=(WINDOW_HEIGHT-100)//2):
        """

        Parameters:
        x_loc -- the x location of the snake's head 
        y_loc -- the y location of the snake's head
        """
        super().__init__(x, y, sprite=SNAKE_HEAD)


class GameBoard:
    """This class is responsible for the gameboard and all its functions.

    """

    def __init__(self):
        pass


# Construct a Game object so the game can begin
Game(
    width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
    window_text='Snake by Dan Tinsley'
)

# Create the game board
GAME_BOARD = (
    sge.gfx.Sprite(width=WINDOW_WIDTH, height=WINDOW_HEIGHT - 100)
)
GAME_BOARD.draw_rectangle(
    0, 0, GAME_BOARD.width, GAME_BOARD.height,
    outline=sge.gfx.Color("black"), fill=sge.gfx.Color("white"),
    outline_thickness=20
)

# Create snake sprites
SNAKE_HEAD = (
    sge.gfx.Sprite(width=SNAKE_WIDTH, height=SNAKE_HEIGHT)
)
SNAKE_HEAD.draw_rectangle(
    0, 0, SNAKE_HEAD.width, SNAKE_HEAD.height,
    outline=sge.gfx.Color('black'), fill=sge.gfx.Color('yellow')
)

snake = Snake()

# Instantiate the board with specified background colors
LAYERS = [sge.gfx.BackgroundLayer(GAME_BOARD, 0, 0)]
BACKGROUND = sge.gfx.Background(LAYERS, sge.gfx.Color('red'))
sge.game.start_room = Room([snake], background=BACKGROUND)

sge.game.mouse.visible = True

if __name__ == '__main__':
    sge.game.start()
