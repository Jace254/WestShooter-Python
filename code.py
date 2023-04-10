import pygame
import asyncio
from physics import Sprite, Target, input_handler, Player
import time


async def main():
    pygame.init()
    # logo = pygame.image.load("favicon.ico")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("West Shooter")

    # Set up the canvas
    canvas_width = 750
    canvas_height = 500
    screen = pygame.display.set_mode((canvas_width, canvas_height))

    # Set up the background color
    background_color = (199, 116, 56)
    screen.fill(background_color)

    # Load the background image and create a sprite
    background_image = pygame.image.load("./assets/background.png")
    background_sprite = Sprite(
        position={"x": 0, "y": 0}, image=background_image)

    # Set up the left ui bars
    life_image = pygame.image.load("./assets/life_heart.png")
    life_bar_y = canvas_height / 8 - life_image.get_height() / 2
    ammo_image = pygame.image.load("./assets/ammo.png")
    ammo_bar_y = canvas_height / 8 - ammo_image.get_height() / 3 + \
        life_bar_y
    bullet_image = pygame.image.load("./assets/bullet.png")
    left_life_bar = []
    for i in range(5):
        x = canvas_width / 2 - life_image.get_width() / 2 - \
            life_image.get_width() * i - 50
        life_sprite = Sprite(position={"x": x, "y": life_bar_y}, image=life_image, layers={
                             "max": 3, "current": 1})
        left_life_bar.append(life_sprite)

    left_ammo_bar = []
    for i in range(3):
        x = canvas_width / 2 - ammo_image.get_width() / 2 - \
            ammo_image.get_width() * i - 50
        ammo_sprite = Sprite(position={"x": x, "y": ammo_bar_y}, image=ammo_image, layers={
                             "max": 3, "current": 1})
        left_ammo_bar.append(ammo_sprite)

    left_bullet_bar = []
    for i in range(4):
        x = canvas_width / 2 - bullet_image.get_width() / 2 - \
            bullet_image.get_width() * i - 50
        y = canvas_height / 8 - bullet_image.get_height() / 4 + ammo_bar_y
        bullet_sprite = Sprite(position={"x": x, "y": y}, image=bullet_image, layers={
                               "max": 4, "current": 2})
        left_bullet_bar.append(bullet_sprite)

    left_ui_group = {
        "lifeBar": left_life_bar,
        "ammoBar": left_ammo_bar,
        "bulletBar": left_bullet_bar
    }

    # Set up the right ui bars
    right_life_bar = []
    for i in range(5):
        life_bar_y = canvas_height / 8 - life_image.get_height() / 2
        x = canvas_width / 2 - life_image.get_width() / 2 + life_image.get_width() * i + 50
        life_sprite = Sprite(position={"x": x, "y": life_bar_y}, image=life_image, layers={
                             "max": 3, "current": 0})
        right_life_bar.append(life_sprite)

    right_ammo_bar = []
    for i in range(3):
        ammo_bar_y = canvas_height / 8 - ammo_image.get_height() / 3 + life_bar_y
        x = canvas_width / 2 - ammo_image.get_width() / 2 + \
            ammo_image.get_width() * i + 50
        ammo_sprite = Sprite(position={"x": x, "y": ammo_bar_y}, image=ammo_image, layers={
            "max": 3, "current": 0})
        right_ammo_bar.append(ammo_sprite)

    right_bullet_bar = []
    for i in range(4):
        x = canvas_width / 2 - bullet_image.get_width() / 2 + \
            bullet_image.get_width() * i + 50
        y = canvas_height / 8 - bullet_image.get_height() / 4 + ammo_bar_y
        bullet_sprite = Sprite(position={"x": x, "y": y}, image=bullet_image, layers={
                               "max": 4, "current": 0})
        right_bullet_bar.append(bullet_sprite)

    right_ui_group = {
        "lifeBar": right_life_bar,
        "ammoBar": right_ammo_bar,
        "bulletBar": right_bullet_bar
    }

    clock = pygame.time.Clock()

    filter_image = pygame.image.load("./assets/filter.png")
    filter_sprite = Sprite(position={"x": 0, "y": 0}, image=filter_image)

    left_platforms = []
    for i in range(10):
        platform_image = pygame.image.load("./assets/platform.png")
        center = i % 3 == 2
        top = i % 3 == 1
        left = i < 4
        mid = i < 7 and i > 3

        x = (canvas_width / 4 - platform_image.get_width() / 2 - platform_image.get_width()) if left else (canvas_width / 4 -
                                                                                                           platform_image.get_width() / 2 if mid else canvas_width / 4 - platform_image.get_width() / 2 + platform_image.get_width())
        y = (canvas_height / 2 - platform_image.get_height() / 16 - platform_image.get_height() / 2) if top else (canvas_height / 2 -
                                                                                                                  platform_image.get_height() / 16 if center else canvas_height / 2 - platform_image.get_height() / 16 + platform_image.get_height() / 2)
        platform_sprite = Sprite(position={"x": x, "y": y + 75}, image=platform_image, layers={
                                 "max": 2, "current": 0})
        left_platforms.append(platform_sprite)

    right_platforms = []
    for i in range(10):
        platform_image = pygame.image.load("./assets/platform.png")
        center = i % 3 == 2
        top = i % 3 == 1
        left = i < 4
        mid = i < 7 and i > 3

        x = ((canvas_width * 3) / 4 - platform_image.get_width() / 2 - platform_image.get_width()) if left else ((canvas_width * 3) /
                                                                                                                 4 - platform_image.get_width() / 2 if mid else (canvas_width * 3) / 4 - platform_image.get_width() / 2 + platform_image.get_width())
        y = (canvas_height / 2 - platform_image.get_height() / 16 - platform_image.get_height() / 2) if top else (canvas_height / 2 -
                                                                                                                  platform_image.get_height() / 16 if center else canvas_height / 2 - platform_image.get_height() / 16 + platform_image.get_height() / 2)
        platform_sprite = Sprite(position={"x": x, "y": y + 75}, image=platform_image, layers={
                                 "max": 2, "current": 1})
        right_platforms.append(platform_sprite)

    left_player_image = pygame.image.load(
        "./assets/left_shooter.png").convert_alpha()
    left_player_sprite = Sprite(position={"x": canvas_width / 4 - left_player_image.get_width() / 5 / 2, "y": canvas_height / 2 -
                                left_player_image.get_height() / 6 / 2 + 75}, image=left_player_image, frames={"max": 5, "current": 1}, layers={"max": 6, "current": 1})

    right_player_image = pygame.image.load(
        "./assets/right_shooter.png").convert_alpha()
    right_player_sprite = Sprite(position={"x": (canvas_width * 3) / 4 - right_player_image.get_width() / 5 / 2, "y": canvas_height / 2 -
                                           right_player_image.get_height() / 6 / 2 + 75}, image=right_player_image, frames={"max": 5, "current": 1}, layers={"max": 6, "current": 1})

    left_targets = []
    for platform_sprite in left_platforms:
        target = Target(platform_sprite, left_player_sprite)
        left_targets.append(target)

    right_targets = []
    for platform_sprite in right_platforms:
        target = Target(platform_sprite, right_player_sprite)
        right_targets.append(target)

    left_player_input_handler = input_handler(
        left_player_sprite, left_targets, left=True)
    left_player = Player(left_player_sprite, left_player_input_handler)

    right_player_input_handler = input_handler(
        right_player_sprite, right_targets, left=False)
    right_player = Player(right_player_sprite, right_player_input_handler)

    last_time = time.time()

    while True:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((199, 116, 56))
        background_sprite.draw(screen)

        for life_sprite in left_ui_group["lifeBar"]:
            life_sprite.draw(screen)

        for ammo_sprite in left_ui_group["ammoBar"]:
            ammo_sprite.draw(screen)

        for bullet_sprite in left_ui_group["bulletBar"]:
            bullet_sprite.draw(screen)

        for life_sprite in right_ui_group["lifeBar"]:
            life_sprite.draw(screen)

        for ammo_sprite in right_ui_group["ammoBar"]:
            ammo_sprite.draw(screen)

        for bullet_sprite in right_ui_group["bulletBar"]:
            bullet_sprite.draw(screen)

        for platform_sprite in left_platforms:
            platform_sprite.draw(screen)

        for platform_sprite in right_platforms:
            platform_sprite.draw(screen)

        left_player_sprite.draw(screen)
        right_player_sprite.draw(screen)

        left_player_sprite.update(
            left_player_input_handler,
            left_player,
            delta_time,
            left_ui_group,
            True,
            right_player
        )
        right_player_sprite.update(
            right_player_input_handler,
            right_player,
            delta_time,
            right_ui_group,
            False,
            left_player
        )

        filter_sprite.draw(screen)


        pygame.display.update()
        await asyncio.sleep(0)


if __name__ == "__main__":
    # call the main function
    asyncio.run(main())
