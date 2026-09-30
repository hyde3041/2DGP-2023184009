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
