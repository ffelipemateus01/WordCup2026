from src.object import IObject
from src.constants.match import BALL_START_POSITION, BALL_SPEED, GROUND_HEIGHT, BALL_GRAVITY_FORCE

class Ball(IObject):
    def __init__(self, skin: int):
        super().__init__(f'ball-{skin}', BALL_START_POSITION, BALL_SPEED)

    def gravity(self):
        displacement = BALL_GRAVITY_FORCE
        newPositionY = self.rect.bottom + displacement
        finalPositionY = newPositionY if newPositionY < GROUND_HEIGHT else GROUND_HEIGHT
        self.rect.bottomleft = (self.rect.top, finalPositionY)
        
    def move(self):
        pass

    def jump(self):
        pass