from .constants import *



class Player:

    START_PROTECTIONS = 3

    def __init__(self, i, j, color, up, left, down, right, put, explode, K, start_protections, is_computer=False):
        self.i = i
        self.j = j
        self.color = color
        self.up = up
        self.left = left
        self.down = down
        self.right = right
        self.put = put
        self.explode = explode
        self.bombs = []
        self.nr_protections = start_protections
        self.is_computer = is_computer
        self.is_max = False
        Player.K = K
        self.time_with_no_bomb = Player.K
        self.bomb_putted = False
        self.moves_cnt = 0
        self.damaged = False
        self.moved = False

    def draw(self, map, players):
        for bomb in self.bombs:
            bomb.draw(map, players)
        map.draw_tile(self.i, self.j, self.color)

    def bomb_activate(self, map, players, bomb):
        bomb.activate()


class Bomb:
    color = BLACK
    range = 4

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.state = INACTIVE

    def covers(self, map, x, y):
        return (self.i, self.j) == map.covers(x, y)

    def draw(self, map, players):

        if self.state == EXPLODING:
            self.draw_explosion(map, players)
        if self.state == ACTIVE:
            self.draw_active(map, players)
        map.draw_tile(self.i, self.j, self.color, True)

    def check_range(self, game_map, i, j):
        if i == self.i:
            jj = j
            dj = 1
            if j < self.j:
                dj = -1
            while game_map[i][jj] != '#':
                if jj == j:
                    return True
                jj += dj

        if j == self.j:
            ii = i
            di = 1
            if i < self.i:
                di = -1
            while game_map[ii][j] != '#':
                if ii == i:
                    return True
                ii += di
        return False

    def estimate_explode_damage(self, game_map, players):
        dirs = ((0, 1), (-1, 0), (0, -1), (1, 0))
        self.state = EXPLOSION
        for dir in dirs:
            i = self.i
            j = self.j
            dist = 1
            while True:
                i += dir[0]
                j += dir[1]
                if not (0 <= i < len(game_map) and 0<= j < len(game_map[i])):
                    break
                for p in players:
                    if (i, j) == (p.i, p.j):
                        if not p.damaged:
                            p.nr_protections -= 1
                            p.damaged = True
                        for b in p.bombs:
                            if (i, j) == (p.i, p.j) and self.state != EXPLOSION:
                                b.estimate_explode_damage(game_map, players)
                                p.bombs.remove(b)
                dist += 1


    def activate(self):
        self.state = PREACTIVE

    def explode(self, map, players):
        self.draw_explosion(map, players)
        self.state = EXPLODING

    def draw_active(self, map, players):
        dirs = ((0, 1), (-1, 0), (0, -1), (1, 0))

        for dir in dirs:
            i = self.i
            j = self.j
            dist = 1
            while True:
                i += dir[0]
                j += dir[1]
                if map.current_map[i][j] != '#':
                    map.draw_tile(i, j, ORANGE)
                else:
                    break
                dist += 1
                if self.state == ACTIVE:
                    for p in players:
                        if (p.i, p.j) == (i, j) and p.moved:
                            self.state = EXPLOSION
                            self.draw_explosion(map, players)


    def draw_explosion(self, map, players):
        dirs = ((0, 1), (-1, 0), (0, -1), (1, 0))

        for dir in dirs:
            i = self.i
            j = self.j
            dist = 1
            while True:
                i += dir[0]
                j += dir[1]
                if 0 <= i < len(map.current_map) and 0<= j < len(map.current_map[i]):
                        map.draw_tile(i, j, YELLOW)
                else:
                    break
                dist += 1
                if self.state == EXPLOSION:
                    for p in players:
                        if (i, j) == (p.i, p.j):
                            if not p.damaged:
                                p.nr_protections -= 1
                                p.damaged = True
                        for b in p.bombs:
                            if (i, j) == (b.i, b.j) and b.state != EXPLOSION and b.state != EXPLODING:
                                b.state = EXPLOSION
                                b.draw_explosion(map, players)
        self.state = EXPLODING

