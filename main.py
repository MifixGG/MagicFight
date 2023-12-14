import pygame as pg

pg.init()

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 750

CHARACTER_WIDTH = 450
CHARACTER_HEIGHT = 550
INDICATOR_END = 300

FPS = 144

font = pg.font.Font(None, 40)


def load_image(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, height))
    return image


def text_render(text):
    return font.render(str(text), True, "black")


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.load_animations()

        self.image = self.idle_animation_right[0]
        self.current_image = 0
        self.current_animation = self.idle_animation_right

        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)

        self.timer = pg.time.get_ticks()
        self.interval = 200
        self.side = "right"
        self.animation_mode = True

        self.charge_power = 0
        self.charge_indicator = pg.Surface((self.charge_power, 10))
        self.charge_indicator.fill("red")

        self.charge_mode = False
        self.attack_mode = False
        self.attack_interval = 500
        self.fireballs = pg.sprite.Group()

        #-------------------------------------------------------------------------

        self.image_2 = self.idle_animation_right_2[0]
        self.current_image_2 = 0
        self.current_animation_2 = self.idle_animation_right_2

        self.rect_2 = self.image_2.get_rect()
        self.rect_2.center = (1200, SCREEN_HEIGHT // 2)

        self.timer_2 = pg.time.get_ticks()
        self.interval_2 = 200
        self.side_2 = "left"
        self.animation_mode_2 = True

        self.charge_power_2 = 0
        self.charge_indicator_2 = pg.Surface((self.charge_power, 10))
        self.charge_indicator_2.fill("red")

        self.charge_mode_2 = False
        self.attack_mode_2 = False
        self.attack_interval_2 = 500
        self.fireballs = pg.sprite.Group()
        self.fireballs_2 = pg.sprite.Group()

    def load_animations(self):
        self.idle_animation_right = [load_image(f"images/fire wizard/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                                     for i in range(1, 4)]

        self.idle_animation_left = [pg.transform.flip(i, True, False) for i in self.idle_animation_right]

        self.move_animation_right = [load_image(f"images/fire wizard/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                                     for i in range(1, 5)]
        self.move_animation_left = [pg.transform.flip(i, True, False) for i in self.move_animation_right]

        self.charge = [load_image("images/fire wizard/charge.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.charge.append(pg.transform.flip(self.charge[0], True, False))

        self.attack = [load_image("images/fire wizard/attack.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.attack.append(pg.transform.flip(self.attack[0], True, False))

        self.down = [load_image("images/fire wizard/down.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.down.append(pg.transform.flip(self.down[0], True, False))
        #---------------------------------------------------------------------------------------------------------------------
        self.idle_animation_right_2 = [load_image(f"images/earth monk/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                                     for i in range(1, 4)]
        self.idle_animation_left_2 = [pg.transform.flip(i, True, False) for i in self.idle_animation_right_2]
        self.move_animation_right_2 = [load_image(f"images/earth monk/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                                     for i in range(1, 5)]
        self.move_animation_left_2 = [pg.transform.flip(i, True, False) for i in self.move_animation_right_2]

        self.charge_2 = [load_image("images/earth monk/charge.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.charge_2.append(pg.transform.flip(self.charge_2[0], True, False))

        self.attack_2 = [load_image("images/earth monk/attack.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.attack_2.append(pg.transform.flip(self.attack_2[0], True, False))

        self.down_2 = [load_image("images/earth monk/down.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.down_2.append(pg.transform.flip(self.down_2[0], True, False))
    def update(self):
        keys = pg.key.get_pressed()
        direction = 0
        if keys[pg.K_a]:
            self.side = "left"
            direction = -1
        elif keys[pg.K_d]:
            self.side = "right"
            direction = 1
#------------------------------------------
        keys_2 = pg.key.get_pressed()
        direction_2 = 0
        if keys_2[pg.K_LEFT]:
            self.side_2 = "left"
            direction_2 = -1
        elif keys_2[pg.K_RIGHT]:
            self.side_2 = "right"
            direction_2 = 1

        self.handle_attack_mode()
        self.handle_movement(direction, keys, direction_2, keys_2)
        self.handle_animation()

    def handle_attack_mode(self):
        if self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.attack_interval:
                self.attack_mode = False
                self.timer = pg.time.get_ticks()


        #------------------------------------------------------------------

        if self.attack_mode_2:
            if pg.time.get_ticks() - self.timer_2 > self.attack_interval_2:
                self.attack_mode_2 = False
                self.timer_2 = pg.time.get_ticks()


    def handle_animation(self):
        if not self.charge_mode and self.charge_power > 0:
            self.timer = pg.time.get_ticks()
            self.attack_mode = True
        if self.animation_mode and not self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.interval:
                self.current_image += 1
                if self.current_image >= len(self.current_animation):
                    self.current_image = 0
                self.image = self.current_animation[self.current_image]
                self.timer = pg.time.get_ticks()

        if self.charge_mode:
            self.charge_power += 1
            self.charge_indicator = pg.Surface((self.charge_power, 10))
            self.charge_indicator.fill("red")
            if self.charge_power >= INDICATOR_END:
                self.attack_mode = True
                # self.image = self.attack[self.side != "right"]


        if self.attack_mode and self.charge_power > 0:
            fireball_position = self.rect.topright if self.side == "right" else self.rect.topleft
            self.fireballs.add(Fireball(fireball_position, self.side, self.charge_power))
            self.charge_power = 0
            self.charge_mode = False
            self.image = self.attack[self.side != "right"]
            self.timer = pg.time.get_ticks()




        #--------------------------------------------------

        if not self.charge_mode_2 and self.charge_power_2 > 0:
            self.timer_2 = pg.time.get_ticks()
            self.attack_mode_2 = True
        if self.animation_mode_2 and not self.attack_mode_2:
            if pg.time.get_ticks() - self.timer_2 > self.interval_2:
                self.current_image_2 += 1
                if self.current_image_2 >= len(self.current_animation_2):
                    self.current_image_2 = 0
                self.image_2 = self.current_animation_2[self.current_image_2]
                self.timer_2 = pg.time.get_ticks()

        if self.charge_mode_2:
            self.charge_power_2 += 1
            self.charge_indicator_2 = pg.Surface((self.charge_power_2, 10))
            self.charge_indicator_2.fill("green")
            if self.charge_power_2 >= INDICATOR_END:
                self.attack_mode_2 = True
                # self.image = self.attack[self.side != "right"]


        if self.attack_mode_2 and self.charge_power_2 > 0:
            fireball_position_2 = self.rect_2.topright if self.side_2 == "right" else self.rect_2.topleft
            self.fireballs_2.add(Fireball(fireball_position_2, self.side_2, self.charge_power_2))
            self.charge_power_2 = 0
            self.charge_mode_2 = False
            self.image_2 = self.attack_2[self.side_2 != "right"]
            self.timer_2 = pg.time.get_ticks()









    def handle_movement(self, direction, keys, direction_2, keys_2):
        if self.attack_mode:
            return
        self.charge_mode = 0
        if direction != 0:

            self.animation_mode = True
            self.charge_mode = False
            self.rect.x += direction
            self.current_animation = self.move_animation_left if direction == -1 else self.move_animation_right
        elif keys[pg.K_SPACE]:
            self.animation_mode = False
            self.image = self.charge[self.side != "right"]
            self.charge_mode = True



        elif keys[pg.K_s]:
            self.animation_mode = False
            self.image = self.down[self.side != "right"]







        else:

            self.animation_mode = True
            self.charge_mode = False
            self.current_animation = self.idle_animation_left if self.side == "left" else self.idle_animation_right

        #-------------------------------------------------------------------

        if self.attack_mode_2:
            return
        self.charge_mode_2 = 0
        if direction_2 != 0:

            self.animation_mode_2 = True
            self.charge_mode_2 = False
            self.rect_2.x += direction_2
            self.current_animation_2 = self.move_animation_left_2 if direction_2 == -1 else self.move_animation_right_2
        elif keys_2[pg.K_m]:
            self.animation_mode_2 = False
            self.image_2 = self.charge_2[self.side_2 != "right"]
            self.charge_mode_2 = True



        elif keys_2[pg.K_DOWN]:
            self.animation_mode_2 = False
            self.image_2 = self.down_2[self.side_2 != "right"]







        else:

            self.animation_mode_2 = True
            self.charge_mode_2 = False
            self.current_animation_2 = self.idle_animation_left_2 if self.side_2 == "left" else self.idle_animation_right_2
class Fireball(pg.sprite.Sprite):
    def __init__(self, coord, side, power):
        super().__init__()
        self.side = side
        self.power = power

        self.image = load_image("images/fire wizard/magicball.png", (200 + power), (150 + power))
        if self.side == "right":
            self.image = pg.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()

        self.rect.center = coord[0], coord[1] + 120



        #-----------------------------------


        self.side_2 = side
        self.power_2 = power

        self.image_2 = load_image("images/earth monk/magicball.png", (200 + power), (150 + power))
        if self.side_2 == "right":
            self.image_2 = pg.transform.flip(self.image_2, True, False)

        self.rect_2 = self.image_2.get_rect()

        self.rect_2.center = coord[0], coord[1] + 120

    def update(self):
        if self.side == "right":
            self.rect.x += 4
            if self.rect.left >= SCREEN_WIDTH:
                self.kill()
        else:
            self.rect.x -= 4
            if self.rect.right <= 0:
                self.kill()



        #-------------------------------------------------

        if self.side_2 == "right":
            self.rect_2.x += 4
            if self.rect_2.left >= SCREEN_WIDTH:
                self.kill()
        else:
            self.rect_2.x -= 4
            if self.rect_2.right <= 0:
                self.kill()


class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")

        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.foreground = load_image("images/foreground.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = Player()

        self.clock = pg.time.Clock()
        self.run()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

    def update(self):
        self.player.update()
        self.player.fireballs.update()
        self.player.fireballs_2.update()

    def draw(self):
        # Отрисовка интерфейса
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.player.image_2, self.player.rect_2)
        if self.player.charge_mode:
            self.screen.blit(self.player.charge_indicator, (self.player.rect.left + 120, self.player.rect.top))
        if self.player.charge_mode_2:
            self.screen.blit(self.player.charge_indicator_2, (self.player.rect_2.left + 120, self.player.rect_2.top))
        self.player.fireballs.draw(self.screen)
        self.player.fireballs_2.draw(self.screen)
        self.screen.blit(self.foreground, (0, 0))

        pg.display.flip()


if __name__ == "__main__":
    Game()
