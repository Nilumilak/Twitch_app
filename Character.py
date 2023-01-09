import pygame
import database
from datetime import datetime, timedelta
from time import time
from Clod import Clod
import twitch_api

time_counter = timedelta(minutes=1)

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

CHAIR_POOF_REVERSED = list(reversed(CHAIR_POOF))

CHAIR = pygame.image.load('images/chair_poof/chair_poof_07_lowres.png')

WAVE = [pygame.image.load('images/wave_anim/wave_01_lowres.png'),
        pygame.image.load('images/wave_anim/wave_02_lowres.png')] * 10

ClAP = [pygame.image.load('images/clap_anim/clap_alt_01_lowres.png'),
        pygame.image.load('images/clap_anim/clap_alt_02_lowres.png')] * 10

THROW = (([pygame.image.load('images/throw_anim/throw_lowres.png')] * 6) +
         ([pygame.image.load('images/throw_anim/count_5_lowres.png')] * 3) +
         ([pygame.image.load('images/throw_anim/count_4_lowres.png')] * 3) +
         ([pygame.image.load('images/throw_anim/count_3_lowres.png')] * 3) +
         ([pygame.image.load('images/throw_anim/count_2_lowres.png')] * 3) +
         ([pygame.image.load('images/throw_anim/count_1_lowres.png')] * 3))

CATCH = [pygame.image.load('images/catch/catch.png'), ] * 25

CAUGHT = [pygame.image.load('images/caught/pt_1_lowres.png'),
          pygame.image.load('images/caught/pt_2_lowres.png'),
          pygame.image.load('images/caught/pt_3_lowres.png'),
          pygame.image.load('images/caught/pt_4_lowres.png')] * 4

OUCH = [pygame.image.load('images/ouch/fail_overlay_1.png'), pygame.image.load('images/ouch/fail_overlay_2.png')] * 8


class Character:
    lurking_list = []
    positions = {1920: True, 2020: True, 2120: True, 2220: True, 2320: True, 2420: True, 2520: True, 2620: True,
                 2720: True, 2820: True, 2920: True, 3020: True, 3120: True, 3220: True, 3320: True, 3420: True,
                 3520: True, 3620: True, 3720: True}

    def __init__(self, name, screen, points=0):
        self.name = name
        self.screen = screen
        self.points = points
        self.time = datetime.now()

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
        self.move_animation_count = 0  # counter for MOVE frames
        self.leave_animation_count = 0  # counter for LEAVING frames
        self.chair_animation_count = 0  # counter for CHAIR frames
        self.wave_animation_count = 0  # counter for WAVE frames
        self.clap_animation_count = 0  # counter for CLAP frames
        self.catch_animation_count = 0  # counter for CATCH frames
        self.throw_animation_count = 0  # counter for THROW frames
        self.caught_animation_count = 0  # counter for CAUGHT frames
        self.ouch_animation_count = 0  # counter for OUCH frames

        self.clod_amount = 0  # how many clods the character has
        self.target = None

        self.add_lurker(self)

    def points_gain(self):
        if datetime.now() >= self.time + time_counter:
            self.points += 1
            self.time = datetime.now()

    @property
    def all_animations(self):
        return {self.leave_animation_count, self.wave_animation_count, self.clap_animation_count,
                self.catch_animation_count, self.throw_animation_count}

    def move(self):
        """
        The character is going to the seat.
        """
        if self.move_animation_count >= self.animation_speed * len(WALK_LEFT):
            self.move_animation_count = 0
        if self.position > 0:
            self.screen.blit(WALK_LEFT[self.move_animation_count // self.animation_speed], self.image_rect)
            self.screen.blit(self.text, (self.image_rect.centerx - self.text_width / 2, self.image_rect.centery - 70))
            self.move_animation_count += 1
            self.image_rect.centerx -= 6
            self.position -= 1
        else:
            if not any(self.all_animations):  # Checks if other animations aren't working
                self.screen.blit(SIT, self.image_rect)
                self.screen.blit(self.text,
                                 (self.image_rect.centerx - self.text_width / 2, self.image_rect.centery - 70))

    def wave(self):
        """
        The character is waving if other animations isn't called.
        """
        if self.wave_animation_count > 0 and self.position <= 0:
            self.screen.blit(WAVE[self.wave_animation_count // self.animation_speed], self.image_rect)
            self.screen.blit(self.text, (self.image_rect.centerx - self.text_width / 2, self.image_rect.centery - 70))
            self.wave_animation_count -= 1

    def wave_update(self):
        """
        Updates the counter for waving.
        """
        if not any(self.all_animations):  # checks if other animations aren't working
            if self.position <= 0:
                self.wave_animation_count = (len(WAVE) * self.animation_speed) - 1

    def clap(self):
        """
        The character is clapping if other animations isn't called.
        """
        if self.clap_animation_count > 0 and self.position <= 0:
            self.screen.blit(ClAP[self.clap_animation_count // self.animation_speed], self.image_rect)
            self.screen.blit(self.text, (self.image_rect.centerx - self.text_width / 2, self.image_rect.centery - 70))
            self.clap_animation_count -= 1

    def clap_update(self):
        """
        Updates the counter for clapping.
        """
        if not any(self.all_animations):  # checks if other animations aren't working
            if self.position <= 0:
                self.clap_animation_count = (len(ClAP) * self.animation_speed) - 1

    def catch(self):
        """
        The character is trying to catch a clod if other animations isn't called.
        """
        if self.catch_animation_count > 0 and self.position <= 0:
            self.screen.blit(CATCH[self.catch_animation_count // self.animation_speed], self.image_rect)
            self.screen.blit(self.text, (self.image_rect.centerx - self.text_width / 2, self.image_rect.centery - 70))
            self.catch_animation_count -= 1

    def catch_update(self):
        """
        Updates the counter for catching.
        """
        if not any(self.all_animations):  # checks if other animations aren't working
            if self.position <= 0:
                self.catch_animation_count = (len(CATCH) * self.animation_speed) - 1

    def get_a_clod(self):
        """
        The character gets 1 clod.
        """
        self.clod_amount += 1
        self.points -= 10

    def throw(self):
        """
        Throws a clod to another character.
        """
        if self.throw_animation_count > 0 and self.position <= 0:
            self.screen.blit(THROW[self.throw_animation_count // self.animation_speed], self.image_rect)
            self.screen.blit(self.text, (self.image_rect.centerx - self.text_width / 2, self.image_rect.centery - 70))
            self.throw_animation_count -= 1
        if self.throw_animation_count == 14:
            self.clod_amount -= 1
            Clod.clod_list.append(Clod(self.screen, self.seat_point, self.target, self.name))

    def throw_update(self, target):
        """
        Updates the counter for throwing.
        :param target: coordinates of another character
        """
        self.target = target
        if not any(self.all_animations):  # checks if other animations aren't working
            if self.position <= 0:
                self.throw_animation_count = (len(THROW) * self.animation_speed) - 1

    def caught(self):
        """
        Animation if the character caught a clod.
        """
        if self.caught_animation_count > 0 and self.position <= 0 and not self.ouch_animation_count:
            self.screen.blit(CAUGHT[self.caught_animation_count // self.animation_speed], self.image_rect)
            self.caught_animation_count -= 1

    def ouch(self):
        """
        Animation if the character didn't catch a clod.
        """
        if self.ouch_animation_count > 0 and self.position <= 0 and not self.caught_animation_count:
            self.screen.blit(OUCH[self.ouch_animation_count // self.animation_speed], self.image_rect)
            self.ouch_animation_count -= 1

    def clod_collision(self):
        """
        Gets a clod if animation of catching is called.
        Clod hits the character if animation wasn't called.
        """
        for clod in Clod.clod_list:
            if ((self.seat_point - 64) <= clod.x_axis <= (self.seat_point + 64) and clod.y_axis >= 1020
                    and clod.who_threw != self.name):
                clod.stop()
                if self.catch_animation_count:
                    print(self.name + ' got the clod')
                    self.caught_animation_count = (len(CAUGHT) * self.animation_speed) - 1
                    self.clod_amount += 1
                    self.points += 5
                else:
                    print(self.name + ' did not get the clod')
                    self.ouch_animation_count = (len(OUCH) * self.animation_speed) - 1

    def chair_puff(self):
        """
        The chair animation.
        """
        if self.image_rect.centerx < 0 and self.chair_animation_count < (
                len(CHAIR_POOF) * self.animation_speed):  # The chair fades out
            self.screen.blit(CHAIR_POOF_REVERSED[self.chair_animation_count // self.animation_speed],
                             (self.seat_point - self.image_rect.width / 2,
                              self.image_rect.centery - self.image_rect.height / 2))
            self.chair_animation_count += 1

        elif self.position <= 50 and self.chair_animation_count >= (
                len(CHAIR_POOF) * self.animation_speed) or self.leave_animation_count > 0:  # The chair stands
            self.screen.blit(CHAIR, (
                self.seat_point - self.image_rect.width / 2, self.image_rect.centery - self.image_rect.height / 2))

        elif 0 < self.position <= 49:  # The chair fades in
            self.screen.blit(CHAIR_POOF[self.chair_animation_count // self.animation_speed],
                             (self.seat_point - self.image_rect.width / 2,
                              self.image_rect.centery - self.image_rect.height / 2))
            self.chair_animation_count += 1

    def get_vip_status(self):
        """
        Purchase VIP status
        """
        username_id = twitch_api.get_user_id(self.name.lower())
        if username_id:
            status = twitch_api.grant_vip_status(username_id)
            if status:
                if status != 422:
                    self.points -= 300
                    database.update_vip_time(self.name, int(time()))
                    return True
                else:
                    return 422

    def lose_vip_status(self):
        """
        Purchase VIP status
        """
        username_id = twitch_api.get_user_id(self.name.lower())
        if username_id:
            status = twitch_api.remove_vip_status(username_id)
            if status:
                if status != 422:
                    return True
                else:
                    return 422

    def leave(self):
        """
        The character leaves the seat.
        """
        if self.leave_animation_count > 0 and self.position <= 0:
            if self.position <= 0:
                self.screen.blit(WALK_LEFT[self.leave_animation_count // self.animation_speed], self.image_rect)
                self.screen.blit(self.text,
                                 (self.image_rect.centerx - self.text_width / 2, self.image_rect.centery - 70))
                self.leave_animation_count -= 1
                self.image_rect.centerx -= 6
            if self.leave_animation_count <= 0:
                self.leave_animation_count = (len(WALK_LEFT) * self.animation_speed) - 1
            if self.image_rect.centerx <= -1 * (len(CHAIR_POOF_REVERSED) * self.animation_speed * 6):
                database.update_points(self.name, self.points)
                Character.positions[self.pos_place] = True
                Character.lurking_list.remove(self)

    def leave_update(self):
        """
        Updates the counter for leaving.
        """
        if not any(self.all_animations):  # checks if other animations aren't working
            if self.position <= 0:
                self.leave_animation_count = (len(WALK_LEFT) * self.animation_speed) - 1
                self.chair_animation_count = 0

    @classmethod
    def add_lurker(cls, user_name):
        cls.lurking_list.append(user_name)

    @classmethod
    def show_lurkers(cls):
        return ', '.join([something.name for something in cls.lurking_list])
