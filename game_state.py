import json
import entities
import projectiles
from physics.vec2 import Vec2
from projectiles.player_bullet import PlayerBullet


class GameState:
    def __init__(self):
        self.player = None
        self.bunkers = []
        self.aliens = []
        self.mystery_ship = None
        self.bullets = []

        self.score = 0
        self.lives = 0

    def save(self):
        game_state = {
            'player': (self.player.position.x, self.player.position.y),
            'bunkers': [GameState.__save_bunker_state(bunker) for bunker in self.bunkers],
            'aliens': [(alien.position.x, alien.position.y) for alien in self.aliens],
            'bullets': [GameState.__save_bullet_state(bullet) for bullet in self.bullets],
            'mystery_ship': GameState.__save_mystery_ship_state(self.mystery_ship),
            'score': self.score,
            'lives': self.lives
        }

        with open('game_state.json', 'w') as f:
            json.dump(game_state, f)

    def load(self):

        with open('game_state.json', 'r') as f:
            game_state = json.load(f)
            self.player = entities.player.Player(Vec2(game_state['player'][0], game_state['player'][1]), 1)
            self.bunkers = [GameState.__load_bunker_state(bunker_state) for bunker_state in game_state['bunkers']]
            self.aliens = [entities.alien.Alien(Vec2(alien_state[0], alien_state[1]), 1) for alien_state in game_state['aliens']]
            self.mystery_ship = GameState.__load_mystery_ship_state(game_state['mystery_ship'])
            self.bullets = [GameState.__load_bullet_state(bullet_state) for bullet_state in game_state['bullets']]

            self.score = game_state['score']
            self.lives = game_state['lives']

    @staticmethod
    def __save_bunker_state(bunker):
        return {
            'position': (bunker.position.x, bunker.position.y),
            'health': bunker.health
        }

    @staticmethod
    def __load_bunker_state(state):
        bunker = entities.bunker.Bunker(Vec2(state['position'][0], state['position'][1]))
        bunker.health = state['health']

        return bunker

    @staticmethod
    def __save_mystery_ship_state(mystery_ship):
        return {
            'position': (mystery_ship.position.x, mystery_ship.position.y),
            'direction': (mystery_ship.direction.x, mystery_ship.direction.y),
            'is_active': mystery_ship.is_active
        }

    @staticmethod
    def __load_mystery_ship_state(state):
        mystery_ship = entities.mystery_ship.MysteryShip(Vec2(state['position'][0], state['position'][1]), 1)
        mystery_ship.direction = Vec2(state['direction'][0], state['direction'][1])
        mystery_ship.is_active = state['is_active']

        return mystery_ship

    @staticmethod
    def __save_bullet_state(bullet):
        if isinstance(bullet, PlayerBullet):
            owner = 'player'
        else:
            owner = 'alien'

        return {
            'owner': owner,
            'direction': (bullet.direction.x, bullet.direction.y),
            'position': (bullet.position.x, bullet.position.y),
        }

    @staticmethod
    def __load_bullet_state(state):
        if state['owner'] == 'player':
            bullet = projectiles.player_bullet.PlayerBullet(Vec2(state['position'][0], state['position'][1]),
                                                            Vec2(state['direction'][0], state['direction'][1]), 1)
        else:
            bullet = projectiles.alien_bullet.AlienBullet(Vec2(state['position'][0], state['position'][1]),
                                                          Vec2(state['direction'][0], state['direction'][1]), 1)

        return bullet
