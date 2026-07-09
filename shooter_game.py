# The game code (can be modified)

from pygame import *
from random import randint


# initialize mixer for sounds/music
mixer.init()

# background music
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)   # lower background music volume
mixer.music.play()

# sound effect for firing
fire_sound = mixer.Sound('laser.mp3')
fire_sound.set_volume(0.1)


# initialize fonts
font.init()

# large font for win/lose messages
font1 = font.SysFont('Arial', 80)

# win and lose text
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

# smaller font for score and missed enemies
font2 = font.SysFont('Arial', 36)
#Lifes font (NOT READY)

# images used in the game
img_back = "galaxy.jpg"     # game background
img_hero = "rocket.png"     # player spaceship
img_enemy = "ufo.png"       # enemy spaceship
img_bullet = "bullet.png"   # bullet image
img_asteroid = 'asteroid.png'

# game variables
score = 0       # enemies destroyed
goal = 50       # enemies needed to win
lost = 0        # enemies missed
max_lost = 5    # player loses if this many enemies are missed
life = 3        # players life
life_str = str(life)
Life_font = font.SysFont('Arial', 40)
life_Text = Life_font.render(str(life) , True, (180, 0, 0))
# parent class for all sprites
class GameSprite(sprite.Sprite):

    # class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):

        # call the Sprite constructor
        sprite.Sprite.__init__(self)

        # load and scale the sprite image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        # sprite movement speed
        self.speed = player_speed

        # create a rectangle around the sprite
        self.rect = self.image.get_rect()

        # set the sprite position
        self.rect.x = player_x
        self.rect.y = player_y

    # draw the sprite on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# main player class
class Player(GameSprite):

    # move the player with arrow keys
    def update(self):
        keys = key.get_pressed()

        # move left, but do not leave the window
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        # move right, but do not leave the window
        if keys[K_RIGHT] and self.rect.x < win_width - 100:
            self.rect.x += self.speed

    # create a bullet at the player's position
    def fire(self):
        bullet = Bullet(
            img_bullet,
            self.rect.centerx,
            self.rect.top,
            15,
            20,
            -15
        )
        bullets.add(bullet)
    def fire2(self):
        asteroid = Asteroid(
            img_asteroid,
            self.rect.centerx,
            self.rect.top,
            15,
            20,
            -15
        )
        bullets.add(asteroid)

# enemy sprite class
class Enemy(GameSprite):

    # enemy movement
    def update(self):
        self.rect.y += self.speed

        global lost

        # if enemy reaches the bottom, move it back to the top
        if self.rect.y > win_height:
            self.rect.x = randint(100, win_width - 100)
            self.rect.y = -40
            lost += 1
            self.speed = randint(1, 3)  # randomize speed for next appearance


# bullet sprite class
class Bullet(GameSprite):

    # bullet movement
    def update(self):
        self.rect.y += self.speed

        # if bullet leaves the screen, remove it
        if self.rect.y < 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed

        global lost

        # if enemy reaches the bottom, move it back to the top
        if self.rect.y > win_height:
            self.rect.x = randint(100, win_width - 100)
            self.rect.y = -40
            self.speed = randint(1, 3)  # randomize speed for next appearance


# function to create enemies
def create_monsters():
    for i in range(1, 6):
        monster = Enemy(
            img_enemy,
            randint(80, win_width - 80),
            -40,
            80,
            50,
            randint(1, 3)
        )
        monsters.add(monster)
def create_asteroids():
    for i in range(1, 3):
        asteroid = Asteroid(
            img_asteroid,
            randint(80, win_width - 80),
            -40,
            80,
            50,
            randint(1, 3)
        )
        asteroids.add(asteroid) 


# create a window
win_width = 1050
win_height = 750

display.set_caption("Space Shooter Game")
window = display.set_mode((win_width, win_height))

# load and resize the background
background = transform.scale(image.load(img_back), (win_width, win_height))


# create the player sprite
ship = Player(img_hero, 5, win_height - 100, 80, 100, 15)


# create enemy group
monsters = sprite.Group()
create_monsters()
asteroids = sprite.Group()
create_asteroids()

# create bullet group
bullets = sprite.Group()


# if finish is True, the game stops updating
finish = False

# stores the time when the game ended
restart_time = 0


# main game loop flag
run = True


# create clock object
clock = time.Clock()

# frames per second
FPS = 60


while run:

    # check events
    for e in event.get():

        # close the game window
        if e.type == QUIT:
            run = False

        # shoot when SPACE is pressed
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                fire_sound.play()
                ship.fire()

    # if game is not finished
    if not finish:

        # draw background
        window.blit(background, (0, 0))

        # update sprite positions
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        # draw sprites
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        # check collision between bullets and enemies
        collides = sprite.groupcollide(monsters, bullets, True, True)

        # for every enemy hit, increase score and create a new enemy
        for c in collides:
            score += 1

            monster = Enemy(
                img_enemy,
                randint(80, win_width - 80),
                -40,
                80,
                50,
                randint(1, 3)
            )
            monsters.add(monster)
            asteroid = Asteroid(
                img_asteroid,
                randint(80, win_width - 80),
                -40,
                80,
                50,
                randint(1, 3)
            )
            asteroids.add(asteroid)

        # check if player collides with an enemy or asteroid
        hit_monster = sprite.spritecollide(ship, monsters, True)
        hit_asteroid = sprite.spritecollide(ship, asteroids, True)

        if hit_monster or hit_asteroid or lost >= max_lost:
            life -= 1
            restart_time = time.get_ticks()

            if life <= 0:
                finish = True
                window.blit(lose, (350, 330))

        # check if player wins
        if score >= goal:
            finish = True
            restart_time = time.get_ticks()
            window.blit(win, (350, 330))
        # show score
        text = font2.render("Score: " + str(score), True, (255, 255, 255))
        window.blit(text, (10, 20))

        # show missed enemies
        text_missed = font2.render("Missed: " + str(lost), True, (255, 255, 255))
        window.blit(text_missed, (10, 50))
        #Show player lifes
        text_life = Life_font.render("Lifes: " + str(life), True, (180, 0, 0))
        window.blit(text_life, (170, 50))
        # update the display
        display.update()

    # if game is finished, restart after 3 seconds
    else:

        # current time
        current_time = time.get_ticks()

        # wait 3000 milliseconds before restarting
        if current_time - restart_time >= 3000:

            # reset game variables
            finish = False
            score = 0
            lost = 0
            life = 3

            # remove all bullets
            for b in bullets:
                b.kill()

            # remove all enemies
            for m in monsters:
                m.kill()

            # create enemies again
            create_monsters()

            # reset player position
            ship.rect.x = 5
            ship.rect.y = win_height - 100

    # control the game speed
    clock.tick(FPS)
