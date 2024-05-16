from projectiles.alien_bullet import AlienBullet
from projectiles.player_bullet import PlayerBullet
from entities.entity import Entity
from physics.hit_box import HitBox
from physics.vec2 import Vec2


class Bunker(Entity):
    def __init__(self, position):
        super().__init__(position, HitBox(position - Vec2(20, 10), position + Vec2(20, 10)), 0)
        self.direction = Vec2(0, -1)
        self.__hp = 10

    def dead_in_conflict(self, obj):
        if isinstance(obj, AlienBullet) or isinstance(obj, PlayerBullet):
            self.__hp -= 1

        return self.__hp <= 0


if __name__ == '__main__':
    pass