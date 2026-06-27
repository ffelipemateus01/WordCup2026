from src.object import IObject
from src.entities.ball import Ball
from src.entities.player import Player
from src.entities.bot import Bot
from src.entities.goal import Goal
from src.entities.player import Player
from src.constants.match import BALL_HIT_FORCE, BALL_LIFT_FORCE, BALL_HEAD_FORCE, ENTITIES_START_POSITION

class CollisionMediator:
    def __init__(self, objs: list[IObject]):
        self.ball: Ball = next(obj for obj in objs if isinstance(obj, Ball))
        self.kickers: list[Player | Bot]= [obj for obj in objs if isinstance(obj, (Player, Bot))]
        self.goals: list[Goal] = [obj for obj in objs if isinstance(obj, Goal)]
        self.scorers = {}
        for kicker in self.kickers:
            self.scorers['goal2' if kicker.name == 'player1' else 'goal1'] = kicker

    def verify_collision(self) -> str | None:
        '''Retorna nome do player se tiver um gol'''
        for kicker in self.kickers:
            if kicker.rect.colliderect(self.ball.rect):
                self.__hitBall(kicker)
        for goal in self.goals:
            if goal.rect.colliderect(self.ball.rect):
                if goal.rect.top >= self.ball.rect.centery:
                    self.ball.velocityY = -abs(self.ball.velocityY)
                    return None
                if goal.name == 'goal1' and goal.rect.right >= self.ball.rect.right:
                    scorer = self.__score(goal)
                    return scorer
                if goal.name == 'goal2' and goal.rect.left <= self.ball.rect.left:
                    scorer = self.__score(goal)
                    return scorer
                return None
                
        return None 

    def __hitBall(self, kicker: IObject):
        varX = self.ball.rect.centerx - kicker.rect.centerx
        varY = self.ball.rect.centery - kicker.rect.centery

        if abs(varX) > abs(varY):
            # batida de lado
            direction = 1 if varX > 0 else -1
            self.ball.velocityX = direction * BALL_HIT_FORCE
            self.ball.velocityY = -BALL_LIFT_FORCE
            if varX > 0:
                self.ball.rect.left = kicker.rect.right
            else:
                self.ball.rect.right = kicker.rect.left
        else:
            # batida por baixo
            if varY < 0:
                self.ball.velocityY = -BALL_LIFT_FORCE
                self.ball.rect.bottom = kicker.rect.top
            else:
                self.ball.velocityY = BALL_HEAD_FORCE
                self.ball.rect.top = kicker.rect.bottom
            self.ball.velocityX = BALL_HIT_FORCE * (1 if varX >= 0 else -1)

    def __score(self, goal: Goal) -> str:
        scorer: Player | Bot = self.scorers.get(goal.name)
        if scorer:
            scorer.score += 1
            self.__resetPositions()
            return scorer.name

    def __resetPositions(self):
        self.ball.rect.topleft = ENTITIES_START_POSITION[self.ball.name]
        self.ball.velocityX = 0
        self.ball.velocityY = 0
        for kicker in self.kickers:
            kicker.rect.topleft = ENTITIES_START_POSITION[kicker.name]
            kicker.velocityY = 0