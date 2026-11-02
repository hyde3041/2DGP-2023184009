#게임월드 리스트 초기화
world = []

#객체를 게임 월드에 추가하는 함수
def add_object(o):
    global world
    world.append(o)

#게임 로직
def update():
    for o in list(world):
        o.update()

def remove_object(o):
    if o in world:
        world.remove(o)
        return True
    return False

#게임 월드 랜더링
def render():
    for o in world:
        o.draw()

