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

    def event_close(self):
        """Close the application."""
        self.end()


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
        pass


# Construct a Game object so the game can begin
Game(
    width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
    window_text='Snake by Dan Tinsley'
)

# Instantiate the board with a specified background color
BACKGROUND = sge.gfx.Background([], sge.gfx.Color('blue'))
sge.game.start_room = Room([], background=BACKGROUND)

if __name__ == '__main__':
    sge.game.start()
