import pyxel


class App:
    def __init__(self):
        pyxel.init(256, 256, title='Hello Pyxel')
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        pyxel.text(55, 41, 'Hello, Pyxel!', 7)


App()
