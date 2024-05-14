from random import random
from entity import Entity
from hit_box import HitBox
from player_bullet import PlayerBullet
from vec2 import Vec2


class MysteryShip(Entity):
    def __init__(self, position: Vec2, speed: int):
        super().__init__(position, HitBox(position - Vec2(10, 10), position + Vec2(10, 10)), speed)
        self.direction = Vec2(0, 1)
        self.__spawn_rate = 0.001
        self.is_active = False

    def dead_in_conflict(self, obj) -> bool:
        return isinstance(obj, PlayerBullet)

    def is_ready_to_spawn(self) -> bool:
        if self.position.x < 0 or self.position.x > 800:
            self.is_active = False

        if self.is_active:
            return False

        if random() < self.__spawn_rate:
            self.is_active = True
            return True

        return False

    def get_new_spawn_point(self):
        if random() < 0.5:
            self.direction = Vec2(1, 0)
            self.move_to(Vec2(20, 30))
        else:
            self.direction = Vec2(-1, 0)
            self.move_to(Vec2(800 - 20, 30))


if __name__ == '__main__':
    pass
