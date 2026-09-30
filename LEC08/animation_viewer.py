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
