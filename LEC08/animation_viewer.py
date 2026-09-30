from pico2d import *

open_canvas(800, 600)
character = load_image('../Labs/LEC08_Animation/animation_sheet.png')

animations = {
    'Walk': [(0, 0, 50, 50), (50, 0, 50, 50), (100, 0, 50, 50), (150, 0, 50, 50)],
    'Run': [(0, 50, 60, 50), (60, 50, 60, 50), (120, 50, 60, 50), (180, 50, 60, 50), (240, 50, 60, 50)]
}

running = True
while running:
    clear_canvas()
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    update_canvas()
    delay(0.05)

close_canvas()
