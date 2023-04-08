import pygame
from physics import Sprite


def main():
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
    left_life_bar = []
    left_life_bar_y = 0
    for i in range(5):
        life_image = pygame.image.load("./assets/life_heart.png")
        left_life_bar_y = canvas_height / 8 - life_image.get_height() / 2
        x = canvas_width / 2 - life_image.get_width() / 2 - \
            life_image.get_width() * i - 50
        life_sprite = Sprite(position={"x": x, "y": left_life_bar_y}, image=life_image, layers={
                             "max": 3, "current": 1})
        left_life_bar.append(life_sprite)

    left_ammo_bar = []
    left_ammo_bar_y = 0
    for i in range(3):
        ammo_image = pygame.image.load("./assets/ammo.png")
        left_ammo_bar_y = canvas_height / 8 - ammo_image.get_height() / 3 + \
            left_life_bar_y
        x = canvas_width / 2 - ammo_image.get_width() / 2 - \
            ammo_image.get_width() * i - 50
        ammo_sprite = Sprite(position={"x": x, "y": left_ammo_bar_y}, image=ammo_image, layers={
                             "max": 3, "current": 1})
        left_ammo_bar.append(ammo_sprite)

    left_bullet_bar = []
    for i in range(5):
        bullet_image = pygame.image.load("./assets/bullet.png")
        x = canvas_width / 2 - bullet_image.get_width() / 2 - \
            bullet_image.get_width() * i - 50
        y = canvas_height / 8 - bullet_image.get_height() / 4 + left_ammo_bar_y
        bullet_sprite = Sprite(position={"x": x, "y": y}, image=bullet_image, layers={
                               "max": 4, "current": 2})
        left_bullet_bar.append(bullet_sprite)

    # Set up the right ui bars
    right_life_bar = []
    right_life_bar_y = 0
    for i in range(5):
        life_image = pygame.image.load("./assets/life_heart.png")
        right_life_bar_y = canvas_height / 8 - life_image.get_height() / 2
        x = canvas_width / 2 - life_image.get_width() / 2 + life_image.get_width() * i + 50
        life_sprite = Sprite(position={"x": x, "y": right_life_bar_y}, image=life_image, layers={
                             "max": 3, "current": 0})
        right_life_bar.append(life_sprite)

    right_ammo_bar = []
    right_ammo_bar_y = 0
    for i in range(3):
        ammo_image = pygame.image.load("./assets/ammo.png")
        right_ammo_bar_y = canvas_height / 8 - ammo_image.get_height() / 3 + \
            right_life_bar_y
        x = canvas_width / 2 - ammo_image.get_width() / 2 + \
            ammo_image.get_width() * i + 50
        ammo_sprite = Sprite(position={"x": x, "y": right_ammo_bar_y}, image=ammo_image, layers={
                             "max": 3, "current": 0})
        right_ammo_bar.append(ammo_sprite)

    right_bullet_bar = []
    for i in range(5):
        bullet_image = pygame.image.load("./assets/bullet.png")
        x = canvas_width / 2 - bullet_image.get_width() / 2 + \
            bullet_image.get_width() * i + 50
        y = canvas_height / 8 - bullet_image.get_height() / 4 + right_ammo_bar_y
        bullet_sprite = Sprite(position={"x": x, "y": y}, image=bullet_image, layers={
                               "max": 4, "current": 0})
        right_bullet_bar.append(bullet_sprite)

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((199, 116, 56))

        background_sprite.draw(screen)

        for life_sprite in left_life_bar:
            life_sprite.draw(screen)

        for ammo_sprite in left_ammo_bar:
            ammo_sprite.draw(screen)

        for bullet_sprite in left_bullet_bar:
            bullet_sprite.draw(screen)

        for life_sprite in right_life_bar:
            life_sprite.draw(screen)

        for ammo_sprite in right_ammo_bar:
            ammo_sprite.draw(screen)

        for bullet_sprite in right_bullet_bar:
            bullet_sprite.draw(screen)

        for platform_sprite in left_platforms:
            platform_sprite.draw(screen)

        filter_sprite.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    # call the main function
    main()
