from src.object import IObject
from src.entities.ball import Ball
from src.constants.match import WIN_WIDTH, JUMP_FORCE
from random import randint

class Bot(IObject):
    def __init__(self, name: str, skin: int, ball: Ball):
        super().__init__(name, f'{name}-{skin}')
        self.score = 0
        self.ball = ball
        self._originalFacingLeft = name == 'bot'
        self._facingLeft = self._originalFacingLeft

    def move(self):
        super().move()
        self.__trackBall()
        self.__autoJump()

    def __trackBall(self):
        varX = self.ball.rect.centerx - self.rect.centerx
        if varX < -self.speed and self.rect.left > 0:
            self.rect.centerx -= self.speed
            self._transformSurf(True)
        elif varX > self.speed and self.rect.right < WIN_WIDTH:
            self.rect.centerx +=self.speed
            self._transformSurf(False)

    def __autoJump(self):
        varX = abs(self.ball.rect.centerx - self.rect.centerx)
        ballIsClose = varX < self.rect.width
        ballIsAbove = self.ball.rect.centery < self.rect.centery
        if self.isOnGround() and ballIsClose and ballIsAbove:
            sucess = randint(0, 30) == 1 #pra nao pular toda hora
            if sucess:
                self.velocityY = -JUMP_FORCE