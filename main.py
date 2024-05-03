import pyxel

WIDTH = 256
HEIGHT = 256
BOTTOM = 20

COLOR_KEY = 5
BG_COLOR = 1
FOOTER_COLOR = 12


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.speed = 2
        self.tilemap_coord = [0, 8]

    def check_screen_collision(self):
        if self.x < 0:
            self.x = 0
        if self.x > pyxel.width - self.w:
            self.x = pyxel.width - self.w
        if self.y < 0:
            self.y = 0
        if self.y > pyxel.height - self.h:
            self.y = pyxel.height - self.h

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed

        self.check_screen_collision()

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.tilemap_coord[0], self.tilemap_coord[1], self.w, self.h, COLOR_KEY)


class Enemy:
    def __init__(self, x=0, y=0, e_type=0):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.speed = 1
        self.enemy_type = e_type
        self.tilemap_coord = [16 * (self.enemy_type % 4), 16 * (self.enemy_type // 4) + 40]
        self.disable = False
        self.frame = 0

    def update(self):
        if not self.disable:
            self.frame = self.frame + 1
            self.x += pyxel.sin(self.frame *10) * 0.5
            self.y += self.speed
            if self.y > pyxel.height - BOTTOM:
                self.y = 0
                #self.disable = True

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.tilemap_coord[0], self.tilemap_coord[1], self.w, self.h, COLOR_KEY)


class App:
    def __init__(self):
        pyxel.init(256, 256, fps=60, title='Hello Pyxel')
        pyxel.load('1.pyxres')
        self.ship = Ship(120, 120)
        self.enemies = [Enemy(0, 0, 0), Enemy(0, 16, 1), Enemy(0, 32, 2)]

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.ship.update()

    def draw(self):
        pyxel.cls(0)
        for enemy in self.enemies:
            enemy.update()
            enemy.draw()
        self.ship.draw()


if __name__ == '__main__':
    App()
