import pyxel

FPS = 60
WIDTH = 256
HEIGHT = 256
BOTTOM = 20

COLOR_KEY = 5
BG_COLOR = 1
FOOTER_COLOR = 12

EXPLOSION_ANIMATION = [(16, 104), (32, 104), (48, 104), (0, 120), (16, 120)]

GAME_STATE = {'START_SCREEN': 0, 'GAME': 1, 'GAME_OVER': 2, 'PAUSE': 3}


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.speed = 2
        self.vie = 3
        self.tilemap_coord = [0, 8]
        self.tier = 1

    def check_screen_collision(self):
        if self.x < 0:
            self.x = 0
        if self.x > pyxel.width - self.w:
            self.x = pyxel.width - self.w
        if self.y < 0:
            self.y = 0
        if self.y > pyxel.height - self.h - BOTTOM:
            self.y = pyxel.height - self.h - BOTTOM

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
        for i in range(self.vie):
            pyxel.blt(10 + (i * 8), 243, 0, 40, 80, 8, 8, 5)

    def upgrade(self):
        if self.tier < 4:
            self.tilemap_coord[0] += 16
            self.tier += 1


class Projectiles:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.speed = 4
        self.tilemap_coord = [0, 104]
        self.frame = 0
        self.disable = False

    def update(self):
        if not self.disable:
            self.y -= self.speed

    def draw(self):
        if not self.disable:
            pyxel.blt(self.x, self.y, 0, self.tilemap_coord[0], self.tilemap_coord[1], self.w, self.h, COLOR_KEY)
        else:
            pyxel.blt(self.x, self.y, 0, EXPLOSION_ANIMATION[self.frame][0], EXPLOSION_ANIMATION[self.frame][1], self.w,
                      self.h, COLOR_KEY)


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
            self.x += pyxel.sin(self.frame * 10) * 0.5
            self.y += self.speed
            if self.y > pyxel.height - self.h - BOTTOM:
                self.y = 0
                # self.disable = True

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.tilemap_coord[0], self.tilemap_coord[1], self.w, self.h, COLOR_KEY)


class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        self.speed = 1
        self.tilemap_coord = [0, 72]

    def update(self):
        self.y += self.speed

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.tilemap_coord[0], self.tilemap_coord[1], self.w, self.h, COLOR_KEY)


class PowerUp(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tilemap_coord = [48, 80]


class Heal(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tilemap_coord = [40, 80]


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, fps=FPS, title='Hello Pyxel')
        pyxel.load('1.pyxres')
        self.ship = Ship(120, 120)
        self.projectiles = []
        self.reload = 0
        self.items = []
        self.current_round = 0
        self.enemies = []
        self.score = 0

        pyxel.run(self.update, self.draw)

    def spawn_item(self, x, y):
        if pyxel.rndi(0, FPS * 10) == 1:
            if pyxel.rndi(0, 2) == 0:
                self.items.append(PowerUp(x, y))
            else:
                self.items.append(Heal(x, y))

    def enemy_collision(self):
        for enemy in self.enemies:
            # Check collision with player
            if (self.ship.x < enemy.x + enemy.w and
                    self.ship.x + self.ship.w > enemy.x and
                    self.ship.y < enemy.y + enemy.h and
                    self.ship.y + self.ship.h > enemy.y):
                self.ship.vie -= 1
                self.enemies.remove(enemy)

            # Check collision with projectiles
            for projectile in self.projectiles:
                if (projectile.x < enemy.x + enemy.w and
                        projectile.x + projectile.w > enemy.x and
                        projectile.y < enemy.y + enemy.h and
                        projectile.y + projectile.h > enemy.y):
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                        projectile.disable = True
                        self.score += FPS * 5
                        self.spawn_item(projectile.x, projectile.y)

    def enemy_spawn(self):
        for i in range(self.current_round * 10):
            coord = (pyxel.rndi(0, pyxel.width), pyxel.rndi(0, -pyxel.height))
            self.enemies.append(Enemy(coord[0], coord[1], pyxel.rndi(0, 7)))

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.ship.tier == 1:
            if pyxel.btnp(pyxel.KEY_SPACE, 0, 10) and self.reload < 0:
                self.projectiles.append(Projectiles(self.ship.x, self.ship.y - 15))
                self.reload = 7
        if self.ship.tier == 2:
            if pyxel.btnp(pyxel.KEY_SPACE, 0, 5) and self.reload < 0:
                self.projectiles.append(Projectiles(self.ship.x, self.ship.y - 15))
                self.reload = 4
        if self.ship.tier == 3:
            if pyxel.btnp(pyxel.KEY_SPACE, 0, 10) and self.reload < 0:
                self.projectiles.append(Projectiles(self.ship.x - 6, self.ship.y - 15))
                self.projectiles.append(Projectiles(self.ship.x + 6, self.ship.y - 15))
                self.reload = 7
        if self.ship.tier == 4:
            if pyxel.btnp(pyxel.KEY_SPACE, 0, 5) and self.reload < 0:
                self.projectiles.append(Projectiles(self.ship.x - 6, self.ship.y - 15))
                self.projectiles.append(Projectiles(self.ship.x + 6, self.ship.y - 15))
                self.reload = 4
        self.reload -= 1

        if self.projectiles:
            for projectile in self.projectiles:
                projectile.update()
                if projectile.y + projectile.h < 0:
                    self.projectiles.remove(projectile)

                if projectile.disable:
                    projectile.frame += 1
                    if projectile.frame >= len(EXPLOSION_ANIMATION):
                        self.projectiles.remove(projectile)

        for enemy in self.enemies:
            enemy.update()

        if self.ship.vie == 0:
            pyxel.quit()

        self.enemy_collision()

        if pyxel.btnp(pyxel.KEY_R):
            self.items.append(PowerUp(50, 50))

        if self.items:
            for i in self.items:
                i.update()
                if i.y > pyxel.height - BOTTOM:
                    self.items.remove(i)

        for i in self.items:
            if i.x < self.ship.x + self.ship.w and i.x + i.w > self.ship.x and i.y < self.ship.y + self.ship.h and i.y + i.h > self.ship.y:
                self.ship.upgrade()
                self.items.remove(i)

        if not self.enemies:
            self.current_round += 1
            self.enemy_spawn()

        self.ship.update()

    def draw(self):
        pyxel.cls(BG_COLOR)
        pyxel.rect(0, pyxel.height - BOTTOM, pyxel.width, pyxel.height, FOOTER_COLOR)

        for enemy in self.enemies:
            enemy.draw()
        self.ship.draw()

        for projectile in self.projectiles:
            projectile.draw()

        for i in self.items:
            i.draw()

        pyxel.text(WIDTH - 60, HEIGHT - BOTTOM * 0.6, 'Score: ' + str(self.score), 7)


if __name__ == '__main__':
    App()
