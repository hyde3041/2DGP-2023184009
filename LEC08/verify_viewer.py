"""실제 main/SDL 렌더러를 실행하고 두 번째 걷기 정지 중 종료한다.

python LEC08/verify_viewer.py --screenshots LEC08/.verification
python LEC08/verify_viewer.py --live
"""
import argparse
import os
from pathlib import Path
from types import SimpleNamespace


def verify(live=False, screenshots=None, escape=False):
    if not live:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        os.environ['SDL_RENDER_DRIVER'] = 'software'

    import animation_viewer as viewer
    import pico2d.pico2d as core
    from sdl2 import (
        SDL_CreateRGBSurfaceWithFormat, SDL_FreeSurface,
        SDL_PIXELFORMAT_RGBA32, SDL_RenderReadPixels,
    )
    from sdl2.sdlimage import IMG_SavePNG

    saved = {
        'events': viewer.pico2d.get_events,
        'delay': viewer.pico2d.delay,
        'draw': viewer.draw_frame,
        'present': viewer.pico2d.update_canvas,
        'time': viewer.time,
    }
    clock = 0.0
    order = []
    captured = set()
    last_player = None
    quit_sent = False
    rendered = 0
    folder = Path(screenshots).resolve() if screenshots else None
    if folder:
        folder.mkdir(parents=True, exist_ok=True)

    def events():
        nonlocal clock, quit_sent
        current = saved['events']()
        clock += 1 / 60
        if order == ['Walk', 'Run', 'Jump', 'Attack', 'Walk'] and last_player.paused:
            quit_sent = True
            if escape:
                current.append(SimpleNamespace(type=viewer.pico2d.SDL_KEYDOWN,
                                               key=viewer.pico2d.SDLK_ESCAPE))
            else:
                current.append(SimpleNamespace(type=viewer.pico2d.SDL_QUIT))
        return current

    def draw(images, player):
        nonlocal last_player, rendered
        last_player = player
        if not order or order[-1] != player.animation.name:
            order.append(player.animation.name)
        rendered += 1
        if rendered > 10000:
            raise AssertionError('동작 순환이나 종료 조건에 도달하지 못했습니다.')
        saved['draw'](images, player)

    def present():
        if folder and last_player:
            player = last_player
            key = (player.animation.name, player.frame_index)
            if key not in captured:
                surface = SDL_CreateRGBSurfaceWithFormat(
                    0, 800, 600, 32, SDL_PIXELFORMAT_RGBA32)
                if not surface:
                    raise RuntimeError('검증용 SDL surface 생성 실패')
                try:
                    result = SDL_RenderReadPixels(
                        core.renderer, None, SDL_PIXELFORMAT_RGBA32,
                        surface.contents.pixels, surface.contents.pitch)
                    if result != 0:
                        raise RuntimeError('실제 렌더링 결과 읽기 실패')
                    path = folder / f'{key[0]}-{key[1] + 1:02d}.png'
                    if IMG_SavePNG(surface, os.fsencode(path)) != 0:
                        raise RuntimeError('렌더링 스크린샷 저장 실패')
                    captured.add(key)
                finally:
                    SDL_FreeSurface(surface)
        saved['present']()

    viewer.pico2d.get_events = events
    viewer.draw_frame = draw
    viewer.pico2d.update_canvas = present
    if not live:
        viewer.time = SimpleNamespace(perf_counter=lambda: clock)
        viewer.pico2d.delay = lambda seconds: None
    try:
        viewer.main()
    finally:
        viewer.pico2d.get_events = saved['events']
        viewer.draw_frame = saved['draw']
        viewer.pico2d.update_canvas = saved['present']
        viewer.pico2d.delay = saved['delay']
        viewer.time = saved['time']
    assert quit_sent, '검증이 끝나기 전에 창이 닫혔습니다.'
    assert order == ['Walk', 'Run', 'Jump', 'Attack', 'Walk']
    assert last_player.paused and last_player.completed_loops == 5
    if folder:
        assert len(captured) == 28
    print(f"SDL OK: {order}, {rendered} renders, "
          f"{'ESC' if escape else 'window close'} during pause, "
          f"{len(captured)} screenshots")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true', help='실제 창에서 실제 속도로 확인')
    parser.add_argument('--screenshots', help='28개 실제 렌더링 PNG를 저장할 폴더')
    parser.add_argument('--escape', action='store_true', help='창 닫기 대신 ESC로 종료 확인')
    args = parser.parse_args()
    verify(args.live, args.screenshots, args.escape)
