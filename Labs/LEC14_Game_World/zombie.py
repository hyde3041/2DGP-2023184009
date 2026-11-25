from pico2d import get_canvas_width, load_image

import game_world


class Zombie:
    SIZE = 100
    SPEED = 2
    WALK_FRAME_COUNT = 10
    DEATH_FRAME_COUNT = 12

    def __init__(self, x=650, y=90):
        self.x, self.y = x, y
        self.direction = -1
        self.walk_frame = 0
        self.dead = False
        self.death_frame = 0
        self.walk_images = [
            load_image(f'zombie/Walk ({i}).png')
            for i in range(1, self.WALK_FRAME_COUNT + 1)
        ]
        self.death_images = [
            load_image(f'zombie/Dead ({i}).png')
            for i in range(1, self.DEATH_FRAME_COUNT + 1)
        ]

    def update(self):
        if self.dead:
            self.death_frame += 1
            if self.death_frame >= self.DEATH_FRAME_COUNT * 5:
                game_world.remove_object(self)
            return

        self.walk_frame = (self.walk_frame + 0.1) % self.WALK_FRAME_COUNT
        self.x += self.direction * self.SPEED
        if self.x < 520:
            self.x = 520
            self.direction = 1
        elif self.x > get_canvas_width() - self.SIZE // 2:
            self.x = get_canvas_width() - self.SIZE // 2
            self.direction = -1

    def draw(self):
        if self.dead:
            image = self.death_images[min(self.death_frame // 5,
                                          self.DEATH_FRAME_COUNT - 1)]
        else:
            image = self.walk_images[int(self.walk_frame)]

        if self.direction < 0:
            image.composite_draw(0, 'h', self.x, self.y, self.SIZE, self.SIZE)
        else:
            image.draw(self.x, self.y, self.SIZE, self.SIZE)

    def get_bb(self):
        half = self.SIZE // 3
        return (self.x - half, self.y - half,
                self.x + half, self.y + half)

    def handle_collision(self, other):
        if not self.dead:
            self.dead = True
            self.death_frame = 0
