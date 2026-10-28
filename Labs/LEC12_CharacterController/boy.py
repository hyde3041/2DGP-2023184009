from pico2d import get_time, load_image
from transitions import Machine


IDLE_FRAMES = 8
IDLE_FPS = 8.0

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0.0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.previous_time = get_time()

        self.state_machine = Machine(
            model=self,
            states=['IDLE'],
            initial='IDLE',
            auto_transitions=False,
        )
        # Internal updates keep IDLE active without leaving/re-entering it.
        self.state_machine.add_transition(
            trigger='animate',
            source='IDLE',
            dest=None,
            after='update_idle',
        )

    def update_idle(self, frame_time):
        self.frame = (self.frame + IDLE_FPS * frame_time) % IDLE_FRAMES

    def update(self):
        current_time = get_time()
        frame_time = current_time - self.previous_time
        self.previous_time = current_time
        self.animate(frame_time)

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw(int(self.frame) * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(int(self.frame) * 100, 200, 100, 100, self.x, self.y)

