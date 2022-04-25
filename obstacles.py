from enum import Enum
import constants as const


class ObstacleStates(Enum):
    moving_left = 0
    moving_right = 1


class Obstacle:
    

    def __init__(self, facing: str, x: int, y: int):
        self.facing = facing
        self.x = x
        self.y = y
        self.switcher = 1
        

    def move(self):
        self.x += const.OBSTACLE_VELOCITY * self.switcher
        if self.x + 300 > const.DISPLAY_W or self.x < 0:
            self.switcher *= -1
