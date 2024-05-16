from projectiles.player_bullet import PlayerBullet
from projectiles.alien_bullet import AlienBullet
from physics.hit_box import HitBox
from entities.entity import Entity
from physics.vec2 import Vec2


class Player(Entity):
    def __init__(self, position: Vec2, speed: int):
        super().__init__(position, HitBox(position - Vec2(10, 10), position + Vec2(10, 10)), speed)
        self.direction = Vec2(0, -1)

    def dead_in_conflict(self, obj):
        return isinstance(obj, AlienBullet)

    def shoot(self):
        return PlayerBullet(self.position, self.direction, self.speed)


if __name__ == '__main__':
    pass
