"""Drill #8: 가변 크기 스프라이트를 중앙에서 순서대로 재생한다."""
from dataclasses import dataclass
from pathlib import Path
import json
import math
import time

import pico2d


ASSET_DIR = Path(__file__).resolve().parent
CANVAS_WIDTH, CANVAS_HEIGHT = 800, 600
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0


@dataclass(frozen=True)
class Frame:
    # 시트 좌상단 기준 사각형과 절대 기준점. 기준점은 사각형 밖이어도 된다.
    x: int
    top: int
    width: int
    height: int
    pivot_x: int
    pivot_y: int

    def source_rect(self, sheet_height):
        # pico2d의 clip_draw는 좌하단 좌표를 사용한다.
        return self.x, sheet_height - self.top - self.height, self.width, self.height

    def draw_rect(self, scale):
        # 크기가 달라도 같은 몸통 기준점을 화면 중앙에 맞춘다.
        x = CANVAS_WIDTH / 2 + (self.x + self.width / 2 - self.pivot_x) * scale
        y = CANVAS_HEIGHT / 2 - (self.top + self.height / 2 - self.pivot_y) * scale
        return x, y, self.width * scale, self.height * scale


@dataclass(frozen=True)
class Animation:
    name: str
    label: str
    sheet: str
    fps: float
    scale: float
    frames: tuple[Frame, ...]


def load_animations(path=ASSET_DIR / 'knight_frames.json'):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    animations = []
    for entry in data['animations']:
        width, height = data['sheets'][entry['sheet']]
        frames = tuple(Frame(*item['rect'], *item['pivot']) for item in entry['frames'])
        if not frames or not math.isfinite(entry['fps']) or entry['fps'] <= 0:
            raise ValueError(f"프레임 또는 FPS 오류: {entry['name']}")
        if not math.isfinite(entry['scale']) or entry['scale'] <= 0:
            raise ValueError(f"확대 배율 오류: {entry['name']}")
        for frame in frames:
            if not (frame.width > 0 and frame.height > 0 and frame.x >= 0
                    and frame.top >= 0 and frame.x + frame.width <= width
                    and frame.top + frame.height <= height):
                raise ValueError(f"시트 영역을 벗어난 프레임: {entry['name']}")
        animations.append(Animation(
            entry['name'], entry['label'], entry['sheet'],
            entry['fps'], entry['scale'], frames,
        ))
    if not animations:
        raise ValueError('애니메이션 목록이 비어 있습니다.')
    return tuple(animations), data['sheets']


class AnimationPlayer:
    def __init__(self, animations):
        self.animations = animations
        self.animation_index = 0
        self.frame_index = 0
        self.completed_loops = 0
        self.paused = False
        self.remaining = 1 / self.animation.fps

    @property
    def animation(self):
        return self.animations[self.animation_index]

    @property
    def frame(self):
        return self.animation.frames[self.frame_index]

    def advance(self, elapsed):
        if not math.isfinite(elapsed) or elapsed < 0:
            raise ValueError('경과 시간은 0 이상의 유한한 값이어야 합니다.')
        # 렌더링이 늦어져도 경과시간을 버리지 않는다.
        while elapsed + 1e-9 >= self.remaining:
            elapsed = max(0.0, elapsed - self.remaining)
            self._next_frame()
        self.remaining -= elapsed

    def _next_frame(self):
        if self.paused:
            self.animation_index = (self.animation_index + 1) % len(self.animations)
            self.frame_index = 0
            self.completed_loops = 0
            self.paused = False
        elif self.frame_index == len(self.animation.frames) - 1:
            self.completed_loops += 1
            if self.completed_loops == REPEAT_COUNT:
                self.paused = True
                self.remaining = PAUSE_SECONDS
                return  # 5회 반복 후 마지막 프레임을 1초 유지한다.
            self.frame_index = 0
        else:
            self.frame_index += 1
        self.remaining = 1 / self.animation.fps


def validate_images(images, sizes):
    for name, expected in sizes.items():
        if (images[name].w, images[name].h) != tuple(expected):
            raise ValueError(f'스프라이트 크기가 메타데이터와 다릅니다: {name}')


def main():
    animations, sizes = load_animations()
    player = AnimationPlayer(animations)
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    images = {}
    try:
        pico2d.hide_lattice()
        for name in sizes:
            images[name] = pico2d.load_image(str(ASSET_DIR / name))
        validate_images(images, sizes)
    finally:
        images.clear()
        pico2d.close_canvas()


if __name__ == '__main__':
    main()
