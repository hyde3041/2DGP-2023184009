# Sprite assets

- `knight_sprite.jpg`: 기존 저장소의 `a4d6e38` 커밋에서 AI 생성으로 기록된 기사 시트. 이 과제에서는 걷기(8), 달리기(8), 점프(6)만 사용한다. 원본 픽셀은 변경하지 않았다.
- `knight_attack.png`: 기존 기사 디자인을 참고해 내장 ImageGen으로 생성한 공격 6프레임. 투명 배경. 인접 프레임이 겹치지 않도록 간격을 보완한 두 번째 결과를 사용한다.
- `knight_frames.json`: 이미지 좌상단 기준으로 측정한 개별 사각형과 캐릭터 정렬 기준점. 원본 이미지 크기를 함께 기록한다.

## 생성 프롬프트 (내장 ImageGen, CLI 사용 안 함)

### 최초 생성

Use case: stylized-concept. Asset type: production 2D game sprite sheet, six-frame sword attack. Reference image: the supplied knight contact sheet is CHARACTER/STYLE REFERENCE only. Keep the identical gray plate armor, closed golden-trimmed visor, dark plume, red cape, roundish dark gold-edged shield, silver-blue sword, black outlines and crisp pixel art look. Create exactly SIX separate sprites in ONE HORIZONTAL ROW on a wide 3:1 canvas, with six equal square cells. Each cell has the same stationary knight facing RIGHT, same body scale and fixed foot baseline. Sequence left to right: 1 neutral ready with sword back, 2 anticipation lifting sword behind head, 3 sword above head winding up, 4 broad forward horizontal slash with small blue arc, 5 down-forward follow-through, 6 recover to ready. Feet and torso stay centered at identical position in every cell, limbs/cape animate. Each complete sprite including sword and effect must stay comfortably INSIDE its own cell, at least 12 percent empty transparent padding to left/right and 8 percent above/below; NO overlap or touching adjacent frames. All six frames are unique coherent consecutive poses of one attack, NOT six unrelated designs. Genuinely transparent background, no ground, no text, no labels, no grid, no shadows, no checkerboard painted into image.

### 간격 보완 (최종)

Use case: precise-object-edit. Edit target: this six-pose knight attack sprite strip. Preserve all six poses, the same knight design, pixel-art rendering, colors, shield, sword and attack arc exactly. ONLY change the layout: each pose must be much smaller with huge transparent padding so its entire bounding box fits inside one of SIX EQUAL nonoverlapping vertical cells of a single horizontal strip. UNIFORMLY SHRINK ALL SIX KNIGHTS TO 55 PERCENT OF THEIR CURRENT SIZE. Do not crop off weapons or cape. Center each in its own cell. In particular, the FOURTH pose's slash effect and FIFTH pose's cape must be completely separated by a large transparent gap, at least a knight torso width. Same body scale and foot baseline for all six. Keep the original broad 3:1 canvas ratio. Do not fill the newly empty space with anything. Large EMPTY gaps are required for game engine clipping. Transparent background, no text, no grid.
