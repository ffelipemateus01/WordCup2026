from src.object import IObject
from src.constants.match import BALL_AIR_RESISTENCE, WIN_WIDTH

class Ball(IObject):
    def __init__(self, skin: int):
        super().__init__('ball', f'ball-{skin}')
        self.velocityX = 0
        
    def move(self):
        super().move()
        self.rect.x += self.velocityX
        self.__airResistence()
        self.__wallCollision()

    def __airResistence(self):
        if self.velocityX > 0:
            self.velocityX = max(0, self.velocityX - BALL_AIR_RESISTENCE)
        elif self.velocityX < 0:
            self.velocityX = min(0, self.velocityX + BALL_AIR_RESISTENCE)

    def __wallCollision(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocityX = -self.velocityX
        elif self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH
            self.velocityX = -self.velocityX