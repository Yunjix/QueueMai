import asyncio
import json
import os
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv("./utils/.env")
TOKEN: str = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

# file readers
with open("utils/owner_ids.0", "r", encoding="utf-8") as tf:
    OWNER_IDS = tf.read()  # recognizes who the owners of the bot is


# grabbing server prefix
def get_server_prefix(client, message):
    with open("data/prefix.json", "r") as f:
        prefix = json.load(f)

    return prefix[str(message.guild.id)]


# bot initializer
client = commands.Bot(
    command_prefix=get_server_prefix, # default is "m!"
    intents=discord.Intents.all(),
    owner_ids=OWNER_IDS
)


# tells the bot is online
@client.event
async def on_ready():
    try:
        synced_commands = await client.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print(f"An error with syncing application commands has occured: {e}")
    print(f"Systems online! Logged in as {client.user}")


# if a server invites the bot, give them default settings
@client.event
async def on_guild_join(guild):
    # add default prefix
    with open("data/prefix.json", "r") as f:
        prefix = json.load(f)

    prefix[str(guild.id)] = "m!"

    with open("data/prefix.json", "w") as f:
        json.dump(prefix, f, indent=4)


@client.event
async def on_guild_remove(guild):
    # remove default prefix on kick
    with open("data/prefix.json", "r") as f:
        prefix = json.load(f)

    prefix.pop(str(guild.id))

    with open("data/prefix.json", "w") as f:
        json.dump(prefix, f, indent=4)


async def load_cogs():
    print("Loading cogs...")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await client.load_extension(f'cogs.{filename[:-3]}')
                print(f"{filename[:-3]} cog is now loaded and ready!")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")


# main run function
async def main():
    async with client:
        await load_cogs()
        await client.start(TOKEN)

asyncio.run(main())
