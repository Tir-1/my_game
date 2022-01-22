import pygame

class Hero(pygame.sprite.Sprite):
    image = pygame.image.load("creature.png").convert_alpha()
    def __init__(self, group):
        super().__init__(group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.y = 301 // 2
        self.x = 301 // 2

    def create(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.x_pos, self.y_pos), 20)

    def coords(self, x, y):
        self.y = y
        self.x = x


    def move(self):
        if self.y != -1 and self.x != -1:
            if self.y_pos < self.y:
                self.y_pos += 1
            elif self.y_pos > self.y:
                self.y_pos -= 1
            if self.x_pos < self.x:
                self.x_pos += 1
            elif self.x_pos > self.x:
                self.x_pos -= 1
            self.create()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 301, 301
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    spisok = []
    object = Hero()
    sprites = pygame.sprite.Group()
    while running:
        #screen.fill((0, 0, 0))
        #object.create()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #Hero.draw()
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
