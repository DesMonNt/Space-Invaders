import unittest
from physics.vec2 import Vec2
from physics.hit_box import HitBox


class TestHitBox(unittest.TestCase):
    def test_init(self):
        top_left = Vec2(10, 10)
        bottom_right = Vec2(20, 20)
        hit_box = HitBox(top_left, bottom_right)
        self.assertEqual(hit_box.top_left, top_left)
        self.assertEqual(hit_box.bottom_right, bottom_right)

    def test_eq(self):
        hit_box1 = HitBox(Vec2(10, 10), Vec2(20, 20))
        hit_box2 = HitBox(Vec2(10, 10), Vec2(20, 20))
        hit_box3 = HitBox(Vec2(15, 15), Vec2(25, 25))
        self.assertEqual(hit_box1, hit_box2)
        self.assertNotEqual(hit_box1, hit_box3)

    def test_is_intersecting(self):
        hit_box1 = HitBox(Vec2(10, 10), Vec2(20, 20))
        hit_box2 = HitBox(Vec2(15, 15), Vec2(25, 25))
        hit_box3 = HitBox(Vec2(30, 30), Vec2(40, 40))
        self.assertTrue(hit_box1.is_intersecting(hit_box2))
        self.assertFalse(hit_box1.is_intersecting(hit_box3))

    def test_move(self):
        hit_box = HitBox(Vec2(10, 10), Vec2(20, 20))
        delta = Vec2(5, 5)
        hit_box.move(delta)
        self.assertEqual(hit_box.top_left, Vec2(15, 15))
        self.assertEqual(hit_box.bottom_right, Vec2(25, 25))

    def test_move_to(self):
        hit_box = HitBox(Vec2(10, 10), Vec2(20, 20))
        new_position = Vec2(50, 50)
        hit_box.move_to(new_position)
        self.assertEqual(hit_box.top_left, new_position)
        self.assertEqual(hit_box.bottom_right, Vec2(60, 60))
