from pico2d import *

open_canvas(800, 600)
character = load_image('../Labs/LEC08_Animation/animation_sheet.png')

animations = {
    'Walk': [(0, 0, 50, 50), (50, 0, 50, 50), (100, 0, 50, 50), (150, 0, 50, 50)],
    'Run': [(0, 50, 60, 50), (60, 50, 60, 50), (120, 50, 60, 50), (180, 50, 60, 50), (240, 50, 60, 50)],
    'Jump': [(0, 100, 55, 60), (55, 100, 55, 60), (110, 100, 55, 60)],
    'Attack': [(0, 150, 70, 70), (70, 150, 70, 70), (140, 150, 70, 70), (210, 150, 70, 70)]
}

anim_sequence = ['Walk', 'Run', 'Jump', 'Attack']
current_anim_idx = 0
current_frame_idx = 0
loop_count = 0

running = True
while running:
    clear_canvas()
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDLK_ESCAPE:
            running = False
            
    state_name = anim_sequence[current_anim_idx]
    frames = animations[state_name]
    x, y, w, h = frames[current_frame_idx]
    
    character.clip_draw(x, y, w, h, 400, 300, 300, 300)
    update_canvas()
    
    current_frame_idx += 1
    if current_frame_idx >= len(frames):
        current_frame_idx = 0
        loop_count += 1
        
    delay(0.05)

close_canvas()
