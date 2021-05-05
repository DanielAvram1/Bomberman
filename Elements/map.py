
from .constants import *
from copy import deepcopy

class Map:

    '''
    clasa care incapsuleaza informatiile ce tin de harta jocului
    '''

    # lista tuturor hartilor care pot fi alese
    map_list = [
        [
            '######################',
            '#1p    #      #      #',
            '# #  ###   ####  #####',
            '# #                  #',
            '#    p #  p  #  ### ##',
            '##########           #',
            '# #     #   ####    ##',
            '#             p      #',
            '# #######   #######  #',
            '#    #  #   #p       #',
            '# ####  #   ### ### p#',
            '#         #         2#',
            '######################'
        ],
        [
            '##########',
            '#1  #p#  #',
            '#  # p   #',
            '#  p     #',
            '#p#  p  2#',
            '##########'
        ],
        [
            '######################',
            '#1p    #      #      #',
            '# # ####         #####',
            '# #                  #',
            '#    p #  p  #  ### ##',
            '##  #  ###           #',
            '# #     #   ####    ##',
            '#             p      #',
            '# ## ####   ##  ###  #',
            '#    #  #    p       #',
            '# ## #    p ### ##  p#',
            '#                   2#',
            '######################'
        ]
    ]

    tile_color = {
        '#': (50, 50, 50),
        ' ': (240, 240, 240),
        'p': (0, 255, 0),
        'b': (0, 0, 0)
    }

    TILE_SIZE = 40


    def __init__(self, map_nr):
        '''
        pe langa initializare, functia proceseaza harta aleasa pentru a face lista de protectii
        si pozitia initiala a fiecarui jucator

        :param map_nr: indecele hartii alese
        '''
        self.current_map = deepcopy(Map.map_list[map_nr])


        for i in range(len(self.current_map)):
            self.current_map[i] = list(self.current_map[i])

        self.protections = []
        for i in range(len(self.current_map)):
            for j in range(len(self.current_map[i])):
                if self.current_map[i][j] == 'p':
                    self.protections.append((i, j))
                elif self.current_map[i][j] == '1':
                    self.player1 = (i, j)
                elif self.current_map[i][j] == '2':
                    self.player2 = (i, j)
                if self.current_map[i][j] != '#':
                    self.current_map[i][j] = ' '


        self.width = len(self.current_map[0])
        self.height = len(self.current_map)

        self.margin = min((WIDTH - self.width * self.TILE_SIZE)//2,
                          ((HEIGHT - HEADER_HEIGHT) - self.height * self.TILE_SIZE) // 2)

    def covers(self, x, y):
        '''
        functia care returneaza in care 'patratel' din harta s-a facut click
        :param x: coordonata x
        :param y: coordonata y
        :return: indicii patratelului pe care s-a facut click
        '''
        i = (y - HEADER_HEIGHT - self.margin) // self.TILE_SIZE
        j = (x - self.margin) // self.TILE_SIZE
        return i, j

    def draw_tile(self, i, j, color, circle=False):
        '''
        functia care deseneaza un patratel la indicii alesi
        :param i: indicele i
        :param j: indicele j
        :param color: culoarea tile-ului
        :param circle: daca sa se deseneze un cerc sau sa ramana patratel
        '''
        y = i * self.TILE_SIZE + HEADER_HEIGHT + self.margin
        x = j * self.TILE_SIZE + self.margin
        tile = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
        if circle is False:
            pygame.draw.rect(WIN, color, tile)
            pygame.draw.rect(WIN, color, tile)
        else:
            pygame.draw.circle(WIN, color, (x + self.TILE_SIZE // 2, y + self.TILE_SIZE // 2), self.TILE_SIZE // 2)

    def draw(self, win, protections):
        '''
        functia de desenare a hartii
        :param win:
        :param protections:
        :return:
        '''
        map_width = len(self.current_map[0])
        map_height = len(self.current_map)

        for i in range(map_height):
            for j in range(map_width):
                color = self.tile_color[self.current_map[i][j]]
                self.draw_tile(i, j, color)

        for protection in protections:
            color = (0, 255, 0)
            i, j = protection
            self.draw_tile(i, j, color)
