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


def draw_circle(character, grass):
    print('CIRCLE')

    for degree in range(0, 361, MOVE_STEP):
        theta = math.radians(degree)
        x = CIRCLE_CENTER_X + CIRCLE_RADIUS * math.cos(theta)
        y = CIRCLE_CENTER_Y + CIRCLE_RADIUS * math.sin(theta)
        draw_character(character, grass, x, y)


def move_top(character, grass):
    print('TOP')

    for x in range(RECTANGLE_LEFT, RECTANGLE_RIGHT + 1, MOVE_STEP):
        draw_character(character, grass, x, RECTANGLE_TOP)


def move_right(character, grass):
    print('RIGHT')

    for y in range(RECTANGLE_TOP, RECTANGLE_BOTTOM - 1, -MOVE_STEP):
        draw_character(character, grass, RECTANGLE_RIGHT, y)


def move_bottom(character, grass):
    print('BOTTOM')

    for x in range(RECTANGLE_RIGHT, RECTANGLE_LEFT - 1, -MOVE_STEP):
        draw_character(character, grass, x, RECTANGLE_BOTTOM)


def move_left(character, grass):
    print('LEFT')

    for y in range(RECTANGLE_BOTTOM, RECTANGLE_TOP + 1, MOVE_STEP):
        draw_character(character, grass, RECTANGLE_LEFT, y)


def draw_rectangle(character, grass):
    print('RECTANGLE')
    move_top(character, grass)
    move_right(character, grass)
    move_bottom(character, grass)
    move_left(character, grass)
