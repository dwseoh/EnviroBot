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
                          activity=activity,
                          status=discord.Status.dnd)

@client.event
async def on_ready():
    print("We have logged in as", client.user)


@client.command()
async def DmMember(ctx, member: discord.User, *, message):
    if ctx.message.author.id != 891434702509060106:
        await member.send(message)
        await ctx.message.reply("Done")
    else:
        em = discord.Embed(
            title="<:xmark:1031920790674886787> Command Disabled",
            description="This command is disabled due to abuse usage",
            color=discord.Color.red())
        await ctx.message.channel.send(f"{ctx.author.mention}", embed=em)




@client.command()
async def test(ctx):
    await ctx.message.reply("test")



client.run(token)