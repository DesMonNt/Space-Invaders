from abc import ABC, abstractmethod
from physics.vec2 import Vec2


class Entity(ABC):
    def __init__(self, position: Vec2, hit_box, speed: int):
        self.position = position
        self.hit_box = hit_box
        self.speed = speed

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False

        return self.position == other.position and self.hit_box == other.hit_box and self.speed == other.speed

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
