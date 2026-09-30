from pico2d import *

open_canvas(800, 600)
character = load_image('../Labs/LEC08_Animation/animation_sheet.png')

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
