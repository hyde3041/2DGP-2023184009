"""AI로 작성한 캐릭터 도형 경로 반복 예제."""

import math

from pico2d import *


WIDTH = 800
HEIGHT = 600
FRAME_DELAY = 0.01
MOVE_SPEED = 4.0

CIRCLE = 0
SQUARE = 1
TRIANGLE = 2

CENTER_X = 400
CENTER_Y = 300
RADIUS = math.hypot(150, 150)
START_ANGLE = -3 * math.pi / 4
ANGLE_STEP = 0.03

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


def move_toward(x, y, target_x, target_y):
    dx = target_x - x
    dy = target_y - y
    distance = math.hypot(dx, dy)

    if distance <= MOVE_SPEED:
        return target_x, target_y, True

    return (
        x + dx / distance * MOVE_SPEED,
        y + dy / distance * MOVE_SPEED,
        False,
    )


def update_polygon(x, y, points, point_index):
    target_x, target_y = points[point_index]
    x, y, reached = move_toward(x, y, target_x, target_y)

    if reached:
        point_index += 1
        if point_index == len(points):
            return x, y, 1, True

    return x, y, point_index, False


def keep_running():
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True


def main():
    open_canvas(WIDTH, HEIGHT)
    character = load_image('character.png')

    x, y = SQUARE_POINTS[0]
    motion = CIRCLE
    angle = START_ANGLE
    point_index = 1
    running = True

    while running:
        running = keep_running()

        if motion == CIRCLE:
            end_angle = START_ANGLE + math.tau
            angle = min(angle + ANGLE_STEP, end_angle)
            x = CENTER_X + RADIUS * math.cos(angle)
            y = CENTER_Y + RADIUS * math.sin(angle)

            if angle >= end_angle:
                motion = SQUARE
                point_index = 1
        elif motion == SQUARE:
            x, y, point_index, finished = update_polygon(
                x, y, SQUARE_POINTS, point_index
            )
            if finished:
                motion = TRIANGLE
                point_index = 1
        else:
            x, y, point_index, finished = update_polygon(
                x, y, TRIANGLE_POINTS, point_index
            )
            if finished:
                motion = CIRCLE
                angle = START_ANGLE

        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(FRAME_DELAY)

    close_canvas()


if __name__ == '__main__':
    main()
