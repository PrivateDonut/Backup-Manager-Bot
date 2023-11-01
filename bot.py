from nextcord.ext import commands, tasks
import os

from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot()

#Load Cogs
try:
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            bot.load_extension(f'commands.{filename[:-3]}')
            print(f"Loaded command: {filename}")
except Exception as e:
    print(f"Error loading cog: {e}")

@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")

bot.run(os.getenv('BOT_TOKEN'))
