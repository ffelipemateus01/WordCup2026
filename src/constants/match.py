from src.constants.window import WIN_WIDTH, WIN_HEIGHT
import pygame

GROUND_HEIGHT = 300

PLAYER_SIZE = (67, 90)
BALL_SIZE = (45, 45)
GOAL_SIZE = (127, 170)

ENTITIES_SPEED = {
    'player1': 3,
    'player2': 3,
    'bot': 4,
    'goal1': 0,
    'goal2': 0,
    'ball': 2,
    'field': 0
}

ENTITIES_START_POSITION = {
    'player1': (GOAL_SIZE[0] / 2, GROUND_HEIGHT - PLAYER_SIZE[1]),
    'player2': (WIN_WIDTH - GOAL_SIZE[0] / 2 - PLAYER_SIZE[0], GROUND_HEIGHT - PLAYER_SIZE[1]),
    'bot': (WIN_WIDTH - GOAL_SIZE[0] / 2 - PLAYER_SIZE[0], GROUND_HEIGHT - PLAYER_SIZE[1]),
    'goal1': (-GOAL_SIZE[0] / 2, GROUND_HEIGHT - GOAL_SIZE[1]),
    'goal2': (WIN_WIDTH - GOAL_SIZE[0] / 2, GROUND_HEIGHT - GOAL_SIZE[1]),
    'ball': (WIN_WIDTH / 2 - BALL_SIZE[0] / 2, WIN_HEIGHT / 4 - BALL_SIZE[1] / 2),
    'field': (0, 0)
}

ENTITIES_GRAVITY_FORCE = {
    'player1': 1,
    'player2': 1,
    'bot': 1,
    'goal1': 999,
    'goal2': 999,
    'ball': 0.1,
    'field': 999
}

PLAYER_KEY_UP = {'player1': pygame.K_w,
                 'player2': pygame.K_UP}
PLAYER_KEY_LEFT = {'player1': pygame.K_a,
                   'player2': pygame.K_LEFT}
PLAYER_KEY_RIGHT = {'player1': pygame.K_d,
                    'player2': pygame.K_RIGHT}
PLAYER_KEY_SHOOT = {'player1': pygame.K_LCTRL,
                    'player2': pygame.K_RCTRL}

JUMP_FORCE = 18
BALL_HIT_FORCE = 8
BALL_LIFT_FORCE = 2
BALL_HEAD_FORCE = 10
BALL_AIR_RESISTENCE = 0.1