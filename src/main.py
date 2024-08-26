import os
import discord
from discord.ext import commands
from dotenv import load_dotenv  # This is the tool to load environment variables

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Load environment variables from a .env file
load_dotenv()


