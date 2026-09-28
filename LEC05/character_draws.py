"""캐릭터가 세 가지 도형을 따라 계속 움직이는 예제."""

from pico2d import *
import math


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FRAME_DELAY = 0.01
MOVE_STEP = 5

CIRCLE_CENTER_X = 400
CIRCLE_CENTER_Y = 300
CIRCLE_RADIUS = 200

RECTANGLE_LEFT = 50
RECTANGLE_RIGHT = 750
RECTANGLE_BOTTOM = 50
RECTANGLE_TOP = 550

TRIANGLE_TOP = (400, 550)
TRIANGLE_RIGHT = (700, 50)
TRIANGLE_LEFT = (100, 50)


def draw_character(character, grass, x, y):
    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, y)
    update_canvas()
    delay(FRAME_DELAY)
