import pygame


def draw_info(text, sc):
    pygame.font.init()
    font2 = pygame.font.Font(None, 40)
    text = text.split(", ")
    text1 = font2.render(str(text[0]), True, (100, 255, 100))
    text2 = font2.render(str(text[1]), True, (100, 255, 100))
    text_x = 1000
    text_y = 800
    sc.blit(text1, (text_x, text_y))
    sc.blit(text2, (text_x, 900))


def draw_score(text, sc):
    pygame.font.init()
    font2 = pygame.font.Font(None, 50)
    text = font2.render(str(text), True, (100, 255, 100))
    text_x = 1300
    text_y = 420
    sc.blit(text, (text_x, text_y))


def draw_score2(text, sc):
    pygame.font.init()
    font3 = pygame.font.Font(None, 50)
    text = font3.render(str(text), True, (100, 255, 100))
    text_x = 1300
    text_y = 120
    sc.blit(text, (text_x, text_y))


class BackFon(pygame.sprite.Sprite):
    def __init__(self, group, name, scale, x, y):
        super().__init__(group)
        self.image = pygame.image.load("data/" + name)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
