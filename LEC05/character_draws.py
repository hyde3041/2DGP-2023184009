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
