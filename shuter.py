from pygame import *
from random import randint

main_weight = 700
main_height = 500
main = display.set_mode((main_weight, main_height))
display.set_caption("Шутер")
background = transform.scale(image.load("горы.png"), (main_weight, main_height))
sprite1 = transform.scale(image.load("пикачу.png"), (50, 50))
sprite2 = transform.scale(image.load("доги.png"), (50, 50))
monstric = transform.scale(image.load("монмтр тортик.png"), (50, 50))
machic = transform.scale(image.load("Мячик.png"), (50, 50))
asteroid = transform.scale(image.load("астероид.png"), (50, 50))

clock = time.Clock()

number = 0

mixer.init()
vistrel = mixer.Sound("vyistrel-pistoleta-36125.ogg")


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_weight, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_weight, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        main.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 10
        if keys[K_RIGHT] and self.rect.x < 645:
            self.rect.x += 10

    def fire(self):
        bullet = Bullet("Мячик.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Gamer(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= 10
        if keys[K_d] and self.rect.x < 645:
            self.rect.x += 10

    def ogon(self):
        bullet = Bullet("Мячик.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 5:
            self.kill()


lost = 0


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > main_height:
            self.rect.x = randint(80, main_weight - 80)
            self.rect.y = 0
            global lost
            lost += 1


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > main_height:
            self.rect.x = randint(80, main_weight - 80)
            self.rect.y = 0
            global number
            number += 1


font.init()
font1 = font.SysFont("Arial", 100)
font2 = font.SysFont("Arial", 35)


winner = font1.render("You WIN!", True, (0, 0, 255))
loser = font1.render("You LOSE!", True, (0, 0, 255))

mixer.init()
mixer.music.load("звуки дождя.ogg")
mixer.music.play()

player1 = Gamer("пикачу.png", 60, 445, 50, 50, 5)
player2 = Player("доги.png", 605, 445, 50, 50, 5)

monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
players1 = sprite.Group()
players1.add(player1)
players2 = sprite.Group()
players2.add(player2)

for i in range(5):
    monster = Enemy("монмтр тортик.png", randint(5, 625), -80, 50, 50, randint(1, 3))
    monsters.add(monster)

for i in range(2):
    vrag = Asteroid("астероид.png", randint(5, 625), -80, 50, 50, randint(1, 3))
    asteroids.add(vrag)

health = 3
gizn = 3
finish = False
game = True
while game:
    main.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_l:
                vistrel.play()
                player2.fire()
            if e.key == K_e:
                vistrel.play()
                player1.ogon()

    if not finish:
        if sprite.groupcollide(bullets, monsters, True, True):
            monster = Enemy("монмтр тортик.png", randint(5, 625), -80, 50, 50, randint(1, 3))
            monsters.add(monster)
            number += 1

        if sprite.groupcollide(players1, asteroids, False, True):
            vrag = Asteroid("астероид.png", randint(5, 625), -80, 50, 50, randint(1, 3))
            asteroids.add(vrag)
            health -= 1

        if sprite.groupcollide(players2, asteroids, False, True):
            vrag = Asteroid("астероид.png", randint(5, 625), -80, 50, 50, randint(1, 3))
            asteroids.add(vrag)
            gizn -= 1

        sprite_list = sprite.spritecollide(monster, monsters, False)

        players1.draw(main)
        players2.draw(main)
        monsters.draw(main)
        bullets.draw(main)
        asteroids.draw(main)

        players1.update()
        players2.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        chot = font2.render("Счёт врагов:" + str(lost) + str(" из 3"), True, (0, 0, 255))
        spisok = font2.render("Счёт пуль:" + str(number) + str(" из 15"), True, (0, 0, 255))
        pikachu = font2.render("Пикачу:" + str(health) + str(" жизней"), True, (0, 0, 255))
        dog = font2.render("Пёсик:" + str(gizn) + str(" жизней"), True, (0, 0, 255))

        main.blit(chot, (15, 15))
        main.blit(spisok, (15, 60))
        main.blit(pikachu, (495, 15))
        main.blit(dog, (495, 60))

        if number >= 15:
            finish = True
            main.blit(winner, (200, 200))

        if lost >= 3:
            finish = True
            main.blit(loser, (200, 200))

        if health <= 0:
            player1.kill()

        if gizn <= 0:
            player2.kill()

        if len(players1) and len(players2) == 0:
            main.blit(loser, (200, 200))

        display.update()
        clock.tick(60)
