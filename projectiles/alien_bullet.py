from entities.entity import Entity
from entities.alien import Alien
from physics.hit_box import HitBox
from physics.vec2 import Vec2


class AlienBullet(Entity):
    def __init__(self, position: Vec2, direction: Vec2, speed: int):
        super().__init__(position, HitBox(position - Vec2(10, 10), position + Vec2(10, 10)), speed)
        self.direction = direction

    def dead_in_conflict(self, obj) -> bool:
        return not isinstance(obj, Alien)


if __name__ == '__main__':
    pass
