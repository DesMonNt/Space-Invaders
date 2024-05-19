from random import random
from entities.alien import Alien
from physics.vec2 import Vec2


class AlienWave:
    def __init__(self, start_position, width, height, block_size):
        self.aliens = AlienWave.__fill_aliens(start_position, width, height, block_size)
        self.__shoot_rate = 0.0002
        self.__screen_size = (width, height)
        self.__block_size = block_size
        self.__direction = Vec2(1, 0)

    def move_horizontal(self):
        if self.aliens.__len__() == 0:
            return

        for alien in self.aliens:
            if alien.position.x >= self.__screen_size[0] - self.aliens[0].speed:
                self.__direction = Vec2(-1, 0)
            if alien.position.x <= self.__block_size:
                self.__direction = Vec2(1, 0)

        delta = Vec2(self.__direction.x, self.__direction.y) * self.aliens[0].speed

        for alien in self.aliens:
            alien.move(delta)

    def move_down(self):
        if self.aliens.__len__() == 0:
            return

        delta = Vec2(0, 1) * self.aliens[0].speed

        for alien in self.aliens:
            alien.move(delta)

    def get_aliens_bullets(self):
        if self.aliens.__len__() == 0:
            return

        bullets = []

        for alien in self.aliens:
            if random() < self.__shoot_rate:
                bullets.append(alien.shoot())

        return bullets

    @staticmethod
    def __fill_aliens(starts_position, width, height, block_size):
        aliens = []

        for i in range(22):
            for j in range(10):
                if i % 2 == j % 2:
                    continue

                x = starts_position.x + i * block_size
                y = starts_position.y + j * block_size

                if x > width or y > height // 1.5:
                    continue

                aliens.append(Alien(Vec2(x, y), block_size))

        return aliens
