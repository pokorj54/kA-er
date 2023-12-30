import logging
import os
import time
import discord
from discord import app_commands
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
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))


def log_message(message):
    try:
        logger.info(f"Message in {message.channel.guild.name}/{message.channel.name} by {message.author.name}: {message.content}")
    except:
        logger.info(f"Message by {message.author.name}: {message.content}")


def contest_msg():
    contests = codeforces.get_upcoming_contests()
    res = f"There are {len(contests)} contests\n"
    t = time.time()
    for c in contests:
        at = time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(t-c['relativeTimeSeconds']))
        rh = -c['relativeTimeSeconds']// 3600
        rm = -c['relativeTimeSeconds']% 3600 // 60
        dh = c['durationSeconds']// 3600
        dm = c['durationSeconds']% 3600 // 60
        res += f"- {c['name']} in {rh}h{str(rm).zfill(2)}m, at {at}, duration {dh}:{str(dm).zfill(2)}\n"
    return res

@client.event 
async def on_message(message):
    msg = str(message.content).lower()
    if msg == '' or message.author == client.user:
        return
    print(msg)
    if 'hello' in msg:
        await message.channel.send("Hello my ducklings.")
    if 'contests' in msg:
        await message.channel.send(contest_msg())
        


# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
@tree.command(
    name="commandname",
    description="My first application Command",
    guild=discord.Object(id=858056633636487238)
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")


client.run(TOKEN)