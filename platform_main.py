import pygame
import math
from pygame import *
from entities import *
# 25 by 25
WIDTH = 800
HEIGHT = 800
# display in width, height
DISPLAY = (WIDTH, HEIGHT)
# number of bits to use for color
DEPTH = 32
# passing 0 for the flags inits the display with the default options
FLAGS = 0
SURFACE_WIDTH = 32
SURFACE_HEIGHT = 32
BG_SURFACE_WH = (SURFACE_WIDTH, SURFACE_HEIGHT)
TIMER_TICK = 30


def main():
    pygame.init()
    screen = display.set_mode(DISPLAY, FLAGS, DEPTH)
    display.set_caption("Blokido Tower v.0.3")
    timer = time.Clock()
    up = down = left = right = False
    bg = Surface(BG_SURFACE_WH)
    # call convert with no args
    # this is the fastest format for blitting
    bg.convert()
    bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    platforms = []

    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPP",
        "PB P                    P",
        "P  P                    P"
        "P  P                    P",
        "P  PP  PPPPPPPP         P",
        "P  P    PP P  P         P",
        "P  P    P PPP P         P",
        "P  P    P PDP P         P",
        "P  P    P PDP P         P",
        "P  P    P PDP P         P",
        "P  P    P PPP P         P",
        "P  P    P  P PP         P",
        "P  P    P  P  P         P",
        "P  P    P  P  P         P",
        "P  P    P  P  P         P",
        "P  P    P  P  PD        P",
        "P  PP  PPPPPPPPPDDDDDDD P",
        "P  P    P               P",
        "P  P    P     P         P",
        "P  P    P     P         P",
        "P  P    P     P         P",
        "P  P    P     P         P",
        "P  P    P     P         P",
        "P       P     P         P",
        "P       PE    P         P",
        "PPPPPPPPPPPPPPP         P"]
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y, SURFACE_WIDTH, SURFACE_HEIGHT)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y, SURFACE_WIDTH, SURFACE_HEIGHT)
                platforms.append(e)
                entities.add(e)
            if col == "B":
                b = Player(x, y, SURFACE_WIDTH, SURFACE_HEIGHT)
                entities.add(b)
            if col == "D":
                d = DeathBlock(x, y, SURFACE_WIDTH, SURFACE_HEIGHT)
                platforms.append(d)
                entities.add(d)
            x += 32
        y += 32
        x = 0

    up = down = left = right = False
    # game loop
    while 1:
        timer.tick(TIMER_TICK)

        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit, "ESCAPE"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False

        # draw background
        for y in range(HEIGHT / SURFACE_HEIGHT):
            for x in range(WIDTH / SURFACE_WIDTH):
                screen.blit(bg, (x * SURFACE_WIDTH, y * SURFACE_HEIGHT))

        # update player, draw everything else
        b.update(up, down, left, right, platforms)
        entities.draw(screen)
        pygame.display.flip()


class Player(Entity):
    def __init__(self, x, y, width, height):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.hitSides = False
        self.onGround = False
        self.stamina = 32
        self.image = Surface((width, height))
        self.image.convert()
        self.image.fill(Color("#0000E6"))
        self.rect = Rect(x, y, width, height)

    def update(self, up, down, left, right, platforms):
        if up:
            if self.stamina > 0:
                # only jump if on the ground or sides of block
                if self.onGround:
                    self.yvel -= 12
                if self.hitSides:
                    self.yvel = -10
                    self.stamina -= 1
                    up = False
            else:
                pass
        if not up and self.hitSides:
            self.hitSides = False

        if down:
            pass
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.5
            # max falling speed
            if self.yvel > 30:
                self.yvel = 30

        if not (left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)

        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    event.post(event.Event(QUIT))
                if isinstance(p, DeathBlock):
                   event.post(event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.hitSides = True
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.hitSides = True
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                    self.stamina = 10
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0


if __name__ == "__main__":
    main()
