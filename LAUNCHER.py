import pygame
import random

#window
FPS = 60
WIDTH = 900
HEIGHT = 600

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIME = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (25,255,0)
GRAY = (128, 128, 128)
VIOLET = (126, 8, 236)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREEN = (0,128,0)
CYAN = (0, 255, 255)
LIGHTGRAY = (211, 211, 211)
NAVY = (0, 0, 128)
MEDIUMSLATEBLUE = (123, 104, 238)
SKYBLUE = (0, 191, 255)
HONEYDEW = (240, 255, 240)
SNOW = (255, 250, 250)
IVORY = (255, 255, 240)
YELLOWGREEN = (154, 205, 50)
DARKGREEN = (0, 100, 0)
INDIGO = (75, 0, 130)

#player(platform) and objects
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platImg,(200,20))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2,HEIGHT-20)
    
    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speedx = -10
        if keys[pygame.K_d]:
            self.speedx = 10
        self.rect.x += self.speedx  

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0     

class Circle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(VIOLET)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.speedx = random.randint(-3,3)
        if self.speedx == 0:
            self.speedx = 2
        self.speedy = random.randint(3,7)

    def update(self):
        if self.rect.right > WIDTH:
            self.speedx = -self.speedx
            

        if self.rect.left < 0:
            self.speedx = -self.speedx
            

        if self.rect.top < 0:
            self.speedy = -self.speedy

        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((43,43))
        self.image.fill(DARKGREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SimplePong')
clock = pygame.time.Clock()

#textures and design
platImg = pygame.image.load('player.jpg').convert()
mainbg = pygame.image.load('mainBg.jpg').convert()
mainbg = pygame.transform.scale(mainbg,(WIDTH, HEIGHT))
mainbg_rect = mainbg.get_rect()

#objects
player = Platform()
circle = Circle()
sprites = pygame.sprite.Group()
circles = pygame.sprite.Group()
blocks = pygame.sprite.Group()
circles.add(circle)
sprites.add(player)
sprites.add(circle)

levels = [
    ['# # # # # # # # # # ',
     '## # # ### # # #    ']
]

level = 0
for i in range(20):
    for j in range(len(levels[level])):
        if levels[level][j][i] == '#':
            block = Block(i*45, j*45)
            sprites.add(block)
            blocks.add(block)

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    hits = pygame.sprite.spritecollide(player, circles, False)
    if hits:
        circle.speedy = -circle.speedy
    if circle.rect.y > HEIGHT:
        run = False

    window.blit(mainbg, mainbg_rect)
    sprites.draw(window)
    sprites.update()
    pygame.display.flip()

pygame.quit()
#280322 ALPHA