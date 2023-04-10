import pygame
import threading

# to be visited
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
        self.refilled = False

    def draw(self, c):
        try:
            c.blit(
                self.image.subsurface(
                    self.frames["current"] * self.width, self.layers["current"] * self.height, self.width, self.height),
                (self.position["x"], self.position["y"])
            )
        except:
            print('failed to draw')

    def update(self, input_handler=None, player=None, deltaTime=None, UIGroup=None, left=False, enemy=None):
        try:
            input_handler.handleInput(player)
            # actions animation
            if not input_handler.keys["up"]["pressed"] and not input_handler.keys["down"]["pressed"] and not input_handler.keys["left"]["pressed"] and not input_handler.keys["right"]["pressed"] and not input_handler.keys["shoot"]["pressed"]:
                if not player.alive:
                    player.die()
                else:
                    player.idle()
                    player.fire = False
                    player.shielded = False

            if not enemy.input_handler.keys["shoot"]["pressed"]:
                player.damage = False

            if (input_handler.keys["up"]["pressed"] == True and player.alive) or (input_handler.keys["down"]["pressed"] == True and player.alive):
                player.move_up_down(deltaTime)

            if (input_handler.keys["left"]["pressed"] == True and player.alive) or (input_handler.keys["right"]["pressed"] == True and player.alive):
                player.move_left_right(deltaTime)

            if input_handler.keys["shoot"]["pressed"] and player.player_stats["bullets"] > 0 and player.alive:
                player.shoot(deltaTime)
                if player.fire == False:
                    if player.player_stats["bullets"] > 0:
                        player.player_stats["bullets"] -= 1
                        if left:
                            UIGroup["bulletBar"][player.player_stats["bullets"]
                                                 ].layers["current"] = 3
                        elif not left:
                            UIGroup["bulletBar"][player.player_stats["bullets"]
                                                 ].layers["current"] = 1

                    if player.player_stats["bullets"] == 0 and player.player_stats["ammo"] > 0:
                        player.player_stats["bullets"] = 4
                        if left:
                            for b in UIGroup["bulletBar"]:
                                b.layers["current"] = 2
                        else:
                            for b in UIGroup["bulletBar"]:
                                b.layers["current"] = 0

                        player.player_stats["ammo"] -= 1
                        UIGroup["ammoBar"][player.player_stats["ammo"]
                                           ].layers["current"] = 2

                    refilled = False
                    player.shielded = False
                    player.fire = True

            if enemy.damage == True:
                def refil():
                    if not self.refilled:
                        player.player_stats["bullets"] += 1
                        if left:
                            UIGroup["bulletBar"][player.player_stats["bullets"] - 1
                                                 ].layers["current"] = 2
                        else:
                            UIGroup["bulletBar"][player.player_stats["bullets"] - 1
                                                 ].layers["current"] = 0

                        self.refilled = True
                timer = threading.Timer(0.35, refil)
                timer.start()

            if input_handler.keys["shield"]["pressed"] and not input_handler.keys["up"]["pressed"] and not input_handler.keys["down"]["pressed"] and not input_handler.keys["left"]["pressed"] and not input_handler.keys["right"]["pressed"] and not input_handler.keys["shoot"]["pressed"] and player.alive:
                player.shield(deltaTime)
                player.shielded = True

            if enemy.input_handler.keys["shoot"]["pressed"] and player.alive and enemy.player_sprite.position["y"] == player.player_sprite.position["y"] and not player.shielded and enemy.player_stats["bullets"] > 0 and enemy.alive:
                player.take_damage(
                    deltaTime, enemy.input_handler.keys["shoot"]["pressed"])
                if player.damage == False:
                    if player.player_stats["life"] > 0:
                        player.player_stats["life"] -= 1
                        UIGroup["lifeBar"][player.player_stats["life"]
                                           ].layers["current"] = 2

                    if player.player_stats["life"] == 0:
                        player.alive = False

                    player.damage = True
        except:
            print('failed to update')

class Target:
    try:
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
    except:
        print('failed to make targets')


class input_handler:
    try:
        def __init__(self, player_sprite, targets, left=False):
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
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if self.left == True:
                        if e.key == pygame.K_w:
                            self.keys["up"]["pressed"] = True
                            print("here")
                        elif e.key == pygame.K_a:
                            self.keys["left"]["pressed"] = True
                        elif e.key == pygame.K_s:
                            self.keys["down"]["pressed"] = True
                        elif e.key == pygame.K_d:
                            self.keys["right"]["pressed"] = True
                        elif e.key == pygame.K_SPACE:
                            self.keys["shoot"]["pressed"] = True
                        elif e.key == pygame.K_b:
                            print('shield')
                            self.keys["shield"]["pressed"] = True
                    if self.left == False:
                        if e.key == pygame.K_UP:
                            self.keys["up"]["pressed"] = True
                        elif e.key == pygame.K_LEFT:
                            self.keys["left"]["pressed"] = True
                        elif e.key == pygame.K_DOWN:
                            self.keys["down"]["pressed"] = True
                        elif e.key == pygame.K_RIGHT:
                            self.keys["right"]["pressed"] = True
                        elif e.key == pygame.K_RETURN:
                            self.keys["shoot"]["pressed"] = True
                        elif e.key == pygame.K_m:
                            self.keys["shield"]["pressed"] = True
                if e.type == pygame.KEYUP:
                    if self.left == True:
                        if e.key == pygame.K_w:
                            self.keys["up"]["pressed"] = False
                            self.keys["up"]["lastKey"] = False
                        elif e.key == pygame.K_a:
                            self.keys["left"]["pressed"] = False
                            self.keys["left"]["lastKey"] = False
                        elif e.key == pygame.K_s:
                            self.keys["down"]["pressed"] = False
                            self.keys["down"]["lastKey"] = False
                        elif e.key == pygame.K_d:
                            self.keys["right"]["pressed"] = False
                            self.keys["right"]["lastKey"] = False
                        elif e.key == pygame.K_SPACE:
                            self.keys["shoot"]["pressed"] = False
                        elif e.key == pygame.K_b:
                            self.keys["shield"]["pressed"] = False
                    if self.left == False:
                        if e.key == pygame.K_UP:
                            self.keys["up"]["pressed"] = False
                            self.keys["up"]["lastKey"] = False
                        elif e.key == pygame.K_LEFT:
                            self.keys["left"]["pressed"] = False
                            self.keys["left"]["lastKey"] = False
                        elif e.key == pygame.K_DOWN:
                            self.keys["down"]["pressed"] = False
                            self.keys["down"]["lastKey"] = False
                        elif e.key == pygame.K_RIGHT:
                            self.keys["right"]["pressed"] = False
                            self.keys["right"]["lastKey"] = False
                        elif e.key == pygame.K_RETURN:
                            self.keys["shoot"]["pressed"] = False
                        elif e.key == pygame.K_m:
                            print("shield")
                            self.keys["shield"]["pressed"] = False

            if player.alive:
                if self.keys["up"]["pressed"] == True and self.keys["up"]["lastKey"] == False:
                    position = self.player.position
                    for t in self.targets:
                        t.checkTarget()
                        if (t.sprite.position["x"] + t.sprite.width / 2 == self.player.position["x"] + self.player.width / 2) and t.up == True:
                            t.resetTarget()
                            if (t.sprite.position["y"] + t.sprite.height / 8 - self.player.height / 2 - self.player.position["y"] == -62):
                                if (self.player.position == position):
                                    self.player.position = {
                                        "x": self.player.position["x"],
                                        "y": t.sprite.position["y"] + t.sprite.height / 8 - self.player.height / 2
                                    }
                        else:
                            t.resetTarget()
                    print("here 3")
                    self.keys["up"]["lastKey"] = True
                elif self.keys["left"]["pressed"] and self.keys["left"]["lastKey"] == False:
                    position = self.player.position
                    for t in self.targets:
                        t.checkTarget()
                        if (t.sprite.position["y"] + t.sprite.height / 8 == self.player.position["y"] + self.player.height / 2) and t.left:
                            t.resetTarget()
                            if (t.sprite.position["x"] + t.sprite.width / 2 - self.player.width / 2 - self.player.position["x"] == -62):
                                if (self.player.position == position):
                                    self.player.position = {
                                        "x": t.sprite.position["x"] + t.sprite.width / 2 - self.player.width / 2,
                                        "y": self.player.position["y"]
                                    }
                        else:
                            t.resetTarget()
                    self.keys["left"]["lastKey"] = True
                elif self.keys["down"]["pressed"] and self.keys["down"]["lastKey"] == False:
                    position = self.player.position
                    for t in self.targets:
                        t.checkTarget()
                        if (t.sprite.position["x"] + t.sprite.width / 2 == self.player.position["x"] + self.player.width / 2) and t.down:
                            t.resetTarget()
                            if (t.sprite.position["y"] + t.sprite.height / 8 - self.player.height / 2 - self.player.position["y"] == 62):
                                if (self.player.position == position):
                                    self.player.position = {
                                        "x": self.player.position["x"],
                                        "y": t.sprite.position["y"] + t.sprite.height / 8 - self.player.height / 2
                                    }
                        else:
                            t.resetTarget()
                    self.keys["down"]["lastKey"] = True
                elif self.keys["right"]["pressed"] and self.keys["right"]["lastKey"] == False:
                    position = self.player.position
                    for t in self.targets:
                        t.checkTarget()
                        if (t.sprite.position["y"] + t.sprite.height / 8 == self.player.position["y"] + self.player.height / 2) and t.right:
                            t.resetTarget()
                            if (t.sprite.position["x"] + t.sprite.width / 2 - self.player.width / 2 - self.player.position["x"] == 62):
                                if (self.player.position == position):
                                    self.player.position = {
                                        "x": t.sprite.position["x"] + t.sprite.width / 2 - self.player.width / 2,
                                        "y": self.player.position["y"]
                                    }
                        else:
                            t.resetTarget()
                    self.keys["right"]["lastKey"] = True
    except:
        print('failed to handle input')


class Player:
    try:
        def __init__(self, player_sprite, input_handler):
            self.player_sprite = player_sprite
            self.input_handler = input_handler
            self.fps = 6
            self.frame_timer = 0
            self.frame_interval = 1000 / self.fps
            self.player_stats = {
                "life": 5,
                "ammo": 3,
                "bullets": 4,
            }
            self.fire = False
            self.damage = False
            self.alive = True
            self.shielded = False

        def die(self):
            self.player_sprite.frames["current"] = 0
            self.player_sprite.layers["current"] = 0

        def idle(self):
            self.player_sprite.frames["current"] = 0
            self.player_sprite.layers["current"] = 1

        def move_up_down(self, delta_time):
            self.player_sprite.layers["current"] = 1
            if self.input_handler.keys["up"]["pressed"] or self.input_handler.keys["down"]["pressed"]:
                if self.frame_timer > self.frame_interval:
                    if self.player_sprite.frames["current"] >= self.player_sprite.frames["max"] - 1:
                        self.player_sprite.frames["current"] = 0
                        self.player_sprite.frames["current"] += 1
                        self.frame_timer = 0
                else:
                    self.frame_timer += delta_time

        def move_left_right(self, delta_time):
            self.player_sprite.layers["current"] = 2
            if self.input_handler.keys["left"]["pressed"] or self.input_handler.keys["right"]["pressed"]:
                if self.frame_timer > self.frame_interval:
                    if self.player_sprite.frames["current"] >= self.player_sprite.frames["max"] - 1:
                        self.player_sprite.frames["current"] = 0
                        self.player_sprite.frames["current"] += 1
                        self.frame_timer = 0
                else:
                    self.frame_timer += delta_time

        def shoot(self, delta_time):
            self.player_sprite.layers["current"] = 3
            if self.input_handler.keys["shoot"]["pressed"]:
                if self.frame_timer > self.frame_interval:
                    if self.player_sprite.frames["current"] >= self.player_sprite.frames["max"] - 1:
                        self.player_sprite.frames["current"] = 0
                        self.player_sprite.frames["current"] += 1
                        self.frame_timer = 0
                else:
                    self.frame_timer += delta_time

        def take_damage(self, delta_time, enemy_shot):
            self.player_sprite.layers["current"] = 4
            if enemy_shot:
                if self.frame_timer > self.frame_interval:
                    if self.player_sprite.frames["current"] >= self.player_sprite.frames["max"] - 1:
                        self.player_sprite.frames["current"] = 0
                        self.player_sprite.frames["current"] += 1
                        self.frame_timer = 0
                else:
                    self.frame_timer += delta_time

        def shield(self, delta_time):
            self.player_sprite.layers["current"] = 5
            if self.input_handler.keys["shield"]["pressed"]:
                if self.frame_timer > self.frame_interval:
                    if self.player_sprite.frames["current"] >= self.player_sprite.frames["max"] - 1:
                        self.player_sprite.frames["current"] = 0
                        self.player_sprite.frames["current"] += 1
                        self.frame_timer = 0
                else:
                    self.frame_timer += delta_time
    except:
        print('failed to create player')
