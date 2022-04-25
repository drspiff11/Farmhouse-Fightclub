import constants as const
from enum import Enum
from spritesheet import SpriteSheet
import pygame
from typing import List
from obstacles import Obstacle


# an Enum class to help differentiate the states
class CharacterStates(Enum):
    still = 1
    jumping = 2
    moving_l = 3
    moving_r = 4
    punching_l = 5
    punching_r = 6
    kicking_l = 7
    kicking_r = 8


class Character:

    # the class initializer
    def __init__(self, sprite: str, facing: str, x: int, y: int):
        # determine which sprite to cut out, depending what is passed in
        if sprite == "SpriteSheet('images/chicken.png')":
            self.sprite = SpriteSheet('images/chicken.png')
        elif sprite == "SpriteSheet('images/cow.png')":
            self.sprite = SpriteSheet('images/cow.png')

        # cut out in individual sprites
        self.stand_left = self.sprite.get_sprite(5, 5, 60, 60)
        self.stand_right = self.sprite.get_sprite(65, 5, 60, 60)
        self.walk_left = self.sprite.get_sprite(5, 65, 60, 60)
        self.walk_right = self.sprite.get_sprite(65, 65, 60, 60)
        self.jump_left = self.sprite.get_sprite(5, 125, 60, 60)
        self.jump_right = self.sprite.get_sprite(65, 125, 60, 60)
        self.punch_left = self.sprite.get_sprite(5, 200, 60, 60)
        self.punch_right = self.sprite.get_sprite(65, 200, 60, 60)
        self.kick_left = self.sprite.get_sprite(5, 260, 60, 60)
        self.kick_right = self.sprite.get_sprite(65, 260, 60, 60)

        # initialize the fields of the class
        self.facing = facing
        self.x = x
        self.y = y
        self.current = self.stand_left
        self.last = pygame.time.get_ticks()
        self.buffer = 300
        self.health = 40
        self.on_platform = False

    # this lets the character jump
    def jumpAnimal(self):
        if self.facing == "left" and self.y == const.GROUND:
            self.y -= const.SCALE * 18
            self.current = self.jump_left
        if self.facing == "right" and self.y == const.GROUND:
            self.y -= const.SCALE * 18
            self.current = self.jump_right

    # this lets the character move
    def moveAnimal(self, direction: str, opponent_x: int, opponent_y: int, is_cpu: bool):
        if not is_cpu:
            if direction == "left" and self.x > 0:
                if (self.x > opponent_x + 25) or (self.x < opponent_x):
                    self.facing = "left"
                    self.current = self.walk_left
                    self.x -= const.SCALE / 2
                    self.current = self.stand_left
                elif self.y < opponent_y:
                    self.facing = "left"
                    self.current = self.walk_left
                    self.x -= const.SCALE / 2
                    self.current = self.stand_left
            elif direction == "right" and self.x < 1150:
                if (self.x + 15 < opponent_x - 25) or (self.x > opponent_x):
                    self.facing = "right"
                    self.current = self.walk_right
                    self.x += const.SCALE / 2
                    self.current = self.stand_right
                    self.facing = "right"
                elif self.y < opponent_y:
                    self.facing = "right"
                    self.current = self.walk_left
                    self.x += const.SCALE / 2
                    self.current = self.stand_left
        else:
            if direction == "left" and self.x > 0:
                if (self.x > opponent_x + 25) or (self.x < opponent_x):
                    self.facing = "left"
                    self.current = self.walk_left
                    self.x -= const.SCALE / 4
                    self.current = self.stand_left
                elif self.y < opponent_y:
                    self.facing = "left"
                    self.current = self.walk_left
                    self.x -= const.SCALE / 4
                    self.current = self.stand_left
            elif direction == "right" and self.x < const.DISPLAY_W:
                if (self.x + 15 < opponent_x - 25) or (self.x > opponent_x):
                    self.facing = "right"
                    self.current = self.walk_right
                    self.x += const.SCALE / 4
                    self.current = self.stand_right
                    self.facing = "right"
                elif self.y < opponent_y:
                    self.facing = "right"
                    self.current = self.walk_left
                    self.x += const.SCALE / 4
                    self.current = self.stand_left

    # this makes the character punch
    def punchAnimal(self):
        if self.current != CharacterStates.jumping:
            if self.facing == "left":
                self.current = self.punch_left
            elif self.facing == "right":
                self.current = self.punch_right

    # this makes the character kick
    def kickAnimal(self):
        if self.current != CharacterStates.jumping:
            if self.facing == "left":
                self.current = self.kick_left
            elif self.facing == "right":
                self.current = self.kick_right

    # this is gravity, so the character falls to the ground
    def gravity(self, obstacles: List[Obstacle]):
        if self.x < obstacles[0].x or self.x > obstacles[0].x + 300:
            now = pygame.time.get_ticks()
            self.on_platform = False
            if self.y < const.GROUND and now - self.last >= self.buffer:
                self.y += const.SCALE
            if self.y == const.GROUND:
                self.last = now

        if obstacles[0].x < self.x < obstacles[0].x + 300:
            now = pygame.time.get_ticks()
            self.on_platform = True
            if self.y - 20 < obstacles[0].y - 70 and now - self.last >= self.buffer:
                self.y += const.SCALE
            if self.y - 20 == obstacles[0].y - 70:
                self.last = now

    # a get function to return the current state (i.e. sprite) of the character
    def getCurrState(self) -> pygame.Surface:
        return self.current

    # a set function to set the current state (i.e. sprite) of the character
    def setCurrState(self, action: CharacterStates):
        self.current = action

    # this is called when the character is kicked by their opponent
    def gotKicked(self, direction_from: str):
        self.health -= 2
        if direction_from == "right":
            if self.x - 20 > 20:
                self.x -= 40
            else:
                self.x = 0
        else:
            if self.x + 20 < const.DISPLAY_W:
                self.x += 40
            else:
                self.x = const.DISPLAY_W

    # this is called when the character is punched by their opponent
    def gotPunched(self, direction_from: str):
        self.health -= 1
        if direction_from == "right":
            if self.x - 20 > 20:
                self.x -= 20
            else:
                self.x = 0
        else:
            if self.x + 20 < const.DISPLAY_W:
                self.x += 20
            else:
                self.x = const.DISPLAY_W
