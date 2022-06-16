import requests
from pprint import pprint
import configparser
import pygame
import time
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


def get_chatters():
    header = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
    }
    respond = requests.get('https://tmi.twitch.tv/group/user/pianoparrot/chatters', headers=header)
    # print(respond.status_code)
    # pprint(respond.json())
    return respond.json()['chatters']['viewers'] + respond.json()['chatters']['moderators']


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
    print(ctx.message.raw_data)
    print(ctx.message.content)
    print(ctx.message.author)
    print(ctx.message.echo)
    print(ctx.message.timestamp)
    print(ctx.message.tags)
    print(ctx.message.channel)
    print(ctx.message.id)
    await ctx.send('this is a test response')


@bot.command(name='lurk')
async def new_lurker(ctx):
    user_name = ctx.message.author.name

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

    for lurker in Character.lurking_list:
        if lurker.name == user_name:
            lurker.wave_update()


@bot.command(name='clap')
async def lurker_clap(ctx):
    user_name = ctx.message.tags['display-name']

    for lurker in Character.lurking_list:
        if lurker.name == user_name:
            lurker.clap_update()


@bot.command(name='leave')
async def lurker_leave(ctx):
    user_name = ctx.message.tags['display-name']

    if user_name not in [lurker.name for lurker in Character.lurking_list]:
        await ctx.send(f"Hey {user_name}, you were not lurking :-)")

    else:
        for lurker in Character.lurking_list:
            if lurker.name == user_name and lurker.position <= 0 and not any(lurker.all_animations):
                lurker.leave_update()
                await ctx.send(f"{user_name} has left the lurking place")


@bot.command(name='lurkers')
async def all_lurkers_list(ctx):
    if Character.lurking_list:
        await ctx.send(f"Lurking: {Character.show_lurkers()}")

    else:
        await ctx.send("Nobody is lurking now...")


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

    past_time = time.time()  # start time

    while True:
        if time.time() >= past_time + 600:  # if 10 minutes has passed, checks if lurkers are still watching
            past_time = time.time()
            current_viewers = get_chatters()
            for lurker in Character.lurking_list:
                if lurker.name not in current_viewers:
                    lurker.leave_update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(bg_color)
        if Character.lurking_list:
            [(lurker.move(), lurker.chair_puff(), lurker.wave(), lurker.clap(), lurker.leave()) for lurker in
             Character.lurking_list]
        pygame.display.update()
        pygame.time.delay(40)
