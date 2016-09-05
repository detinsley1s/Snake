#!/usr/bin/env python3

"""Snake
Programmed by Daniel Tinsley
Copyright 2016

The classic snake game.
"""

from collections import deque
import random
import shelve

import sge

# dimensions of window
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

# dimensions of sprites
SPRITE_HEIGHT = 15
SPRITE_WIDTH = 15

# speed of snake's movement
SNAKE_SPEED = 15


class Game(sge.dsp.Game):
    """This class handles most parts of the game which work globally.

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
    """This class is responsible for the processing of the snake.

    Subclass of sge.dsp.Object

    Methods:
    change_direction
    event_collision
    event_key_press
    event_step
    lengthen_body

    Instance variables:
    body_parts -- list of SnakeBodyPart objects
    direction -- string denoting the direction that the snake's head is
                 moving
    is_alive -- boolean denoting if the snake is alive or dead
    predirections -- collections.deque object acting as storage of the
                     directions of the prior two body parts that moved
    tail_direction -- string denoting the direction the snake's tail is
                      moving
    x -- integer for the x location of the snake's head
    xvelocity -- integer for the velocity of the snake in the x
                 direction
    y -- integer for the y location of the snake's head
    yvelocity -- integer for the velocity of the snake in the y
                 direction
    """

    def __init__(self):
        """Initialize the variables of the snake and its behavior."""
        x_loc = WINDOW_WIDTH // 2
        y_loc = (WINDOW_HEIGHT - 100) // 2
        super().__init__(x_loc, y_loc, sprite=SNAKE_HEAD)
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
        self.is_alive = True
        self.predirections = deque()

    def event_key_press(self, key, char):
        """Detect when a key is pressed on the keyboard.

        Overrides method from superclass sge.dsp.Game

        Parameters:
        key -- the identifier string of the key that was pressed
        char -- the Unicode character associated with the key press
        """
        if self.is_alive:
            if key == 'up' and self.direction not in ('up', 'down'):
                self.snake_turned(key)
                self.yvelocity = -SNAKE_SPEED
                self.xvelocity = 0
            elif key == 'down' and self.direction not in ('up', 'down'):
                self.snake_turned(key)
                self.yvelocity = SNAKE_SPEED
                self.xvelocity = 0
            elif key == 'left' and self.direction not in ('left', 'right'):
                self.snake_turned(key)
                self.xvelocity = -SNAKE_SPEED
                self.yvelocity = 0
            elif key == 'right' and self.direction not in ('left', 'right'):
                self.snake_turned(key)
                self.xvelocity = SNAKE_SPEED
                self.yvelocity = 0

    def snake_turned(self, key):
        """Track the snake's new direction and its prior direction.

        Parameter:
        key -- string denoting the snake head's new direction
        """
        self.predirections.clear()
        self.predirections.append(self.direction)
        self.direction = key

    def event_step(self, time_passed, delta_mult):
        """Do level processing once each frame to track the snake.

        Overrides method from superclass sge.dsp.Room

        Parameters:
        time_passed -- the total milliseconds that have passed during
                       the last frame
        delta_mult -- what speed and movement should be multiplied by
                      this frame due to delta timing
        """
        current_game.display_score()
        if self.is_alive:
            if current_game.score > 0:
                current_game.update_score(-1)
            if not self.predirections:
                self.predirections.append(self.direction)

            # Make the snake move and turn correctly
            for idx, part in enumerate(self.body_parts):
                x_add = 0
                y_add = 0
                self.predirections.append(self.body_parts[idx].direction)
                if idx == 0:
                    part.update(
                        self.xprevious, self.yprevious,
                        self.predirections.popleft()
                    )
                else:
                    if self.body_parts[idx-1].direction in ('up', 'down'):
                        y_add = 15
                    else:
                        x_add = 15
                    if self.body_parts[idx-1].direction in ('down', 'right'):
                        x_add = -x_add
                        y_add = -y_add
                    part.update(
                        self.body_parts[idx-1].x + x_add,
                        self.body_parts[idx-1].y + y_add,
                        self.predirections.popleft()
                    )
                sge.game.project_sprite(part.sprite, 0, part.x, part.y)
            self.predirections.clear()

        # Detect if the snake touched the screen's border
        if(self.bbox_top < 10 or self.bbox_left < 10 or
           self.bbox_bottom > WINDOW_HEIGHT - 110 or
           self.bbox_right > WINDOW_WIDTH - 10):
            current_game.game_end(self)

    def event_collision(self, other, xdirection, ydirection):
        """Process game state after a collision with an object occurs.

        Parameters:
        other -- the object with which the snake collided
        xdirection -- the horizontal direction of the collision
                      represented by -1 (left), 1 (right),
                      or 0 (no horizontal direction)
        ydirection -- the vertical direction of the collision
                      represented by -1 (left), 1 (right),
                      or 0 (no vertical direction)
        """
        if isinstance(other, SnakeBodyPart):
            current_game.game_end(self)
        elif isinstance(other, Pellet):
            pellet.set_new_location()
            self.lengthen_body()
            current_game.update_score(100)
            current_game.increment_round()

    def lengthen_body(self):
        """Increase the length of the snake by one segment."""
        tail = self.body_parts[-1] if self.body_parts else self
        self.tail_direction = tail.direction
        x_add = 0
        y_add = 0
        if tail != self:
            if self.tail_direction in ('up', 'down'):
                y_add = 15
            else:
                x_add = 15
            if self.tail_direction in ('down', 'right'):
                x_add = -x_add
                y_add = -y_add
        x_loc = tail.x + x_add
        y_loc = tail.y + y_add

        # The first three body parts aren't collideable. This should
        # help the game run even better by alerting that to the game.
        tangible = len(self.body_parts) > 3
        self.body_parts.append(
            SnakeBodyPart(x_loc, y_loc, self.tail_direction, tangible)
        )
        obj = self.body_parts[-1]
        sge.game.current_room.add(obj)


class SnakeBodyPart(sge.dsp.Object):
    """This class is responsible for the individual snake body parts.

    Subclass of sge.dsp.Object

    Methods:
    update

    Instance variables:
    direction -- string denoting the body part's movement direction
    x -- integer for the x location of the body part
    y -- integer for the y location of the body part
    """

    def __init__(self, x, y, direction, tangible):
        """Initialize the body part.

        Parameters:
        direction -- string for the first direction the part will move
        tangible -- boolean for if the part may be part of collisions
        x -- integer for the initial x location of the part
        y -- integer for the initial y location of the part
        """
        super().__init__(
            x, y, sprite=SNAKE_BODY, tangible=tangible,
            checks_collisions=False
        )
        self.direction = direction

    def update(self, x_loc, y_loc, direction):
        """Update the instance variables of the body part.

        Parameters:
        direction -- string for the new direction the part will move
        x_loc -- integer for the new x location of the part
        y_loc -- integer for the new y location of the part
        """
        self.x = x_loc
        self.y = y_loc
        self.direction = direction


class Pellet(sge.dsp.Object):
    """This class is responsible for the pellet that the snake eats.

    Subclass of sge.dsp.Object

    Methods:
    event_step
    set_new_location

    Instance variables:
    x -- integer for the x location of the pellet
    y -- integer for the y location of the pellet
    """

    def __init__(self):
        """Initialize the pellet on the screen in a random location."""
        x_loc = random.randrange(
            10, WINDOW_WIDTH - SPRITE_WIDTH - 10, SPRITE_WIDTH
        )
        y_loc = random.randrange(
            10, WINDOW_HEIGHT - SPRITE_HEIGHT - 110, SPRITE_HEIGHT
        )
        super().__init__(x_loc, y_loc, sprite=PELLET, checks_collisions=False)

    def set_new_location(self):
        """Place the pellet in a random location on the screen."""
        self.x = random.randrange(
            10, WINDOW_WIDTH - SPRITE_WIDTH - 10, SPRITE_WIDTH
        )
        self.y = random.randrange(
            10, WINDOW_HEIGHT - SPRITE_HEIGHT - 110, SPRITE_HEIGHT
        )

    def event_step(self, time_passed, delta_mult):
        """Do level processing once each frame to display the pellet.

        Overrides method from superclass sge.dsp.Room

        Parameters:
        time_passed -- the total milliseconds that have passed during
                       the last frame
        delta_mult -- what speed and movement should be multiplied by
                      this frame due to delta timing
        """
        sge.game.project_sprite(self.sprite, 0, self.x, self.y)


class CurrentGame:
    """This class is responsible for the game's data while it's running.

    Methods:
    display_score
    game_end
    increment_round
    update_score

    Instance variables:
    high_score -- integer for the overall highest score
    round -- integer for the snake's current length
    score -- integer for the game's current score
    """

    def __init__(self):
        """Initialize the score, round, and high score at game start."""
        self.score = 0
        self.round = 1
        with shelve.open('high_score.db') as h_score:
            if 'high_score' not in h_score:
                h_score['high_score'] = 0
            self.high_score = h_score['high_score']

    def update_score(self, additional_score):
        """Update the score.

        Parameter:
        change -- integer for the extra points to add to the score
        """
        self.score += additional_score

    def increment_round(self):
        """Increase the round number by one."""
        self.round += 1

    def display_score(self):
        """Display the current score, the round, and the high score."""
        sge.game.project_text(
            SCORE_FONT, 'Score\n{}'.format(self.score), 140,
            WINDOW_HEIGHT - 53, color=sge.gfx.Color('black'), halign='center',
            valign='middle'
        )
        sge.game.project_text(
            SCORE_FONT, 'Round\n{}'.format(self.round), 382,
            WINDOW_HEIGHT - 53, color=sge.gfx.Color('black'), halign='center',
            valign='middle'
        )
        sge.game.project_text(
            SCORE_FONT, 'High Score\n{}'.format(self.high_score), 625,
            WINDOW_HEIGHT - 53, color=sge.gfx.Color('black'), halign='center',
            valign='middle'
        )

    def game_end(self, snake):
        """Kill the snake, show menu, and store any new high scores.

        Parameter:
        snake -- Snake object used by player during game
        """
        snake.yvelocity = 0
        snake.xvelocity = 0
        for part in snake.body_parts:
            part.active = False
        snake.is_alive = False
        sge.game.project_text(
            GAME_OVER_FONT, 'You Died. Game. Over.', 155,
            (WINDOW_HEIGHT - 106) // 3, color=sge.gfx.Color('black'),
            halign='middle', valign='middle'
        )
        sge.game.project_text(
            GAME_OVER_INSTRUCTIONS,
            'N -- New Game\nESC -- Quit', 330,
            (WINDOW_HEIGHT - 56) // 2, color=sge.gfx.Color('black'),
            halign='middle', valign='middle'
        )
        with shelve.open('high_score.db') as h_score:
            if self.score > h_score['high_score']:
                h_score['high_score'] = self.score


def start_new_game():
    """Start a new game."""
    global pellet
    global current_game
    current_game = CurrentGame()
    pellet = Pellet()
    snake = Snake()
    return sge.dsp.Room([snake, pellet], background=BACKGROUND)

# Construct a Game object so the game can begin
Game(
    width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
    window_text='Snake by Dan Tinsley', fps=10
)

# Create the font
GAME_OVER_FONT = sge.gfx.Font(name='fonts/horta.ttf', size=72)
GAME_OVER_INSTRUCTIONS = sge.gfx.Font(name='fonts/horta.ttf', size=32)
SCORE_FONT = sge.gfx.Font(name='fonts/horta.ttf', size=40)

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
    sge.gfx.Sprite(width=SPRITE_WIDTH, height=SPRITE_HEIGHT)
)
SNAKE_HEAD.draw_rectangle(
    0, 0, SNAKE_HEAD.width, SNAKE_HEAD.height,
    outline=sge.gfx.Color('black'), fill=sge.gfx.Color('yellow')
)
SNAKE_BODY = (
    sge.gfx.Sprite(width=SPRITE_WIDTH, height=SPRITE_HEIGHT)
)
SNAKE_BODY.draw_rectangle(
    0, 0, SNAKE_BODY.width, SNAKE_BODY.height, fill=sge.gfx.Color('green'),
    outline=sge.gfx.Color('black')
)

# Create the pellet's sprite
PELLET = (
    sge.gfx.Sprite(width=SPRITE_WIDTH, height=SPRITE_HEIGHT)
)
PELLET.draw_rectangle(
    0, 0, PELLET.width, PELLET.height, fill=sge.gfx.Color('blue')
)

# Instantiate the board with specified background colors
LAYERS = [sge.gfx.BackgroundLayer(GAME_BOARD, 0, 0)]
BACKGROUND = sge.gfx.Background(LAYERS, sge.gfx.Color('red'))

# Start the game
sge.game.start_room = start_new_game()

if __name__ == '__main__':
    sge.game.start()
