from pico2d import get_canvas_width, load_image

import game_world


class Ball:
    RADIUS = 10
    SPEED = 10

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = load_image('ball21x21.png')

    def update(self):
        self.x += self.direction * self.SPEED
        if self.x < 0 or self.x > get_canvas_width():
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return (self.x - self.RADIUS, self.y - self.RADIUS,
                self.x + self.RADIUS, self.y + self.RADIUS)

    def handle_collision(self, other):
        game_world.remove_object(self)
