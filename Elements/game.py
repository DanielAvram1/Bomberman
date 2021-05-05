from copy import copy

from copy import deepcopy
from time import time

from .map import Map
from .player import Player, Bomb
from .state import State
from .algorithms import algorithms
from .menu import *


class Game:
    '''
    clasa singleton care 'reprezinta' tot jocul
    '''
    algorithm = None
    player = None
    depth = None
    sections = []
    buttons = []
    start_play = False
    header = None
    players = []
    map = None
    style = None
    protections = []
    go_menu2 = False
    heuristic1 = None
    heuristic2 = None

    def __init__(self, K, START_PROTECTIONS):
        '''
        se initializeaza cu parametrii dati in consola

        :param K: numarul de pasi dupa care se va pune o bomba
        :param START_PROTECTIONS: numarul de protectii a jucatorilor la inceputul jocului
        '''
        Game.K = K
        Game.START_PROCTECTIONS = START_PROTECTIONS

    def menu1(self):
        '''
        functia care proceseaza primul meniu
        '''
        self.header = Header()
        self.players = []
        self.buttons = []
        self.menu1_sections = []
        self.algorithm = None
        self.player = None
        self.depth = None

        def choose_alfa_beta():
            Game.algorithm = algorithms['alpha_beta']
            print('alfa_beta')

        def choose_min_max():
            Game.algorithm = algorithms['min_max']
            print('min_max')

        def start_game():
            if Game.style is not None and Game.algorithm is not None and Game.depth is not None:
                Game.go_menu2 = True

        min_max = Button('MIN MAX', choose_min_max)
        alpha_beta = Button('ALPHA BETA', choose_alfa_beta)
        new_game = Button('NEW GAME', start_game, LIME)
        self.buttons.append(min_max)
        self.buttons.append(alpha_beta)
        self.buttons.append(new_game)
        algorithm_section = Section('Algorithm:', (min_max, alpha_beta, new_game), 0, Header.height)
        self.menu1_sections.append(algorithm_section)

        def choose_player1():
            Game.style = '1'
            Game.heuristic1 = 'real player'

        def choose_player2():
            Game.style = '2'
            Game.heuristic2 = 'real player'

        def choose_eve():
            Game.style = 'e'

        def choose_pvp():
            Game.style = 'p'
            Game.heuristic1 = 'real player'
            Game.heuristic2 = 'real player'

        player1 = Button('PLAYER 1', choose_player1)
        player2 = Button('PLAYER 2', choose_player2)
        eve = Button('Engine vs Engine', choose_eve)
        pvp = Button('Player vs Player', choose_pvp)
        self.buttons.append(player1)
        self.buttons.append(player2)
        self.buttons.append(eve)
        self.buttons.append(pvp)

        player_section = Section('Player:', (player1, player2, eve, pvp), Section.width, Header.height)
        self.menu1_sections.append(player_section)

        def choose_easy():
            Game.depth = 3

        def choose_normal():
            Game.depth = 5

        def choose_hard():
            Game.depth = 7

        easy = Button('EASY', choose_easy)
        normal = Button('NORMAL', choose_normal)
        hard = Button('HARD', choose_hard)
        self.buttons.append(easy)
        self.buttons.append(normal)
        self.buttons.append(hard)
        difficulty_section = Section('Difficulty:', (easy, normal, hard), Section.width * 2, Header.height)
        self.menu1_sections.append(difficulty_section)

        menu1 = Menu(self.menu1_sections, Header())

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for section in self.menu1_sections:
                        for button in section.buttons:
                            if button.covers(x, y):
                                if button.text != 'NEW GAME':
                                    for button2 in section.buttons:
                                        button2.highlighted = False
                                    button.highlighted = True
                                button.on_choose()
                                break

            if Game.go_menu2:
                # self.play()
                self.menu2()
                Game.go_menu2 = False

            menu1.draw()

        pygame.quit()

    def menu2(self):
        '''
        functia care proceseaza al doilea meniu

        '''
        self.menu2_sections = []

        def choose_map1():
            Game.map = Map(0)
            print('mapa Chisinau')

        def choose_map2():
            Game.map = Map(1)
            print('mapa Riga')

        def choose_map3():
            Game.map = Map(2)
            print('mapa Riga')

        def start_game():
            print(Game.heuristic1, Game.heuristic2, Game.map)
            if Game.heuristic1 is not None and Game.heuristic2 is not None and Game.map is not None:
                Game.start_play = True

        map1 = Button('CHISINAU', choose_map1)
        map2 = Button('RIGA', choose_map2)
        map3 = Button('BUCURESTI', choose_map3)
        start = Button('START', start_game, LIME)
        map_section = Section('Choose map:', (map1, map2, map3, start), 0, Header.height)
        self.menu2_sections.append(map_section)
        if Game.style == '2' or Game.style == 'e':
            def choose_heu1():
                Game.heuristic1 = State.estimate_Sun_Tzu

            def choose_heu2():
                Game.heuristic1 = State.estimate_pacifist

            def choose_heu3():
                Game.heuristic1 = State.estimate_warrior
                print('warrior')

            suntzu = Button('SUN TZU', choose_heu1)
            pacifist = Button('PACIFIST', choose_heu2)
            warrior = Button('WARRIOR', choose_heu3)

            player_section1 = Section('Engine 1:', (suntzu, pacifist, warrior), Section.width, Header.height)
            self.menu2_sections.append(player_section1)

        if Game.style == '1' or Game.style == 'e':
            def choose_heu1():
                Game.heuristic2 = State.estimate_Sun_Tzu
                print('suntzu')

            def choose_heu2():
                Game.heuristic2 = State.estimate_pacifist
                print('pacifist')

            def choose_heu3():
                Game.heuristic2 = State.estimate_warrior
                print('warrior')

            suntzu = Button('SUN TZU', choose_heu1)
            pacifist = Button('PACIFIST', choose_heu2)
            warrior = Button('WARRIOR', choose_heu3)

            player2_section = Section('Engine 2:', (suntzu, pacifist, warrior), Section.width * 2, Header.height)
            self.menu2_sections.append(player2_section)

        menu2 = Menu(self.menu2_sections, Header())

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for section in self.menu2_sections:
                        for button in section.buttons:
                            if button.covers(x, y):
                                if button.text != 'START':
                                    for button2 in section.buttons:
                                        button2.highlighted = False
                                    button.highlighted = True
                                button.on_choose()
                                break

            if Game.start_play:
                self.play()
                Game.start_play = False

            menu2.draw()

    def print_everything(self, map, players, protections):
        '''
        functia care printeaza in consola toate informatiile legate de o miscare

        :param map: harta dupa miscare
        :param players: lista cu jucatori si informatia lor
        :param protections: lista coordonatelor protectiilor
        :return: None
        '''
        map = deepcopy(map)

        for p in protections:
            map[p[0]][p[1]] = 'p'

        for i in range(len(players)):
            p = players[i]
            map[p.i][p.j] = str(i + 1)
            for b in p.bombs:
                if b.state == INACTIVE:
                    map[b.i][b.j] = 'b'
                elif b.state == ACTIVE or b.state == PREACTIVE:
                    map[b.i][b.j] = 'a'
                elif b.state == EXPLOSION or b.state == EXPLODING:
                    map[b.i][b.j] = 'e'

        for line in map:
            for c in line:
                print(c, end='')
            print(end='\n')

    def draw_header(self, players):
        '''
        functia care afiseaza headerul jocului

        :param players: lista de jucatori
        '''
        text1 = FONT.render('Player 1:' + str(players[0].nr_protections), True, BLACK, WHITE)
        text2 = FONT.render('Player 2:' + str(players[1].nr_protections), True, BLACK, WHITE)

        def back_to_menu():
            self.cont = False

        self.back_menu = Button('Back to menu', back_to_menu, RED, type="small")
        self.back_menu.draw((WIDTH - Button.width) // 2, 10)

        text1_rect = text1.get_rect()
        text2_rect = text2.get_rect()
        text2_rect.x = WIDTH - text2_rect.width

        WIN.blit(text1, text1_rect)
        WIN.blit(text2, text2_rect)

    def draw_window(self, map, players):
        '''
        functia care afiseaza fereastra jocului

        :param map: informatiile legate de harta
        :param players: lista cu jucatori
        '''
        WIN.fill(WHITE)

        self.draw_header(players)
        map.draw(WIN, self.protections)
        for p in players:
            p.draw(map, players)
        pygame.display.update()

    def play(self):
        '''
        functia-cheie care proceseaza starea jocului in dependenta de tipul jucatorilor, a hartii si aeuristicii alese

        '''
        map = Game.map
        self.map = map
        self.protections = deepcopy(map.protections)
        self.nodes_cnt = []
        self.comp_times = []
        self.cont = True
        i, j = map.player1
        player1 = Player(i, j, BLUE, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_q, pygame.K_e, Game.K, Game.START_PROCTECTIONS)
        i, j = map.player2
        player2 = Player(i, j, RED, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_q, pygame.K_e, Game.K, Game.START_PROCTECTIONS)

        if Game.style == '1':
            player2.is_computer = True
        elif Game.style == '2':
            player1.is_computer = True
        elif Game.style == 'e':
            player2.is_computer = True
            player1.is_computer = True

        players = [player1, player2]
        self.players = players
        turn = 0
        run = True
        clock = pygame.time.Clock()
        overall_start_time = time()
        start_time = time()

        print('Este randul jucatorului {}'.format(turn + 1))
        while run:
            if not self.cont:
                break
            clock.tick(30)

            if players[turn].is_computer:
                players[turn].moved = False
                for p in players:
                    for b in p.bombs:
                        if b.state == EXPLODING or b.state == EXPLOSION:
                            p.bombs.remove(b)
                players[turn].is_max = True
                players[(turn + 1) % 2].is_max = False
                state = State(self.map.current_map, self.protections, players[turn], players[(turn + 1) % 2],
                              Game.depth)
                start_time = time()
                if turn == 0:
                    state, nr_noduri = Game.algorithm(state, Game.heuristic1)
                else:
                    state, nr_noduri = Game.algorithm(state, Game.heuristic2)
                end_time = time()

                print('Jucatorul {} (calculator):'.format(turn + 1))
                self.print_everything(self.map.current_map, players, self.protections)
                print('Scor:', players[0].nr_protections, ':', players[1].nr_protections)
                print('Estimarea:', state.estimation)
                print('Timpul de gandire:', end_time - start_time)
                print('Nr de noduri generate:', nr_noduri)

                self.comp_times.append(end_time - start_time)
                self.nodes_cnt.append(nr_noduri)
                if state.next_state is None:

                    print('Jocul s-a terminat')
                    self.comp_times = sorted(self.comp_times)
                    print('Timp minim:', self.comp_times[0])
                    print('Timp maxim:', self.comp_times[-1])
                    print('Timp median:', self.comp_times[len(self.comp_times) // 2])

                    self.nodes_cnt = sorted(self.nodes_cnt)
                    print('Nr noduri minim:', self.nodes_cnt[0])
                    print('Nr noduri maxim:', self.nodes_cnt[-1])
                    print('Nr noduri mediana:', self.nodes_cnt[len(self.nodes_cnt) // 2])

                    print('Miscari jucator 1:', players[0].moves_cnt)
                    print('Miscari jucator 2:', players[1].moves_cnt)

                    if players[(turn + 1) % 2].is_computer:
                        if state.estimation == MAX:
                            self.game_over(WHITE, 'Player {} won!'.format(turn + 1))
                        elif state.estimation == -MAX:
                            self.game_over(WHITE, 'Player {} won!'.format((turn + 1) % 2 + 1))
                       # else:
                      #      self.game_over(WHITE, 'Draw!'.format((turn + 1) % 2 + 1))
                    else:
                        if state.estimation == MAX:
                            self.game_over(RED, 'You lost!', 'Player {} won!'.format(turn + 1))
                        elif state.estimation == -MAX:
                            self.game_over(LIME, 'You won!', 'Player {} won!'.format((turn + 1) % 2 + 1))
                    #    else:
                     #       self.game_over(WHITE, 'Draw!5'.format((turn + 1) % 2 + 1))

                    return
                action, direction = state.next_state.how_to_get
                i = copy(players[turn].i)
                j = copy(players[turn].j)
                if action is not None:
                    if action == 'b':
                        for b in players[turn].bombs:
                            b.state = PREACTIVE
                        players[turn].bombs.append(Bomb(i, j))
                        players[turn].time_with_no_bomb = Player.K

                    elif action[0] == 'a':
                        to_activate = players[turn].bombs[action[1]]
                        players[turn].bomb_activate(map, players, to_activate)
                        players[turn].time_with_no_bomb -= 1

                else:
                    players[turn].time_with_no_bomb -= 1

                i, j = direction
                if map.current_map[i][j] == ' ' and (i, j) not in self.protections:
                    players[turn].i = i
                    players[turn].j = j
                elif (i, j) in self.protections:
                    self.protections.remove((i, j))
                    players[turn].i = i
                    players[turn].j = j
                    players[turn].nr_protections += 1

                for b in players[turn].bombs:
                    if b.state == PREACTIVE:
                        b.state = ACTIVE


                start_time = time()
                players[turn].moves_cnt += 1
                players[turn].damaged = False
                for p in players:
                    for b in p.bombs:
                        if b.state == EXPLODING or b.state == EXPLOSION:
                            p.bombs.remove(b)
                players[turn].moved = True
                players[(turn + 1) % 2].moved = False
                print('Este randul jucatorului {}'.format((turn + 1) % 2 + 1))
                turn = (turn + 1) % 2

            else:   # real player
                players[turn].moved = False
                if self.is_final(map, players, turn):
                    print('Jocul s-a terminat')
                    if len(self.comp_times) > 0:
                        self.comp_times = sorted(self.comp_times)
                        print('Timp minim:', self.comp_times[0])
                        print('Timp maxim:', self.comp_times[-1])
                        print('Timp median:', self.comp_times[len(self.comp_times) // 2])

                        self.nodes_cnt = sorted(self.nodes_cnt)
                        print('Nr noduri minim:', self.nodes_cnt[0])
                        print('Nr noduri maxim:', self.nodes_cnt[-1])
                        print('Nr noduri mediana:', self.nodes_cnt[len(self.nodes_cnt) // 2])

                    print('Miscari jucator 1:', players[0].moves_cnt)
                    print('Miscari jucator 2:', players[1].moves_cnt)

                    self.game_over(RED, 'You lost!', 'Player {} won!'.format((turn + 1) % 2 + 1))
                    return

                key_pressed = pygame.key.get_pressed()
                x, y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONDOWN:
                        for p in players:
                            for b in p.bombs:
                                if b.state == EXPLODING:
                                    p.bombs.remove(b)
                        if event.type == pygame.KEYUP:
                            i = copy(players[turn].i)
                            j = copy(players[turn].j)

                            #
                            # if key_pressed[players[turn].explode]:
                            #         if players[turn].bomb is not None:
                            #             players[turn].bomb_explode(map, players)

                            if players[turn].time_with_no_bomb == 0 and not players[turn].bomb_putted:
                                for b in players[turn].bombs:
                                    b.state = PREACTIVE
                                players[turn].bombs.append(Bomb(i, j))
                                players[turn].bomb_putted = True
                                players[turn].time_with_no_bomb = Player.K

                            if key_pressed[players[turn].put]:
                                if not players[turn].bomb_putted:
                                    for b in players[turn].bombs:
                                        b.state = PREACTIVE
                                    players[turn].bombs.append(Bomb(i, j))
                                    players[turn].bomb_putted = True
                                    players[turn].time_with_no_bomb = Player.K
                        else:

                            if self.back_menu.covers(x, y):
                                print('Jocul s-a terminat')
                                if len(self.comp_times) > 0:
                                    self.comp_times = sorted(self.comp_times)
                                    print('Timp minim:', self.comp_times[0])
                                    print('Timp maxim:', self.comp_times[-1])
                                    print('Timp median:', self.comp_times[len(self.comp_times) // 2])

                                    self.nodes_cnt = sorted(self.nodes_cnt)
                                    print('Nr noduri minim:', self.nodes_cnt[0])
                                    print('Nr noduri maxim:', self.nodes_cnt[-1])
                                    print('Nr noduri mediana:', self.nodes_cnt[len(self.nodes_cnt) // 2])

                                print('Miscari jucator 1:', players[0].moves_cnt)
                                print('Miscari jucator 2:', players[1].moves_cnt)
                                return

                            for b in players[turn].bombs:
                                if b.covers(map, x, y):
                                    if b.state == INACTIVE:
                                        b.state = PREACTIVE

                        move = False
                        if event.type == pygame.KEYUP:
                            correct_key = False
                            if key_pressed[players[turn].up]:
                                i -= 1
                                correct_key = True
                            elif key_pressed[players[turn].left]:
                                j -= 1
                                correct_key = True
                            elif key_pressed[players[turn].down]:
                                i += 1
                                correct_key = True
                            elif key_pressed[players[turn].right]:
                                j += 1
                                correct_key = True
                            if correct_key:
                                cont = True
                                for p in players:
                                    if (i, j) == (p.i, p.j):
                                        cont = False
                                        break
                                    for b in p.bombs:
                                        if (i, j) == (b.i, b.j):
                                            cont = False
                                            break
                                    if not cont:
                                        break

                                if cont and map.current_map[i][j] == ' ' and (i, j) not in self.protections:
                                    players[turn].i = i
                                    players[turn].j = j
                                    move = True

                                elif cont and (i, j) in self.protections:
                                    self.protections.remove((i, j))
                                    players[turn].i = i
                                    players[turn].j = j
                                    players[turn].nr_protections += 1
                                    move = True

                        if move:
                            end_time = time()
                            players[turn].bomb_putted = False
                            players[turn].time_with_no_bomb -= 1
                            for b in players[turn].bombs:
                                if b.state == PREACTIVE:
                                    b.state = ACTIVE
                            for p in players:
                                for b in p.bombs:
                                    if b.state == EXPLODING:
                                        p.bombs.remove(b)
                            players[turn].damaged = False
                            players[turn].moves_cnt += 1

                            print('Jucatorul {} (persoana):'.format(turn + 1))
                            self.print_everything(self.map.current_map, players, self.protections)
                            print('Scor:', players[0].nr_protections, ':', players[1].nr_protections)
                            print('Timpul de gandire:', end_time - start_time)
                            print('Este randul jucatorului {}'.format((turn + 1) % 2 + 1))

                            players[turn].moved = True
                            players[(turn + 1)%2].moved = False
                            if turn == 0:
                                turn = 1
                            else:
                                turn = 0

            self.draw_window(map, players)


    def is_final(self, map, players, turn):
        '''
        Functie care verifica daca jocul este sau nu in stare finala

        :param map: harta la momentul verificarii
        :param players: starea jucatorilor la momentul verificarii
        :param turn: al cui a fost randul de a misca
        :rtype: Bool
        '''
        current = players[turn]
        opponent = players[(turn + 1) % 2]

        if current.nr_protections == 0:
            return True

        i = current.i
        j = current.j

        dirs = ((0, -1), (0, 1), (-1, 0), (1, 0))

        for dir in dirs:
            if map.current_map[i + dir[0]][j + dir[1]] == '#':
                continue
            else:
                cont = False
                if (current.i + dir[0], current.j + dir[1]) == (opponent.i, opponent.j):
                    cont = True

                if not cont:
                    for b in current.bombs:
                        if b.i == i + dir[0] and b.j == j + dir[1] and b.state != EXPLOSION and b.state != EXPLODING:
                            cont = True
                            break

                if not cont:
                    for b in opponent.bombs:
                        if b.i == i + dir[0] and b.j == j + dir[1] and b.state != EXPLOSION and b.state != EXPLODING:
                            cont = True
                            break

                if not cont:
                    return False
        return True

    def draw_final(self, button, color, top_text, bottom_text=''):
        '''
        functia care afiseaza fereastra la finalul jocului
        :param button: butonul de intoarcere la meniul precedent
        :param color: culoarea fonului
        :param top_text: textul de castig/pierdere
        :param bottom_text: care jucator a castigat/pierdut
        '''
        WIN.fill(WHITE)

        self.draw_header(self.players)
        self.map.draw(WIN, self.protections)
        victorious = None
        for p in self.players:
            p.draw(self.map, self.players)
            if p.nr_protections != 0:
                victorious = p

        text = top_text
        win_text = bottom_text
        bg_color = color
        OPACITY = 200
        background = pygame.Surface((WIDTH, HEIGHT))
        background.set_alpha(OPACITY)
        background.fill(bg_color)
        WIN.blit(background, (0, 0))

        text1 = FONT_LARGE.render(text, True, BLACK, bg_color)
        text2 = FONT_LARGE.render(win_text, True, BLACK, bg_color)

        text1_rect = text1.get_rect()
        text2_rect = text2.get_rect()

        WIN.blit(text1, (WIDTH//2 - text1_rect.width // 2, HEIGHT//2 - text1_rect.height))
        WIN.blit(text2, (WIDTH//2 - text2_rect.width // 2, HEIGHT//2 + text1_rect.height))

        button.draw(10, 30)
        pygame.display.update()

    def game_over(self, color, top_text, bottom_text=''):
        '''
        functia care proceseaza finalul jocului

        :param color: culoarea de pe fon
        :param top_text: textul de castig/pierdere
        :param bottom_text: informatii despre jucatorul care a castigat/pierdut
        '''
        run = True

        def back_menu():
            Game.start_play = False
            self.menu1()

        back_menu = Button('Back to the menu', back_menu, WHITE)
        self.buttons.append(back_menu)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if back_menu.covers(x, y):
                        return
            self.draw_final(back_menu, color, top_text, bottom_text)
