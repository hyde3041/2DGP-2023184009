#게임월드 리스트 초기화
world = [[], []]

#객체를 게임 월드에 추가하는 함수
def add_object(o, depth = 0): # depth는 객체의 레이어를 나타내며 기본값은 0
    world[depth].append(o)


def remove_object(o):
    for layer in world:#모든 레이어를 순회하며 객체를 제거
        if o in layer: #객체가 해당 레이어에 존재하면 제거
            layer.remove(o) 
            return #제거 후 함수종료

#게임 로직
def update():
    for layer in world: #모든 레이어를 순회하며 객체를 업데이트
        for o in list(layer):
            o.update()

#게임 월드 랜더링
def render():
    for layer in world: #모든 레이어를 순회하며 객체를 랜더링
        for o in layer:
            o.draw()