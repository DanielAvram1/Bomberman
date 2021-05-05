import pygame

WIDTH, HEIGHT = 900, 600

HEADER_HEIGHT = 40
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Omu' cu bombe Avram Daniel")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (200, 200, 200)
LIME = (100, 255, 0)
ORANGE = (255,165,0)

FONT = pygame.font.Font('freesansbold.ttf', HEADER_HEIGHT//2)
FONT_LARGE = pygame.font.Font('freesansbold.ttf', HEADER_HEIGHT*2)
FONT_SMALL = pygame.font.Font('freesansbold.ttf', HEADER_HEIGHT//3)
ACTIVE = 'active'
INACTIVE = 'inactive'
EXPLODING = 'exploding'
EXPLOSION = 'explosion'
PREACTIVE = 'preactive'

MAX = 999999999999