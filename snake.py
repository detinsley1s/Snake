#!/usr/bin/env python3

"""Snake
Programmed by Daniel Tinsley
Copyright 2016

The classic snake game.
"""

from collections import deque
import random
import sge

# dimensions of window
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

# dimensions of snake segments
SNAKE_HEIGHT = 15
SNAKE_WIDTH = 15

# speed of snake's movement
SNAKE_SPEED = 1


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
        elif key == 'n':
            start_new_game().start()

    def event_close(self):
        """Close the application."""
        self.end()


class Snake(sge.dsp.Object):
    """This class is responsible for the snake.

    Subclass of sge.dsp.Object

    Method:
    change_direction

    Instance variables:
    direction -- the direction that the snake's head is moving
    x -- the x location of the snake's head
    y -- the y location of the snake's head
    """

    def __init__(self):
        """

        """
        x = WINDOW_WIDTH // 2
        y = (WINDOW_HEIGHT - 100) // 2
        super().__init__(x, y, sprite=SNAKE_HEAD)
        #self.body_coords = [(x, y)]
        self.body_parts = []
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        if self.direction == 'up':
            self.yvelocity = -SNAKE_SPEED
        elif self.direction == 'down':
            self.yvelocity = SNAKE_SPEED
        elif self.direction == 'left':
            self.xvelocity = -SNAKE_SPEED
        else:
            self.xvelocity = SNAKE_SPEED
        self.tail_direction = self.direction
        self.predirections = deque()
        self.game_in_progress = True

    def event_key_press(self, key, char):
        """Detect when a key is pressed on the keyboard.

        Overrides method from superclass sge.dsp.Game

        Parameters:
        key -- the identifier string of the key that was pressed
        char -- the Unicode character associated with the key press
        """
        if self.game_in_progress:
            if key == 'up' and self.direction != 'down':
                self.predirections.clear()
                self.predirections.append(self.direction)
                self.yvelocity = -SNAKE_SPEED
                self.xvelocity = 0
                self.direction = key
            elif key == 'down' and self.direction != 'up':
                self.predirections.clear()
                self.predirections.append(self.direction)
                self.yvelocity = SNAKE_SPEED
                self.xvelocity = 0
                self.direction = key
            elif key == 'left' and self.direction != 'right':
                self.predirections.clear()
                self.predirections.append(self.direction)
                self.xvelocity = -SNAKE_SPEED
                self.yvelocity = 0
                self.direction = key
            elif key == 'right' and self.direction != 'left':
                self.predirections.clear()
                self.predirections.append(self.direction)
                self.xvelocity = SNAKE_SPEED
                self.yvelocity = 0
                self.direction = key
            elif key == 'q':
                self.lengthen_body()
        
    def event_step(self, time_passed, delta_mult):
        if self.game_in_progress:
            if not self.predirections:
                self.predirections.append(self.direction)
            for idx, part in enumerate(self.body_parts):
                if idx == 0:
                    if self.direction in ('up', 'down'):
                        x_add = 0
                        y_add = 1#SNAKE_HEIGHT - 1
                    else:
                        x_add = 1#SNAKE_WIDTH - 1
                        y_add = 0
                    if self.direction in ('down', 'right'):
                        x_add = -x_add
                        y_add = -y_add
                    self.predirections.append(self.body_parts[0].direction)
                    part.update(self.xprevious+x_add, self.yprevious+y_add, self.predirections.popleft())
                else:
                    if self.body_parts[idx-1].direction in ('up', 'down'):
                        x_add = 0
                        y_add = 1
                    else:
                        x_add = 1
                        y_add = 0
                    if self.body_parts[idx-1].direction in ('down', 'right'):
                        x_add = -x_add
                        y_add = -y_add
                    self.predirections.append(self.body_parts[idx].direction)
                    part.update(self.body_parts[idx-1].x+x_add, self.body_parts[idx-1].y+y_add, self.predirections.popleft())
                sge.game.project_sprite(part.sprite, 0, part.x, part.y)
            self.predirections.clear() 
        if(self.bbox_top < 10 or self.bbox_left < 10 or
                self.bbox_bottom > WINDOW_HEIGHT - 109 or
                self.bbox_right > WINDOW_WIDTH - 9):
            self.game_end()

    def game_end(self):
        self.yvelocity = 0
        self.xvelocity = 0
        for part in self.body_parts:
            part.active = False
        
        sge.game.project_text(
            GAME_OVER_FONT, 'You Died. Game. Over.', 155,
            (WINDOW_HEIGHT - 106) // 3, color=sge.gfx.Color('black'),
            halign='middle', valign='middle'
        )
        sge.game.project_text(
            GAME_OVER_INSTRUCTIONS,
            'N -- New Game\nH -- High Scores\nESC -- Quit', 330,
            (WINDOW_HEIGHT - 56) // 2, color=sge.gfx.Color('black'),
            halign='middle', valign='middle'
        )
        self.game_in_progress = False

    def event_collision(self, other, xdirection, ydirection):
        if isinstance(other, Pellet) or isinstance(other, SnakeBodyPart):
            self.game_end()

    def lengthen_body(self):
        tail = self.body_parts[-1] if self.body_parts else self
        self.tail_direction = tail.direction
        for i in range(15):
            while True:
                if self.tail_direction in ('up', 'down'):
                    x_add = 0
                    y_add = 1# if self.body_parts else SNAKE_HEIGHT
                else:
                    x_add = 1# if self.body_parts else SNAKE_WIDTH
                    y_add = 0
                if self.tail_direction in ('down', 'right'):
                    x_add = -x_add
                    y_add = -y_add
                x = self.body_parts[-1].x + x_add if self.body_parts else self.x - x_add
                y = self.body_parts[-1].y + y_add if self.body_parts else self.y - y_add
                if y > 11 and x + SNAKE_WIDTH < WINDOW_WIDTH - 10 and x > 11 and y + SNAKE_HEIGHT < WINDOW_HEIGHT - 110:
                    break
                else:
                    if self.tail_direction == 'up':
                        self.tail_direction = 'right'
                    elif self.tail_direction == 'right':
                        self.tail_direction = 'down'
                    elif self.tail_direction == 'down':
                        self.tail_direction = 'left'
                    else:
                        self.tail_direction = 'up'

            # Used to only have every 15th body part be collidable to help
            # the frame rate. Also, the first sections can't be collidable
            # since they overlap the head, which is the area that detects
            # collisions.
            tangible = i == 14 and len(self.body_parts) > 20
            self.body_parts.append(SnakeBodyPart(x, y, self.tail_direction, tangible))
            obj = self.body_parts[-1]
            sge.game.current_room.add(obj)


class SnakeBodyPart(sge.dsp.Object):
    def __init__(self, x, y, direction, tangible):
        super().__init__(x, y, sprite=SNAKE_BODY, tangible=tangible)
        self.direction = direction

    def update(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


class Pellet(sge.dsp.Object):
    def __init__(self, x=100, y=100):
        super().__init__(x, y, sprite=SNAKE_HEAD)


def start_new_game():
    snake = Snake()
    return sge.dsp.Room([snake], background=BACKGROUND)

# Construct a Game object so the game can begin
Game(
    width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
    window_text='Snake by Dan Tinsley', fps=250,
)

# Create the font
GAME_OVER_FONT = sge.gfx.Font(name='fonts/horta.ttf', size=72)
GAME_OVER_INSTRUCTIONS = sge.gfx.Font(name='fonts/horta.ttf', size=32)

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
SNAKE_BODY = (
    sge.gfx.Sprite(width=SNAKE_WIDTH, height=SNAKE_HEIGHT)
)
SNAKE_BODY.draw_rectangle(
    0, 0, SNAKE_BODY.width, SNAKE_BODY.height, fill=sge.gfx.Color('green')
)

# Instantiate the board with specified background colors
LAYERS = [sge.gfx.BackgroundLayer(GAME_BOARD, 0, 0)]
BACKGROUND = sge.gfx.Background(LAYERS, sge.gfx.Color('red'))
sge.game.start_room = start_new_game()

if __name__ == '__main__':
    sge.game.start()
