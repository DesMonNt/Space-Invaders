from math import pi
import unittest
from physics.vec2 import Vec2


class TestVec2(unittest.TestCase):
    def test_init(self):
        v = Vec2(1.0, 2.0)
        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 2.0)

    def test_add(self):
        v1 = Vec2(1.0, 2.0)
        v2 = Vec2(3.0, 4.0)
        v3 = v1 + v2
        self.assertEqual(v3.x, 4.0)
        self.assertEqual(v3.y, 6.0)

    def test_sub(self):
        v1 = Vec2(1.0, 2.0)
        v2 = Vec2(3.0, 4.0)
        v3 = v1 - v2
        self.assertEqual(v3.x, -2.0)
        self.assertEqual(v3.y, -2.0)

    def test_mul(self):
        v1 = Vec2(1.0, 2.0)
        v2 = v1 * 2.0
        self.assertEqual(v2.x, 2.0)
        self.assertEqual(v2.y, 4.0)

    def test_truediv(self):
        v1 = Vec2(1.0, 2.0)
        v2 = v1 / 2.0
        self.assertEqual(v2.x, 0.5)
        self.assertEqual(v2.y, 1.0)

    def test_eq(self):
        v1 = Vec2(1.0, 2.0)
        v2 = Vec2(1.0, 2.0)
        v3 = Vec2(3.0, 4.0)
        self.assertEqual(v1, v2)
        self.assertNotEqual(v1, v3)

    def test_length(self):
        v1 = Vec2(3.0, 4.0)
        self.assertEqual(v1.length(), 5.0)

    def test_normalize(self):
        v1 = Vec2(3.0, 4.0)
        v2 = v1.normalize()
        self.assertAlmostEqual(v2.x, 0.6, delta=1e-6)
        self.assertAlmostEqual(v2.y, 0.8, delta=1e-6)

    def test_dot(self):
        v1 = Vec2(1.0, 2.0)
        v2 = Vec2(3.0, 4.0)
        self.assertEqual(v1.dot(v2), 11.0)

    def test_rotate(self):
        v1 = Vec2(1.0, 0.0)
        v2 = v1.rotate(pi / 2)
        self.assertAlmostEqual(v2.x, 0.0, delta=1e-6)
        self.assertAlmostEqual(v2.y, 1.0, delta=1e-6)