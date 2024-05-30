class HitBox:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def __eq__(self, other):
        if not isinstance(other, HitBox):
            return False

        return self.top_left == other.top_left and self.bottom_right == other.bottom_right

    def is_intersecting(self, obj):
        x1_min, x1_max = self.top_left.x, self.bottom_right.x
        x2_min, x2_max = obj.top_left.x, obj.bottom_right.x
        x_overlap = max(0, min(x1_max, x2_max) - max(x1_min, x2_min))

        y1_min, y1_max = self.top_left.y, self.bottom_right.y
        y2_min, y2_max = obj.top_left.y, obj.bottom_right.y
        y_overlap = max(0, min(y1_max, y2_max) - max(y1_min, y2_min))

        return x_overlap > 0 and y_overlap > 0

    def move(self, delta):
        self.top_left += delta
        self.bottom_right += delta

    def move_to(self, position):
        delta = self.bottom_right - self.top_left
        self.top_left = position
        self.bottom_right = position + delta


if __name__ == '__main__':
    pass
