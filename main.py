import pygame
import sys
from Elements.game import Game

pygame.init()


def main(K, STAR_PROTECTIONS):

    game = Game(K, STAR_PROTECTIONS)
    game.menu1()


if __name__ == '__main__':
    K = int(sys.argv[1])
    START_PROTECTIONS = int(sys.argv[2])
    main(K, START_PROTECTIONS)
