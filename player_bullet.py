from entity import Entity
from hit_box import HitBox
from vec2 import Vec2


class PlayerBullet(Entity):
    def __init__(self, position: Vec2, direction: Vec2, speed: int):
        super().__init__(position, HitBox(position - Vec2(10, 10), position + Vec2(10, 10)), speed)
        self.direction = direction

    def dead_in_conflict(self, obj) -> bool:
        return True


if __name__ == '__main__':
    pass
