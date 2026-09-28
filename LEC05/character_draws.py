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


def interpolate(start, end, ratio):
    return start + (end - start) * ratio


def move_triangle_right(character, grass):
    print('TRIANGLE RIGHT')
    start_x, start_y = TRIANGLE_TOP
    end_x, end_y = TRIANGLE_RIGHT

    for x in range(start_x, end_x + 1, MOVE_STEP):
        ratio = (x - start_x) / (end_x - start_x)
        y = interpolate(start_y, end_y, ratio)
        draw_character(character, grass, x, y)


def move_triangle_bottom(character, grass):
    print('TRIANGLE BOTTOM')
    start_x, start_y = TRIANGLE_RIGHT
    end_x, _ = TRIANGLE_LEFT

    for x in range(start_x, end_x - 1, -MOVE_STEP):
        draw_character(character, grass, x, start_y)


def move_triangle_left(character, grass):
    print('TRIANGLE LEFT')
    start_x, start_y = TRIANGLE_LEFT
    end_x, end_y = TRIANGLE_TOP

    for x in range(start_x, end_x + 1, MOVE_STEP):
        ratio = (x - start_x) / (end_x - start_x)
        y = interpolate(start_y, end_y, ratio)
        draw_character(character, grass, x, y)


def draw_triangle(character, grass):
    print('TRIANGLE')
    move_triangle_right(character, grass)
    move_triangle_bottom(character, grass)
    move_triangle_left(character, grass)


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    grass = load_image('grass.png')
    character = load_image('character.png')

    while True:
        draw_circle(character, grass)
        draw_rectangle(character, grass)
        draw_triangle(character, grass)

    close_canvas()
