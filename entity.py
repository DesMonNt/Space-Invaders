from abc import ABC, abstractmethod
from vec2 import Vec2


class Entity(ABC):
    def __init__(self, position: Vec2, hit_box, speed: int):
        self.position = position
        self.hit_box = hit_box
        self.speed = speed

    def move(self, delta: Vec2):
        self.position += delta
        self.hit_box.move(delta)

    def move_to(self, position: Vec2):
        self.position = position
        self.hit_box.move_to(position)

    def is_intersecting(self, obj) -> bool:
        return self.hit_box.is_intersecting(obj.hit_box)

    @abstractmethod
    def dead_in_conflict(self, obj) -> bool:
        pass


if __name__ == '__main__':
    pass
