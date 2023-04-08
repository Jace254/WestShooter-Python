import pygame


class Sprite:
    def __init__(self, position, image, frames={"max": 1, "current": 0}, layers={"max": 1, "current": 0}):
        self.position = position
        self.image = image
        self.frames = frames
        self.layers = layers
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.width = self.image_width / self.frames["max"]
        self.height = self.image_height / self.layers["max"]
        self.center = {
            "x": self.position["x"] - self.width / 2,
            "y": self.position["y"] - self.height / 2,
        }
        self.x = self.frames["current"] * self.width
        self.y = self.layers["current"] * self.height
        self.image = self.image.subsurface(
            self.x, self.y, self.width, self.height)
        self.clock = pygame.time.Clock()
        self.refilled = False

    def draw(self, c):
        self.clock.tick(60)
        c.blit(
            self.image,
            (self.position["x"], self.position["y"])
        )

    def update(inputHandler=None, player=None, deltaTime=None, UIGroup=None, left=False, enemy=None):
        inputHandler.handleInput(player)

        # actions animation
        if not inputHandler.keys.up.pressed and not inputHandler.keys.down.pressed and not inputHandler.keys.left.pressed and not inputHandler.keys.right.pressed and not inputHandler.keys.shoot.pressed:
            if not player.alive:
                player.die()
            else:
                player.idle()
                player.fire = False
                player.shielded = False

        if not enemy.inputHandler.keys.shoot.pressed:
            player.damage = False

        if (inputHandler.keys.up.pressed == True and player.alive) or (inputHandler.keys.down.pressed == True and player.alive):
            player.moveUpDown(deltaTime)

        if (inputHandler.keys.left.pressed == True and player.alive) or (inputHandler.keys.right.pressed == True and player.alive):
            player.moveLeftRight(deltaTime)

        if inputHandler.keys.shoot.pressed and player.playerStats.bullets > 0 and player.alive:
            player.shoot(deltaTime)
            if player.fire == False:
                if player.playerStats.bullets > 0:
                    player.playerStats.bullets -= 1
                    if left:
                        UIGroup.bulletBar[player.playerStats.bullets].layers.current = 3
                    else:
                        UIGroup.bulletBar[player.playerStats.bullets].layers.current = 1

                if player.playerStats.bullets == 0 and player.playerStats.ammo > 0:
                    player.playerStats.bullets = 4
                    if left:
                        for b in UIGroup.bulletBar:
                            b.layers.current = 2
                    else:
                        for b in UIGroup.bulletBar:
                            b.layers.current = 0

                    player.playerStats.ammo -= 1
                    UIGroup.ammoBar[player.playerStats.ammo].layers.current = 2

                refilled = False
                player.shielded = False
                player.fire = True

        if enemy.damage == True:
            def refil():
                nonlocal refilled
                if not refilled:
                    player.playerStats.bullets += 1
                    if left:
                        UIGroup.bulletBar[player.playerStats.bullets -
                                          1].layers.current = 2
                    else:
                        UIGroup.bulletBar[player.playerStats.bullets -
                                          1].layers.current = 0

                    refilled = True
            Timer(0.35, refil).start()

        if inputHandler.keys.shield.pressed and not inputHandler.keys.up.pressed and not inputHandler.keys.down.pressed and not inputHandler.keys.left.pressed and not inputHandler.keys.right.pressed and not inputHandler.keys.shoot.pressed and player.alive:
            player.shield(deltaTime)
            player.shielded = True

        if enemy.inputHandler.keys.shoot.pressed and player.alive and enemy.playerSprite.position.y == player.playerSprite.position.y and not player.shielded and enemy.playerStats.bullets > 0 and enemy.alive:
            player.takeDamage(
                deltaTime, enemy.inputHandler.keys.shoot.pressed)
            if player.damage == False:
                if player.playerStats.life > 0:
                    player.playerStats.life -= 1
                    UIGroup.lifeBar[player.playerStats.life].layers.current = 2

                if player.playerStats.life == 0:
                    player.alive = False

                player.damage = True


class Target:
    def __init__(self, sprite, player):
        self.player = player
        self.sprite = sprite
        self.up = False
        self.left = False
        self.down = False
        self.right = False

    def checkTarget(self):
        if (
            self.sprite.position["y"] + self.sprite.height / 8 <
            self.player.position["y"] + self.player.height / 2
        ):
            self.up = True
        if (
            self.sprite.position["x"] + self.sprite.width / 2 >
            self.player.position["x"] + self.player.width / 2
        ):
            self.right = True
        if (
            self.sprite.position["y"] + self.sprite.height / 8 >
            self.player.position["y"] + self.player.height / 2
        ):
            self.down = True
        if (
            self.sprite.position["x"] + self.sprite.width / 2 <
            self.player.position["x"] + self.player.width / 2
        ):
            self.left = True

    def resetTarget(self):
        self.up = False
        self.left = False
        self.down = False
        self.right = False


class InputHandler:
    def __init__(self, player_sprite, targets, left):
        self.player = player_sprite
        self.targets = targets
        self.left = left
        self.keys = {
            "up": {
                "pressed": False,
                "lastKey": False
            },
            "left": {
                "pressed": False,
                "lastKey": False
            },
            "down": {
                "pressed": False,
                "lastKey": False
            },
            "right": {
                "pressed": False,
                "lastKey": False
            },
            "shoot": {
                "pressed": False
            },
            "shield": {
                "pressed": False
            }
        }

    def handleInput(self, player):
        def keydown_handler(e):
            if self.left:
                if e.key == "w" or e.key == "W":
                    self.keys["up"]["pressed"] = True
                elif e.key == "a" or e.key == "A":
                    self.keys["left"]["pressed"] = True
                elif e.key == "s" or e.key == "S":
                    self.keys["down"]["pressed"] = True
                elif e.key == "d" or e.key == "D":
                    self.keys["right"]["pressed"] = True
                elif e.key == " ":
                    self.keys["shoot"]["pressed"] = True
                elif e.key == "b" or e.key == "B":
                    self.keys["shield"]["pressed"] = True
            else:
                if e.key == "ArrowUp":
                    self.keys["up"]["pressed"] = True
                elif e.key == "ArrowLeft":
                    self.keys["left"]["pressed"] = True
                elif e.key == "ArrowDown":
                    self.keys["down"]["pressed"] = True
                elif e.key == "ArrowRight":
                    self.keys["right"]["pressed"] = True
                elif e.key == "Enter":
                    self.keys["shoot"]["pressed"] = True
                elif e.key == "m" or e.key == "M":
                    self.keys["shield"]["pressed"] = True

        def keyup_handler(e):
            if self.left:
                if e.key == "w" or e.key == "W":
                    self.keys["up"]["pressed"] = False
                    self.keys["up"]["lastKey"] = False
                elif e.key == "a" or e.key == "A":
                    self.keys["left"]["pressed"] = False
                    self.keys["left"]["lastKey"] = False
                elif e.key == "s" or e.key == "S":
                    self.keys["down"]["pressed"] = False
                    self.keys["down"]["lastKey"] = False
                elif e.key == "d" or e.key == "D":
                    self.keys["right"]["pressed"] = False
                    self.keys["right"]["lastKey"] = False
                elif e.key == " ":
                    self.keys["shoot"]["pressed"] = False
                elif e.key == "b" or e.key == "B":
                    self.keys["shield"]["pressed"] = False
            else:
                if e.key == "ArrowUp":
                    self.keys["up"]["pressed"] = False
                    self.keys["up"]["lastKey"] = False
                elif e.key == "ArrowLeft":
                    self.keys["left"]["pressed"] = False
                    self.keys["left"]["lastKey"] = False
                elif e.key == "ArrowDown":
                    self.keys["down"]["pressed"] = False
                    self.keys["down"]["lastKey"] = False
