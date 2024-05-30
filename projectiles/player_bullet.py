from entities.entity import Entity
from physics.hit_box import HitBox
from physics.vec2 import Vec2


class PlayerBullet(Entity):
    def __init__(self, position: Vec2, direction: Vec2, speed: int):
        super().__init__(position, HitBox(position - Vec2(10, 10), position + Vec2(10, 10)), speed)
        self.direction = direction

    def __eq__(self, other):
        return (self.position == other.position and self.hit_box == other.hit_box and self.direction == other.direction
                and self.speed == other.speed)

    def dead_in_conflict(self, obj) -> bool:
        return True

