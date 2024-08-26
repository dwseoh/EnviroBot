import os
import discord
from discord.ext import commands


from dotenv import load_dotenv  # This is the tool to load environment variables


# Load environment variables from a .env file


# HELLOOOOOOOOOOOOOOOOOOOOOOOOOOOOo testing
load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')


intents = discord.Intents.all()
activity = discord.Game(name="hello testing")

client = commands.Bot(case_insensitive=True,
                          command_prefix='?',
                          intents=intents,
                          status=discord.Status.dnd)

@client.event
async def on_ready():
    print("We have logged in as", client.user)



@client.command()
async def test(ctx):
    print("test")

client.run(token)