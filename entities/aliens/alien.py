from entities.entity import Entity
from physics.hit_box import HitBox
from projectiles.player_bullet import PlayerBullet
from physics.vec2 import Vec2


class Alien(Entity):
    def __init__(self, position: Vec2, speed: int):
        super().__init__(position, HitBox(position - Vec2(10, 10), position + Vec2(10, 10)), speed)
        self.__direction = Vec2(0, 1)

    def dead_in_conflict(self, obj) -> bool:
        return isinstance(obj, PlayerBullet)

    def shoot(self):
        from projectiles.alien_bullet import AlienBullet
        return AlienBullet(self.position, self.__direction, self.speed)
