import configparser
import pygame
import time
import sys
from twitchio.ext import commands
from threading import Thread
from Character import Character
from Clod import Clod
import database
import twitch_api

config = configparser.ConfigParser()
config.read('settings.ini')
client_id = config['Twitch']['client_id']
client_secret = config['Twitch']['client_secret']
access_token = config['Twitch']['access_token']
token_oauth = config['Twitch']['token_oauth']


# def get_chatters():
#     """
#     Gets list of viewers from chat.
#     """
#     header = {
#         'Authorization': f'Bearer {access_token}',
#         'Client-Id': client_id,
#     }
#     respond = requests.get('https://tmi.twitch.tv/group/user/pianoparrot/chatters', headers=header)
#     return respond.json()['chatters']['viewers'] + respond.json()['chatters']['moderators'] + ['pianoparrot']


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
    """
    Testing function.
    """
    print(ctx.message.raw_data)
    print(ctx.message.content)
    print(ctx.message.content[ctx.message.content.find(' ') + 1:])
    print(ctx.message.author)
    print(ctx.message.echo)
    print(ctx.message.timestamp)
    print(ctx.message.tags)
    print(ctx.message.tags['display-name'])
    print(ctx.message.channel)
    print(ctx.message.id)
    text = ctx.message.content.split(' ', maxsplit=2)
    if len(text) >= 2:
        print(text[1])
    if len(text) == 3:
        print(text[2])
    await ctx.send('this is a test response')


@bot.command(name='lurk')
async def new_lurker(ctx):
    user_name = ctx.message.tags['display-name']

    if user_name in [lurker.name for lurker in Character.lurking_list]:
        await ctx.send(f"Hey {user_name}, you are already lurking :-)")

    elif not any(Character.positions.values()):
        await ctx.send(f"I'm sorry {user_name}, but there are no free seats :-(")

    else:
        if database.check_users(user_name):
            Character(user_name, screen, database.get_points(user_name))
        else:
            database.insert_user(user_name)
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


@bot.command(name='clod')
async def clod(ctx):
    user_name = ctx.message.tags['display-name']

    for lurker in Character.lurking_list:
        if lurker.name == user_name and lurker.position <= 0:
            if lurker.points >= 10:
                lurker.get_a_clod()
                await ctx.send(f"{user_name}, you've got a clod, now you can throw it! -10 points")
            else:
                await ctx.send(f"{user_name}, you need at least 10 points to purchase the clod :-)")


@bot.command(name='numclods')
async def clods(ctx):
    user_name = ctx.message.tags['display-name']

    for lurker in Character.lurking_list:
        if lurker.name == user_name and lurker.position <= 0:
            await ctx.send(f"{user_name}, you have {lurker.clod_amount} clod"+(f"s"*(lurker.clod_amount != 1)))


@bot.command(name='throw')
async def throw(ctx):
    user_name = ctx.message.tags['display-name']
    target = (ctx.message.content[ctx.message.content.find(' ') + 1:])

    for lurker in Character.lurking_list:
        if lurker.name == user_name and lurker.position <= 0 and not any(lurker.all_animations):
            if lurker.clod_amount > 0:
                for aim in Character.lurking_list:
                    if aim.name.lower() == target.lower() and aim.position <= 0:
                        lurker.throw_update(aim.seat_point)
            else:
                await ctx.send(f"{user_name}, you have no clods to throw :-(")


@bot.command(name='catch')
async def catch(ctx):
    user_name = ctx.message.tags['display-name']

    for lurker in Character.lurking_list:
        if lurker.name == user_name:
            lurker.catch_update()


@bot.command(name='points')
async def lurker_points(ctx):
    user_name = ctx.message.tags['display-name']

    for lurker in Character.lurking_list:
        if lurker.name == user_name:
            await ctx.send(f"Your points: {lurker.points}")


@bot.command(name='get_vip_for_a_week')
async def get_vip_for_a_week(ctx):
    user_name = ctx.message.tags['display-name']

    for lurker in Character.lurking_list:
        if lurker.name == user_name:
            if lurker.points >= 300:
                if user_name not in twitch_api.get_vip_list():
                    status = lurker.get_vip_status()
                    if status and status != 422:
                        await ctx.send(f"{user_name} purchased VIP status! :O")
                    else:
                        await ctx.send(f"Sorry {user_name}, something went wrong :\\ Try again in a few seconds")
                else:
                    await ctx.send(f"Hey {user_name}, you already have VIP status :\\")
            else:
                await ctx.send(f"Hey {user_name}, you are too poor :D You need to have 300 points for this")


@bot.command(name='remove_vip_status')
async def remove_vip_status(ctx):
    user_name = ctx.message.tags['display-name']

    for lurker in Character.lurking_list:
        if lurker.name == user_name:
            if user_name in twitch_api.get_vip_list():
                status = lurker.lose_vip_status()
                if status and status != 422:
                    await ctx.send(f"You've been kicked out of the VIP room! :|")
                else:
                    await ctx.send(f"Sorry {user_name}, something went wrong :\\ Try again in a few seconds")
            else:
                await ctx.send(f"Hey {user_name}, you are just a regular :D")


@bot.command(name='timeout')
async def timeout(ctx):
    target = None
    reason = None

    user_name = ctx.message.tags['display-name']
    text = ctx.message.content.split(' ', maxsplit=2)

    if len(text) >= 2:
        target = text[1]
    if len(text) >= 3:
        reason = text[2]

    if target:
        if target.lower() in twitch_api.get_list_of_banned_users():
            await ctx.send(f"{user_name}, somebody already banned {target} :D")
        else:
            for lurker in Character.lurking_list:
                if lurker.name == user_name:
                    if lurker.points >= 100:
                        status = lurker.give_timeout(target, reason if reason else None)
                        if status:
                            await ctx.send(f"{user_name}, just banned {target} :O")
                        else:
                            await ctx.send(f"Sorry {user_name}, something went wrong :\\ Try again in a few seconds")
                    else:
                        await ctx.send(f"{user_name}, you need at least 100 points to use such power B)")


@bot.command(name='leave_all')
async def lurker_leave(ctx):
    user_name = ctx.message.tags['display-name']

    if user_name == 'PianoParrot':
        for lurker in Character.lurking_list:
            if lurker.position <= 0 and not any(lurker.all_animations):
                lurker.leave_update()


@bot.command(name='com_list')
async def com_list(ctx):
    await ctx.send(f"Commands are available: !lurk, !leave, !wave, !clap, !clod, !numclods, !throw username, !catch, !points, !get_vip_for_a_week, !remove_vip_status, !timeout username reason(optional), !lurkers")


@bot.command(name='lurkers')
async def all_lurkers_list(ctx):
    if Character.lurking_list:
        await ctx.send(f"Lurking: {Character.show_lurkers()}")

    else:
        await ctx.send("Nobody is lurking now...")


def checking():
    global past_time
    past_time = time.time()
    current_viewers = twitch_api.get_chatters()
    for lurker in Character.lurking_list:
        if lurker.name.lower() not in current_viewers:
            lurker.leave_update()


def vip_expired():
    all_vip_users = twitch_api.get_vip_list()
    for user in all_vip_users:
        vip_time = database.get_vip_time(user)
        if vip_time and vip_time + 604800 < time.time():
            username_id = twitch_api.get_user_id(user.lower())
            twitch_api.remove_vip_status(username_id)


if __name__ == '__main__':
    vip_expired()
    t1 = Thread(target=bot.run)
    t1.start()
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('twitch_app')
    bg_color = (0, 255, 0)

    past_time = time.time()  # start time

    while True:
        if time.time() >= past_time + 1200:  # if 20 minutes has passed, checks if lurkers are still watching
            t2 = Thread(target=checking)
            t2.start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(bg_color)
        if Character.lurking_list:
            [clod.fly() for clod in Clod.clod_list]
            [(lurker.move(), lurker.chair_puff(), lurker.wave(), lurker.clap(), lurker.points_gain(),
              lurker.clod_collision(), lurker.throw(), lurker.catch(), lurker.caught(),
              lurker.ouch()) for lurker in Character.lurking_list]
            [lurker.leave() for lurker in Character.lurking_list]
        pygame.display.update()
        pygame.time.delay(40)
