import math


class Vec2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vec2):
            return False

        return self.x == other.x and self.y == other.y

    def length(self):
        return math.sqrt(self.dot(self))

    def normalize(self):
        length = self.length()

        if length == 0:
            return Vec2(0, 0)

        return Vec2(self.x / length, self.y / length)

    def dot(self, other):
        return self.x * other.x + self.y * other.y


if __name__ == '__main__':
    pass
