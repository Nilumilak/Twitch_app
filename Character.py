import pygame

WALK_LEFT = [pygame.image.load('images/basic/1.png'), pygame.image.load('images/basic/2.png'),
             pygame.image.load('images/basic/3.png')]

SIT = pygame.image.load('images/basic_sitting_lowres.png')

CHAIR_POOF = [pygame.image.load('images/chair_poof/chair_poof_01_lowres.png'),
              pygame.image.load('images/chair_poof/chair_poof_02_lowres.png'),
              pygame.image.load('images/chair_poof/chair_poof_03_lowres.png'),
              pygame.image.load('images/chair_poof/chair_poof_04_lowres.png'),
              pygame.image.load('images/chair_poof/chair_poof_05_lowres.png'),
              pygame.image.load('images/chair_poof/chair_poof_06_lowres.png'),
              pygame.image.load('images/chair_poof/chair_poof_07_lowres.png')]

CHAIR = pygame.image.load('images/chair_poof/chair_poof_07_lowres.png')

# WAVE = pygame.image.load('')


class Character:
    lurking_list = []
    positions = {1920: True, 2020: True, 2120: True, 2220: True, 2320: True, 2420: True, 2520: True, 2620: True,
                 2720: True, 2820: True, 2920: True, 3020: True, 3120: True, 3220: True, 3320: True, 3420: True,
                 3520: True, 3620: True, 3720: True}

    def __init__(self, name, screen):
        self.name = name
        self.screen = screen

        self.image = SIT
        self.image_rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()  # rectangle (x_axis, y_axis, width, height)

        for pos in Character.positions:  # finding free seat
            if Character.positions[pos]:
                self.pos_place = pos
                Character.positions[pos] = False
                break

        self.image_rect.centerx = self.pos_place  # middle of the image on the x axis
        self.image_rect.centery = 1020  # middle of the image on the y axis

        self.font = pygame.font.SysFont('font', 20)
        self.text = self.font.render(self.name, True, 'white')
        self.text_width = self.text.get_rect().width  # text width

        self.position = 310  # counter while the character is going left
        self.seat_point = self.image_rect.centerx - self.position * 6  # the final point for a character

        self.animation_speed = 3  # speed of changing frames (should be a multiple of len(frames), but NOT SHURE)
        self.move_animation_count = 0  # counter for frames
        self.chair_animation_count = 0  # counter for frames
        # self.wave_animation_count = len(CHAIR_POOF) * self.animation_speed

        self.add_lurker(self)

    def move(self):
        if self.move_animation_count >= self.animation_speed * len(WALK_LEFT):
            self.move_animation_count = 0
        if self.position > 0:
            self.screen.blit(WALK_LEFT[self.move_animation_count // self.animation_speed], self.image_rect)
            self.screen.blit(self.text, (self.image_rect.centerx - self.text_width / 2, self.image_rect.centery - 70))
            self.move_animation_count += 1
            self.image_rect.centerx -= 6
            self.position -= 1
        else:
            # FIXME: if NOT OTHER ANIMATION THEN SHOW IDLE
            self.screen.blit(SIT, self.image_rect)
            self.screen.blit(self.text, (self.image_rect.centerx - self.text_width / 2, self.image_rect.centery - 70))

    def wave(self):
        pass

    def chair_puff(self):
        if self.position <= 50 - (self.animation_speed * len(CHAIR_POOF)):
            self.screen.blit(CHAIR, (
                self.seat_point - self.image_rect.width / 2, self.image_rect.centery - self.image_rect.height / 2))
        elif self.position <= 49:
            self.screen.blit(CHAIR_POOF[self.chair_animation_count // self.animation_speed],
                             (self.seat_point - self.image_rect.width / 2,
                              self.image_rect.centery - self.image_rect.height / 2))
            self.chair_animation_count += 1

    @classmethod
    def add_lurker(cls, user_name):
        cls.lurking_list.append(user_name)

    @classmethod
    def show_lurkers(cls):
        return ', '.join([something.name for something in cls.lurking_list])

    @classmethod
    def leaving(cls, user_name):
        for lurker in cls.lurking_list:
            if lurker.name == user_name:
                cls.positions[lurker.pos_place] = True
                cls.lurking_list.remove(lurker)
