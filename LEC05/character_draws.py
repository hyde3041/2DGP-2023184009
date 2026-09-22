"""원, 사각형, 삼각형 경로를 반복해서 움직이는 캐릭터 예제."""

import math

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FRAME_DELAY = 0.01
MOVE_SPEED = 4.0

MOTION_CIRCLE = 0
MOTION_SQUARE = 1
MOTION_TRIANGLE = 2

CIRCLE_CENTER_X = 400
CIRCLE_CENTER_Y = 300
CIRCLE_RADIUS = math.hypot(150, 150)
CIRCLE_START_ANGLE = -3 * math.pi / 4
CIRCLE_ANGLE_STEP = 0.03

SQUARE_POINTS = (
    (250, 150),
    (550, 150),
    (550, 450),
    (250, 450),
    (250, 150),
)

TRIANGLE_POINTS = (
    (250, 150),
    (550, 150),
    (400, 450),
    (250, 150),
)


def distance_between(x, y, target_x, target_y):
    return math.hypot(target_x - x, target_y - y)


def move_toward(x, y, target_x, target_y):
    distance = distance_between(x, y, target_x, target_y)
    if distance <= MOVE_SPEED:
        return target_x, target_y, True

    ratio = MOVE_SPEED / distance
    x += (target_x - x) * ratio
    y += (target_y - y) * ratio
    return x, y, False
