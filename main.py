import requests
from pprint import pprint
import configparser
import pygame
import sys
from twitchio.ext import commands
from threading import Thread
from Character import Character

config = configparser.ConfigParser()
config.read('settings.ini')
client_id = config['Twitch']['client_id']
client_secret = config['Twitch']['client_secret']
access_token = config['Twitch']['access_token']
token_oauth = config['Twitch']['token_oauth']

bot = commands.Bot(
    token=token_oauth,
    client_id=client_id,
    client_secret=client_secret,
    prefix='!',
    initial_channels=['pianoparrot']
)


@bot.event
async def event_message(ctx):
    await bot.handle_commands(ctx)


@bot.command(name='test')
async def test_command(ctx):
    # print(ctx.message.raw_data)
    # print(ctx.message.content)
    # print(ctx.message.author)
    # print(ctx.message.echo)
    # print(ctx.message.timestamp)
    print(ctx.message.tags)
    # print(ctx.message.channel)
    # print(ctx.message.id)
    await ctx.send('this is a test response')


@bot.command(name='lurk')
async def new_lurker(ctx):
    user_name = ctx.message.tags['display-name']

    if user_name in [lurker.name for lurker in Character.lurking_list]:
        await ctx.send(f"Hey {user_name}, you are already lurking :-)")

    elif not any(Character.positions.values()):
        await ctx.send(f"I'm sorry {user_name}, but there are no free seats :-(")

    else:
        Character(user_name, screen)
        await ctx.send(f"{user_name} is now lurking")

@bot.command(name='wave')
async def lurker_wave(ctx):
    user_name = ctx.message.tags['display-name']
    # for lurker in Character.lurking_list:
    #     if lurker.name == user_name:
    #         lurker.wave_action = True


@bot.command(name='lurkers')
async def all_lurkers_list(ctx):
    if Character.lurking_list:
        await ctx.send(f"Lurking: {Character.show_lurkers()}")
    else:
        await ctx.send("Nobody is lurking now...")


@bot.command(name='leave')
async def remove_lurker(ctx):
    user_name = ctx.message.tags['display-name']

    if user_name in [lurker.name for lurker in Character.lurking_list]:
        Character.leaving(user_name)
        await ctx.send(f"{user_name} has left the lurking place")
    else:
        await ctx.send(f"Hey {user_name}, you were not lurking :-)")


class Thread1(Thread):
    def run(self):
        bot.run()


if __name__ == '__main__':
    t1 = Thread1()
    t1.start()
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('twitch_app')
    bg_color = (0, 255, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(bg_color)
        if Character.lurking_list:
            [(lurker.move(), lurker.chair_puff(), lurker.wave()) for lurker in Character.lurking_list]
        pygame.display.update()
        pygame.time.delay(50)
