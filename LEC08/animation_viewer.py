from pico2d import *

# 800x600 캔버스 열기
open_canvas(800, 600)

# 애니메이션 스프라이트 시트 로드
# 주의: 사용하실 스프라이트 시트 이미지로 파일명을 수정하세요.
character = load_image('../Labs/LEC08_Animation/animation_sheet.png')

# 애니메이션 프레임 크기 및 갯수가 다르도록 구현 (+2, +2 보너스 요건)
# 각 튜플은 (x, y, width, height)를 나타냅니다.
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
            
    state_name = anim_sequence[current_anim_idx]
    frames = animations[state_name]
    x, y, w, h = frames[current_frame_idx]
    
    # 화면 중앙에 확대해서 출력 (화면 절반 크기)
    character.clip_draw(x, y, w, h, 400, 300, 300, 300)
    update_canvas()
    
    current_frame_idx += 1
    if current_frame_idx >= len(frames):
        current_frame_idx = 0
        loop_count += 1
        if loop_count >= 5:
            # 5회 반복 시 1초 대기
            delay(1.0)
            loop_count = 0
            current_anim_idx = (current_anim_idx + 1) % len(anim_sequence)
            current_frame_idx = 0
        
    delay(0.05)

close_canvas()
