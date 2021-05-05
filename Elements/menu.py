
from .constants import *
import pygame

class Menu:

    '''
    clasa care incapsuleaza informatia despre un meniu al jocului
    '''

    def __init__(self, sections, header):
        self.sections = sections
        self.header = header


    def draw(self):
        '''
        functia care afiseaza meniul
        :return:
        '''
        WIN.fill(WHITE)
        self.header.draw()
        for section in self.sections:
            section.draw()
        pygame.display.update()


class Section:
    '''
    clasa care incapsuleaza informatiile unei sectiuni din meniu
    '''
    width = 280
    vertical_padding = 5
    horizontal_padding = 10

    def __init__(self, title, buttons, x, y):
        self.title = title
        self.buttons = buttons
        self.x = x
        self.y = y

    def draw(self):
        '''
        functia care afiseaza o sectiune in parte
        '''
        text = FONT.render(self.title, True, BLACK, WHITE)
        rect = text.get_rect()
        rect.x = self.x + (self.width - rect.width - self.horizontal_padding) // 2
        rect.y = self.y + self.horizontal_padding + 30
        WIN.blit(text, rect)
        x = self.x + self.horizontal_padding
        for i in range(len(self.buttons)):
            button = self.buttons[i]
            y = self.y + (i + 1) * button.height + i * self.vertical_padding
            button.draw(x, y)


class Button:
    '''
    clasa care incapsuleaza toate informatiile legate de un buton
    '''
    highlighted = False
    width = 260
    height = 90

    def __init__(self, text, on_choose, bg_color = LIGHT_GRAY, type="big"):
        self.text = text
        self.on_choose = on_choose
        self.bg_color = bg_color
        self.x = self.y = 0
        self.type = type

    def draw(self, x, y):
        self.x = x
        self.y = y
        if self.highlighted:
            bg_color = YELLOW
        else:
            bg_color = self.bg_color

        text = FONT.render(self.text, True, BLACK, bg_color)
        if self.type == 'small':
            text = FONT_SMALL.render(self.text, True, WHITE, bg_color)
            self.width //= 2
            self.height //= 2

        text_horizontal_padding = (self.width - text.get_width()) // 2
        text_vertical_padding = (self.height - text.get_height()) // 2
        rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(WIN, bg_color, rect)
        WIN.blit(text, (x + text_horizontal_padding, y + text_vertical_padding))

    def covers(self, ver_x, ver_y):
        '''
        functie care verifica daca o pereche de coordonate acopera sau nu un buton
        :rtype: bool
        '''
        return (self.x < ver_x < self.x + self.width) and (self.y < ver_y < self.y + self.height)



class Header:
    '''
    clasa care incapsuleaza informatiile ce tin de headerul unui meniu
    '''
    height = 100

    def draw(self):
        text = FONT_LARGE.render('BOMBERMAN', True, BLACK, WHITE)
        rect = text.get_rect()
        rect.x = (WIDTH - rect.width) // 2
        WIN.blit(text, rect)