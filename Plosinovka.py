import sys
from sys import exit
from sys import path
sys.path.append("D:\Python\Lib\site-packages")
print(sys.path)
from random import randint

import pygame

pygame.init()
pygame.mixer.init()

RYCHLOST = 2
CETNOST = 220
JUMP = -25

cas = 0
gravity = 0
score = 0
naraz = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pict1 = pygame.image.load("Grafika/Panacek1.png")
        pict2 = pygame.image.load("Grafika/Panacek2.png")
        pict3s = pygame.image.load("Grafika/Panacek3.png")
        self.picture_index = 0
        self.pictures = (pict1, pict2, pict3s)
        self.image = self.pictures[self.picture_index]
        self.rect = self.image.get_rect(midbottom=(50, 580))
        self.gravitace = 0

    def player_input(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.rect.bottom == 580:
            self.gravitace = JUMP
            SKOK_SOUND.play()
            pygame.event.post(pygame.event.Event(score_plus))

    def player_skok(self):
        self.rect.bottom += self.gravitace
        self.gravitace += 1
        if self.rect.bottom >= 580:
            self.rect.bottom = 580
            self.gravitace = 0


    def animate_player (self):
        if self.rect.bottom < 580:
            self.picture_index = 2
        else:
            self.picture_index += 0.1
            if self.picture_index >= len(self.pictures): self.picture_index = 0
        self.image = self.pictures[int(self.picture_index)]

    def update(self):
        self.player_input()
        self.player_skok()
        self.animate_player()

class Monster(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        ptak_image1 = pygame.transform.rotozoom(pygame.image.load("Grafika/Ptak1.png"),0 , 0.4).convert_alpha()
        ptak_image2 = pygame.transform.rotozoom(pygame.image.load("Grafika/Ptak2.png"),0 , 0.4).convert_alpha()
        ptak_image3 = pygame.transform.rotozoom(pygame.image.load("Grafika/Ptak3.png"),0 , 0.4).convert_alpha()
        morbo_image1 = pygame.transform.rotozoom(pygame.image.load("Grafika/Monster1.png"),0 , 0.8).convert_alpha()
        morbo_image2 = pygame.transform.rotozoom(pygame.image.load("Grafika/Monster2.png"),0 , 0.8).convert_alpha()
        morbo_image3 = pygame.transform.rotozoom(pygame.image.load("Grafika/Monster3.png"),0 , 0.8).convert_alpha()
        morbo_image4 = pygame.transform.rotozoom(pygame.image.load("Grafika/Monster4.png"),0 , 0.8).convert_alpha()
        self.index = 0

        # ptak
        if type == 0:
            self.pictures = [ptak_image1, ptak_image2, ptak_image3]
            self.image = self.pictures[self.index]
            self.rect = self.image.get_rect(bottomleft=(randint(1200,1400), randint(300,450)))
        # morbo
        else:
            self.pictures = [morbo_image1, morbo_image2, morbo_image3, morbo_image4]
            self.image = self.pictures[self.index]
            self.rect = self.image.get_rect(bottomleft=(randint(1200,1400), 580))

    def animate(self):
        self.index += 0.1
        if self.index >= len(self.pictures): self.index = 0
        self.image = self.pictures[int(self.index)]

    def pohyb(self):
        self.rect.x -= RYCHLOST * 3
        if self.rect.x < -150: self.kill()

    def update(self):
        self.animate()
        self.pohyb()

def kolize(naraz):
    if pygame.sprite.spritecollide(player.sprite, monsters, False):
        if naraz == True: SRAZKA_SOUND.play()
        return False
    else:
        return True

player = pygame.sprite.GroupSingle()
player.add(Player())
monsters = pygame.sprite.Group()

screen = pygame.display.set_mode((1200, 600))

test_font = pygame.font.Font(None, 50)

dno_surf = pygame.Surface((1200, 20))
dno_surf.fill("Brown")

pozadi_surf = pygame.image.load("Grafika/Landscape-hory.png").convert_alpha()

les_surf = pygame.image.load("Grafika/Landscape-les.png").convert_alpha()

konec_surf = test_font.render("zmáčkni 'r' a začni znovu", True, (30, 100, 20))

SKOK_SOUND = pygame.mixer.Sound("MP3/Silencer.mp3")
SRAZKA_SOUND = pygame.mixer.Sound("MP3/Granat.mp3")

score_plus = pygame.USEREVENT +1
spawn = pygame.USEREVENT +2

while True:

    if pygame.key.get_pressed()[pygame.K_r] and kolize(naraz) == False:
        monsters.empty()
        cas = 0
        score = 0
        naraz = True

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    # počítání score
        if event.type == score_plus:
                score += 1
    # rození monster
        if event.type == spawn:
                monsters.add(Monster(randint(0, 1)))

    if kolize(naraz):

    # blit
        score_surf = test_font.render(f'Score: {score}', False, (30, 100, 20))
        score_rect = score_surf.get_rect(center = (200,70))

        screen.blit(pozadi_surf, (0, 0))
        screen.blit(les_surf, (cas % 1200 - 1200, 400))
        screen.blit(dno_surf, (0, 580))
        screen.blit(score_surf,score_rect)

        player.draw(screen)
        player.update()

        monsters.draw(screen)
        monsters.update()

        clock = pygame.time.Clock()

        pygame.event.pump()

    # zrychlování hry a čas
        cas -= RYCHLOST
        if cas > -1500:
            clock.tick(40)
            CETNOST = 240
        elif cas > -3500:
            clock.tick(60)
            CETNOST = 200
        elif cas > -6000:
            clock.tick(80)
            CETNOST = 170
        elif cas > -8000:
            clock.tick(100)
            CETNOST = 140
        else:
            clock.tick(130)
            CETNOST = 125

        if cas % CETNOST == 0:
            pygame.event.post(pygame.event.Event(spawn))
        pygame.display.update()
    else:
        naraz = False
        screen.fill("red")
        screen.blit(score_surf,(400, 300))
        screen.blit(konec_surf, (400, 350))
        pygame.display.update()
