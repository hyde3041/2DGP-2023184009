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


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True


def draw_frame(character, x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()


def update_circle(angle):
    end_angle = CIRCLE_START_ANGLE + math.tau
    angle = min(angle + CIRCLE_ANGLE_STEP, end_angle)
    x = CIRCLE_CENTER_X + CIRCLE_RADIUS * math.cos(angle)
    y = CIRCLE_CENTER_Y + CIRCLE_RADIUS * math.sin(angle)
    return x, y, angle, angle >= end_angle


def update_path(x, y, points, target_index):
    target_x, target_y = points[target_index]
    x, y, reached = move_toward(x, y, target_x, target_y)
    finished = False

    if reached:
        target_index += 1
        if target_index == len(points):
            target_index = 1
            finished = True

    return x, y, target_index, finished


def create_initial_state():
    x, y = SQUARE_POINTS[0]
    return x, y, MOTION_CIRCLE, CIRCLE_START_ANGLE, 1


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    character = load_image('character.png')
    x, y, motion, angle, target_index = create_initial_state()
    close_canvas()
