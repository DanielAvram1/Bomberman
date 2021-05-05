import pygame
from copy import copy
from copy import deepcopy
from .player import Player, Bomb
from .map import  Map
from .constants import *
from random import randint
class State:

    def __init__(self, game_map, protections, current, opponent, depth, parent=None, how_to_get=None):
        self.game_map = game_map
        self.protections = protections
        self.current = current
        self.opponent = opponent
        self.parent = parent
        self.estimation = None
        self.depth = depth
        self.how_to_get = how_to_get
        self.next_state = None

    def estimate_Sun_Tzu(self):
        '''
        estimarea care combina estimarea Pacifist si estimarea Warior

        :rtype: int

        '''
        min_dist_prot = 100000
        estimation_current = 0

        dist_to_opp = abs(self.current.i - self.opponent.i) + abs(self.current.j + self.opponent.j)
        val_for_dist = 100 - dist_to_opp
        for protection in self.protections:
            i, j = protection
            min_dist_prot = min(min_dist_prot, abs(i - self.current.i) + abs(j - self.current.j))
        estimation_current += (100 - min_dist_prot) * 10
        estimation_current += self.current.nr_protections * 10000

        min_dist_prot = 100000
        estimation_opponent = 0
        for protection in self.protections:
            i, j = protection
            min_dist_prot = min(min_dist_prot, abs(i - self.opponent.i) + abs(j - self.opponent.j))
        estimation_opponent += (100 - min_dist_prot) * 10
        estimation_opponent += self.opponent.nr_protections * 10000

        if self.current.is_max:
            if self.is_final(self.opponent, self.current):
                return float('inf')
            elif self.is_final(self.current, self.opponent):
                return float('-inf')
            return estimation_current - estimation_opponent + val_for_dist
        else:
            if self.is_final(self.current, self.opponent):
                return float('inf')
            elif self.is_final(self.opponent, self.current):
                return float('-inf')
            return estimation_opponent - estimation_current + val_for_dist

    def estimate_pacifist(self):
        '''
        se prioretizeaza diferenta dintre scorurile jucatorului max si min,
        si apoi se prioretizeaza distanta pana la cea mai apropiata protectie, cu cat mai mica distanta, cu atat mai bine

        :return:
        '''
        min_dist_prot = 10000
        estimation_current = 0

        for protection in self.protections:
            i, j = protection
            min_dist_prot = min(min_dist_prot, abs(i - self.current.i) + abs(j - self.current.j))
        estimation_current += (100 - min_dist_prot) * 1000
        estimation_current += self.current.nr_protections * 1000

        min_dist_prot = 100000
        estimation_opponent = 0
        for protection in self.protections:
            i, j = protection
            min_dist_prot = min(min_dist_prot, abs(i - self.opponent.i) + abs(j - self.opponent.j))
        estimation_opponent += (100 - min_dist_prot) * 1000
        estimation_opponent += self.opponent.nr_protections * 1000

        if self.current.is_max:
            if self.is_final(self.opponent, self.current):
                return float('inf')
            elif self.is_final(self.current, self.opponent):
                return float('-inf')
            return estimation_current - estimation_opponent
        else:
            if self.is_final(self.current, self.opponent):
                return float('inf')
            elif self.is_final(self.opponent, self.current):
                return float('-inf')
            return estimation_opponent - estimation_current

    def estimate_warrior(self):
        '''
        se prioretizeaza diferenta dintre scorurile jucatorului max si min,
        si apoi se prioretizeaza distanta pana la oponent- cu cat mai mica distanta, cu atat mai bine
        :return:
        '''
        estimation_current = 0

        dist_to_opp = abs(self.current.i - self.opponent.i) + abs(self.current.j + self.opponent.j)
        val_for_dist = 100 - dist_to_opp

        estimation_current += self.current.nr_protections * 10000

        estimation_opponent = 0

        estimation_opponent += self.opponent.nr_protections * 10000

        if self.current.is_max:
            if self.is_final(self.opponent, self.current):
                return MAX
            elif self.is_final(self.current, self.opponent):
                return -MAX
            return estimation_current - estimation_opponent + val_for_dist
        else:
            if self.is_final(self.current, self.opponent):
                return MAX
            elif self.is_final(self.opponent, self.current):
                return -MAX
            return estimation_opponent - estimation_current + val_for_dist

    def is_final(self, current, opponent):

        if current.nr_protections == 0:
            return True

        i = current.i
        j = current.j

        dirs = ((0, -1), (0, 1), (-1, 0), (1, 0))

        for dir in dirs:
            if self.game_map[i + dir[0]][j + dir[1]] == '#':
                continue
            else:
                cont = False
                if (current.i + dir[0], current.j + dir[1]) == (opponent.i, opponent.j):
                    cont = True

                if not cont:
                    for b in current.bombs:
                        if b.i == i + dir[0] and b.j == j + dir[1] and b.state == INACTIVE:
                            cont = True
                            break

                if not cont:
                    for b in opponent.bombs:
                        if b.i == i + dir[0] and b.j == j + dir[1] and b.state == INACTIVE:
                            cont = True
                            break

                if not cont:
                    return False
        return True


    def add_by_directions(self, move_list, possible_directions, or_current, or_opponent, or_map, or_protections, depth, action):
        for direction in possible_directions:
            next_current = deepcopy(or_current)
            next_opponent = deepcopy(or_opponent)
            next_game_map = deepcopy(or_map)
            next_protections = deepcopy(or_protections)

            next_current.damaged = False
            next_opponent.damaged = False

            i, j = direction
            next_current.i, next_current.j = i, j
            if (i, j) in or_protections:
                next_current.nr_protections += 1
                next_protections.remove((i, j))

            for b in next_current.bombs:
                if b.check_range(next_game_map, i, j) and b.state != INACTIVE:
                    b.estimate_explode_damage(self.game_map, (next_current, next_opponent))
                    next_current.bombs.remove(b)

            for b in next_opponent.bombs:
                if b.check_range(next_game_map, i, j) and b.state != INACTIVE:
                    b.estimate_explode_damage(self.game_map, (next_current, next_opponent))
                    next_opponent.bombs.remove(b)

            next_current.damaged = False
            next_opponent.damaged = False

            move_list.append(State(next_game_map, next_protections, next_opponent, next_current, depth - 1, self, (action, direction)))

    def generate_moves(self):
        '''
        se genereaza toate miscarile posibile de trei ori:
        1. fara plasarea bombei
        2. cu plasarea bombei
        3. cu activarea unei bombe

        :return:
        '''
        potential_directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        possible_directions = []

        for direction in potential_directions:
            i, j = direction
            i += self.current.i
            j += self.current.j
            cont = True
            for b in self.opponent.bombs:
                if (i, j) == (b.i, b.j):
                    cont = False
                    break
            if cont:
                for b in self.current.bombs:
                    if (i, j) == (b.i, b.j):
                        cont = False
                        break

            if self.game_map[i][j] != '#' and (i, j) != (self.opponent.i, self.opponent.j) and cont:
                possible_directions.append((i, j))

        move_list = []
        action = None
        # move with no actions
        if self.current.time_with_no_bomb > 0:
            self.current.time_with_no_bomb -= 1
            self.add_by_directions(move_list, possible_directions, self.current, self.opponent, self.game_map, self.protections, self.depth, action)
            self.current.time_with_no_bomb += 1


        # move with activating a bomb and maybe putting another one
        if self.current.time_with_no_bomb > 0:
            next_current = deepcopy(self.current)
            next_opponent = deepcopy(self.opponent)
            next_current.time_with_no_bomb -= 1
            inac = None
            for i in range(len(self.current.bombs)):
                if self.current.bombs[i].state == INACTIVE:
                    inac = i
                    break

            if inac is not None:
                action = ('a', inac)
                next_current.bombs[inac].activate()
                self.add_by_directions(move_list, possible_directions, next_current, next_opponent, self.game_map, self.protections, self.depth, action )

        # move with placing a bomb
        next_current = deepcopy(self.current)
        next_opponent = deepcopy(self.opponent)
        next_current.time_with_no_bomb = Player.K
        for b in next_current.bombs:
            if b.state == INACTIVE:
                b.state = PREACTIVE
                break

        action = 'b'
        next_current.bombs.append(Bomb(next_current.i, next_current.j))
        self.add_by_directions(move_list, possible_directions, next_current, next_opponent, self.game_map,
                               self.protections, self.depth, action)

        return move_list


if __name__ == "__main__":
    map = Map(0)

    player1 = Player(1, 1, BLUE, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_q, pygame.K_e)
    player2 = Player(map.height - 2, map.width - 2, RED, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT,
                     pygame.K_RCTRL, pygame.K_RSHIFT)
    players = [player1, player2]

    state = State(map.current_map, player1, player2, None)
    state.generate_moves()


