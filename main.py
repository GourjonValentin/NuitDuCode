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
        self.vie = 3
        self.tilemap_coord = [0, 0]

    def check_screen_collision(self):
        if self.x < 0:
            self.x = 0
        if self.x > pyxel.width - self.w:
            self.x = pyxel.width - self.w
        if self.y < 0:
            self.y = 0
        if self.y > pyxel.height - self.h - 20:
            self.y = pyxel.height - self.h - 20

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
        pyxel.blt(self.x, self.y, 0, self.tilemap_coord[0], self.tilemap_coord[1], self.w, self.h, 5)
        for i in range(self.vie):
            pyxel.blt(10 + (i * 8), 243, 0, 40, 80, 8, 8, 5)


class Projectiles:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.speed = 4
        self.tilemap_coord = [0, 104]

    def update(self):
        self.y -= self.speed

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.tilemap_coord[0], self.tilemap_coord[1], self.w, self.h, 5)


class App:
    def __init__(self):
        pyxel.init(256, 256, title='Hello Pyxel', fps=60)
        pyxel.load('1.pyxres')
        self.ship = Ship(120, 120)
        self.projectiles = []
        self.ship = Ship(128, 128)
        self.reload = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_SPACE) and self.reload < 0:
            self.projectiles.append(Projectiles(self.ship.x, self.ship.y))
            self.reload = 20
        self.reload -= 1

        if self.projectiles:
            for projectile in self.projectiles:
                projectile.update()
                if projectile.y < 0:
                    self.projectiles.remove(projectile)

        self.ship.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, pyxel.height - BOTTOM, pyxel.width, pyxel.height, FOOTER_COLOR)
        self.ship.draw()

        for projectile in self.projectiles:
            projectile.draw()


if __name__ == '__main__':
    App()
