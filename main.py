import logging
import os
import time
import discord
# from discord import app_commands
import my_secret_token
import codeforces
import euler
import json

LOG_FOLDER = ".local"

def load_json_file(filename):
    data = dict()
    with open(filename) as file:
        data = json.load(file)
    return data

CONFIG = load_json_file("config.json")

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


sources = {
    "euler": euler.Euler(),
    "codeforces": codeforces.Codeforces(),
}

def format_contest(c):
    t = time.time()
    at = time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(c[0]))
    rh = int((c[0]-t)// 3600)
    rm = int((c[0]-t)% 3600 // 60)
    return f"- {c[1]} in {rh}h{str(rm).zfill(2)}m, at {at}\n"

def upcoming(source):
    upcoming = source.get_upcoming()
    res = f"There are {len(upcoming)} upcoming events\n"
    for u in upcoming:
        res += format_contest(upcoming[u]) 
    return res

@client.event 
async def on_message(message):
    msg = str(message.content).lower()
    if msg == '' or message.author == client.user:
        return
    if 'hello' in msg:
        await message.channel.send("Hello my ducklings.")
    if 'info' in msg:
        await message.channel.send('Check me at https://github.com/pokorj54/kACer')
    for source in sources:
        if source in msg:
            await message.channel.send(upcoming(sources[source]))
            
    
from discord.ext import tasks

#TODO get rid of this global object
ANNOUNCED = dict()

async def news_monitoring(channel, source):
    news = source.get_news()
    for msg in news:
        await channel.send(msg)

async def upcoming_monitoring(channel, source):
    global ANNOUNCED
    upcoming = source.get_upcoming()
    for u in upcoming:
        for i,t in enumerate(CONFIG['notification_durations']):
            ut = upcoming[u][0]
            if  time.time() < ut < time.time()+t and (u not in ANNOUNCED or ANNOUNCED[u> i] ):
                await channel.send('Coming soon:\n'+format_contest(upcoming[u]))
                ANNOUNCED[u] = i


@tasks.loop(seconds=CONFIG['refresh_rate'])
async def monitoring():
    await news_monitoring(client.get_channel(CONFIG['channels']['codeforces']), sources["codeforces"])
    await news_monitoring(client.get_channel(CONFIG['channels']['euler']), sources["euler"])
    await upcoming_monitoring(client.get_channel(CONFIG['channels']['codeforces']), sources["codeforces"])
    await upcoming_monitoring(client.get_channel(CONFIG['channels']['euler']), sources["euler"])

def ignore_old_news():
    for source in sources:
        sources[source].get_news()

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))
    ignore_old_news()
    monitoring.start()

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