import pygame
import sys

CLOD = pygame.image.load('images/clod/ball_lowres.png')


class Clod:
    clod_list = []

    def __init__(self, screen, start, finish, who_threw):
        self.screen = screen

        self.x_axis = start
        self.y_axis = 1000
        self.finish = finish

        self.who_threw = who_threw

        self.x_speed = 2.8573 * ((self.finish - self.x_axis) / 100)
        self.y_speed = 2

        self.max_y_height = 18
        self.ground_position = self.max_y_height * self.y_speed
        self.fly_position = self.max_y_height * self.y_speed

    def fly(self):
        self.x_axis += self.x_speed
        self.fly_position -= self.y_speed
        self.y_axis -= self.fly_position
        self.screen.blit(CLOD, (self.x_axis - 32, self.y_axis - 32))
        if self.y_axis >= 1080:
            print('the clod fell')
            self.stop()

    def stop(self):
        Clod.clod_list.remove(self)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1920, 1020))
    pygame.display.set_caption('twitch_app')
    bg_color = (0, 0, 0)
    Clod.clod_list.append(Clod(screen, 100, 500, 'pianoparrot'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(bg_color)

        [c.fly() for c in Clod.clod_list]

        pygame.display.update()
        pygame.time.delay(40)
