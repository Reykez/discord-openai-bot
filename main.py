import asyncio
import discord
import nest_asyncio
from openai_connector import *
from discord.ext import commands
from settings import *
from conversations_manager import *

print("Starting discord bot...")

# MISCELLANEOUS
nest_asyncio.apply()

# DISCORD BOT
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.command()
async def askGPT(ctx, *args):
    message = ' '.join(args)
    response = get_chat_response([{
        "role": "user",
        "content": message
    }])
    await ctx.send(response)


@bot.command()
async def test(ctx, *args):
    print(conversations)


async def main():
    async with bot:
        await bot.load_extension('cog.channel_manager')
        await bot.load_extension('cog.message_listener')
        await bot.start(discord_token)

asyncio.run(main())
