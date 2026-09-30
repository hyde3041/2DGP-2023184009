from pico2d import *

# 800x600 캔버스 열기
open_canvas(800, 600)

# AI를 이용해 생성한 기사(Knight) 스프라이트 시트 로드
character = load_image('knight_sprite.jpg')

# 애니메이션 프레임 크기 및 갯수가 다르도록 구현 (+2, +2 보너스 요건)
# 1024x1024 이미지 기준, Pico2D는 좌하단이 (0,0)입니다.
animations = {
    'Walk': [(i * 128, 768, 128, 256) for i in range(8)],
    'Run': [(i * 128, 512, 128, 256) for i in range(8)],
    'Jump': [(i * 170, 256, 170, 256) for i in range(6)],
    'Attack': [(i * 170, 0, 170, 256) for i in range(6)]
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
