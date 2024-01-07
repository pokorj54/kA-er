import logging
import os
import time
import discord
# from discord import app_commands
import my_secret_token
import codeforces

LOG_FOLDER = ".local"

def init():
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    logging.basicConfig(
        filename="{}/all.log".format(LOG_FOLDER),
        level="INFO",
        format="%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s",
    )

init()
logger = logging.getLogger(__name__)

TOKEN = my_secret_token.get_token()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
# tree = app_commands.CommandTree(client)

def log_message(message):
    try:
        logger.info(f"Message in {message.channel.guild.name}/{message.channel.name} by {message.author.name}: {message.content}")
    except:
        logger.info(f"Message by {message.author.name}: {message.content}")


def format_contest(c):
        t = time.time()
        at = time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(c['startTimeSeconds']))
        rh = int((c['startTimeSeconds']-t)// 3600)
        rm = int((c['startTimeSeconds']-t)% 3600 // 60)
        dh = int(c['durationSeconds']// 3600)
        dm = int(c['durationSeconds']% 3600 // 60)
        return f"- {c['name']} in {rh}h{str(rm).zfill(2)}m, at {at}, duration {dh}:{str(dm).zfill(2)}\n"

def contest_msg():
    contests = codeforces.get_upcoming_contests()
    res = f"There are {len(contests)} contests\n"
    for c in contests:
        res += format_contest(c)
    return res

@client.event 
async def on_message(message):
    msg = str(message.content).lower()
    if msg == '' or message.author == client.user:
        return
    if 'hello' in msg:
        await message.channel.send("Hello my ducklings.")
    if 'contests' in msg:
        await message.channel.send(contest_msg())
    if 'info' in msg:
        await message.channel.send('Check me at https://github.com/pokorj54/kACer')
    
from discord.ext import tasks

PREV_CONTESTS = None
ANNOUNCED = set()

@tasks.loop(seconds=60)
async def contest_monitoring(channel):
    global PREV_CONTESTS
    global ANNOUNCED
    contests = codeforces.get_unfinished_contests()
    [c.pop('relativeTimeSeconds') for c in contests]
    if PREV_CONTESTS is None:
        PREV_CONTESTS = contests
        return
    for c in contests:
        if c not in PREV_CONTESTS:
            await channel.send('New contest appeared\n'+format_contest(c))
        if  time.time() < c['startTimeSeconds'] < time.time()+3600 and c['id'] not in ANNOUNCED:
            await channel.send('Contest in less than 1 hour\n'+format_contest(c))
    for c in PREV_CONTESTS:
        if c['phase'] == 'SYSTEM_TEST' and c not in contests:
            await channel.send('Contest tests completed\n'+format_contest(c))
    PREV_CONTESTS = contests

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))
    contest_monitoring.start(client.get_channel(920263329585459220))

# TODO config
# TODO better logging

# TODO slash commands
# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
# @tree.command(
#     name="commandname",
#     description="My first application Command",
#     guild=discord.Object(id=858056633636487238)
# )
# async def first_command(interaction):
#     await interaction.response.send_message("Hello!")


client.run(TOKEN)