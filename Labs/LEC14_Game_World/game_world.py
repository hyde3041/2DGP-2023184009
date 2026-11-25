#게임월드 리스트 초기화
world = [[], []]
collision_pairs = {}

#객체를 게임 월드에 추가하는 함수
def add_object(o, depth = 0): # depth는 객체의 레이어를 나타내며 기본값은 0
    world[depth].append(o)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
    for pairs in collision_pairs.values():
        for objects in pairs:
            if o in objects:
                objects.remove(o)


def add_collision_pairs(group, a=None, b=None):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if a is not None and a not in collision_pairs[group][0]:
        collision_pairs[group][0].append(a)
    if b is not None and b not in collision_pairs[group][1]:
        collision_pairs[group][1].append(b)


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    return not (left_a > right_b or right_a < left_b or
                top_a < bottom_b or bottom_a > top_b)


def handle_collision():
    for objects_a, objects_b in list(collision_pairs.values()):
        for a in list(objects_a):
            for b in list(objects_b):
                if a in objects_a and b in objects_b and collide(a, b):
                    a.handle_collision(b)
                    b.handle_collision(a)

#게임 로직
def update():
    for layer in world:
        for o in list(layer):
            o.update()

#게임 월드 랜더링
def render():
    for layer in world: #모든 레이어를 순회하며 객체를 랜더링
        for o in layer:
            o.draw()