import pyxel


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.speed = 2
        self.tilemap_coord = [0, 0]

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.tilemap_coord[0], self.tilemap_coord[1], self.w, self.h, 0)


class App:
    def __init__(self):
        pyxel.init(256, 256, title='Hello Pyxel')
        pyxel.load('1.pyxres')
        self.ship = Ship(128, 128)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.ship.update()

    def draw(self):
        pyxel.cls(5)

        self.ship.draw()
        #pyxel.blt(16, 16, 0, 0, 0, 16, 16, 0)

if __name__ == '__main__':
    App()


    print("testes")