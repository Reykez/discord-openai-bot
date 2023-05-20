import os
import openai
import discord
import string
import random
from discord.ext import commands

print("Starting discord bot...")
openai.api_key = os.getenv("OPENAI_API_KEY")
discord_token = os.getenv("DISCORD_API_KEY") 
channel_category_id = 1109461410309754891
base_channel_id = 1109467454343757865

# Internal Variables
conversations = {}

# FUNCTIONS
def getChatResponse(chatMsg):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": chatMsg,
        }]
    )
    print(completion)
    return completion.choices[0].message.content;

def addToArray(arr, item):
    if not item in arr:
        arr.append(item)

# DISCORD BOT
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def askGPT(ctx, *args):
    arguments = ' '.join(args)
    response = getChatResponse(arguments)
    print('USER:', arguments)
    print('BOT:', response)
    await ctx.send(response)

@bot.command()
async def createChannel(ctx, *args):
    channelName = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    print(channelName)

    guild = ctx.guild
    category = discord.utils.get(guild.categories, id=channel_category_id)
    channel = await guild.create_text_channel(channelName, category=category)

    await ctx.send(f"Channel created: {channel.mention}")

@bot.command()
async def deleteChannel(ctx, *args):
    if not isinstance(ctx.channel, discord.TextChannel) or ctx.channel.category_id != channel_category_id:
        return

    conversations.pop(ctx.channel.id, None)
    await ctx.channel.delete()

@bot.command()
async def chat(ctx, *args):
    if not isinstance(ctx.channel, discord.TextChannel) or ctx.channel.category_id != channel_category_id:
        return

    channel_id = ctx.channel.id
    conversations[channel_id] = {
        "message": ' '.join(args)
    }
    # addToArray(conversations, channel_id)

@bot.event
async def on_message(message):
    if message.author == bot.user or not isinstance(message.channel, discord.TextChannel) or message.channel.category_id != channel_category_id or message.content[0] == '$':
        await bot.process_commands(message)

    print(f"{message.content} - zostanie sprocesowana przez ChatGPT")
    # . zapytać chatgpt
    # . Dodać wiadomość użytkownika i odpowiedź do conversation
    # . Wyrzucić wiadomość na ekran.

@bot.command()
async def test(ctx, *args):
    print(conversations)



bot.run(discord_token)
