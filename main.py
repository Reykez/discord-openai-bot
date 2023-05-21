import os
import openai
import discord
import string
import random
import yaml
from discord.ext import commands

print("Starting discord bot...")
openai.api_key = os.getenv("OPENAI_API_KEY")
discord_token = os.getenv("DISCORD_API_KEY") 

channel_category_id = 1109461410309754891
base_channel_id = 1109467454343757865

# Internal Variables
conversations = {}

# FUNCTIONS
def getChatResponse(messages) -> str:
    print('CHATGPT MESSAGE: ', messages)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    print('Returned content: ', completion.choices)
    return completion.choices[-1].message.content

def mapConversation(conversation, userMessage) -> dict:
    messages = []
    for dialog in conversation:
        messages.append({
            "role": "user",
            "content": dialog["message"]
        })
        messages.append({
            "role": "assistant",
            "content": dialog["response"]
        })
    messages.append({
        "role": "user",
        "content": userMessage     
    })
    return messages

def saveConversation(conversation, channel_id) -> None:
    if not os.path.exists("./conversations"):
        os.makedirs("./conversations")
    with open(f"./conversations/{channel_id}.yml", 'w') as yaml_file:
        yaml.dump(conversation, yaml_file, default_flow_style=False, allow_unicode=True)

def createOrRestoreConversation(channel_id) -> dict:
    if not os.path.isfile(f"./conversations/{channel_id}.yml"):
        return {}
    with open(f"./conversations/{channel_id}.yml", 'r') as yaml_file:
        return yaml.safe_load(yaml_file)

def addToArray(arr, item) -> None:
    if not item in arr:
        arr.append(item)

# DISCORD BOT
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def askGPT(ctx, *args) -> None:
    arguments = ' '.join(args)
    response = getChatResponse(arguments)
    print('USER:', arguments)
    print('BOT:', response)
    await ctx.send(response)

@bot.command()
async def createChannel(ctx, *args) -> None:
    channelName = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    print(channelName)

    guild = ctx.guild
    category = discord.utils.get(guild.categories, id=channel_category_id)
    channel = await guild.create_text_channel(channelName, category=category)

    await ctx.send(f"Channel created ({channel.name}/{channel_id}): {channel.mention}")

@bot.command()
async def deleteChannel(ctx, *args) -> None:
    if not isinstance(ctx.channel, discord.TextChannel) or ctx.channel.category_id != channel_category_id:
        return

    conversations.pop(ctx.channel.id, None)
    await ctx.channel.delete()

@bot.event
async def on_message(message) -> None:
    if message.author == bot.user or not isinstance(message.channel, discord.TextChannel) or message.channel.category_id != channel_category_id or message.content[0] == '$':
        await bot.process_commands(message)
        return

    print(f"{message.content} - zostanie sprocesowana przez ChatGPT")
    
    channel_id = message.channel.id
    if not channel_id in conversations:
        conversations[channel_id] = createOrRestoreConversation(channel_id)

    messages = mapConversation(conversations[channel_id], message.content)
    response = getChatResponse(messages)

    conversations[channel_id].append(
        {
            "message": message.content,
            "response": response
        }
    )

    print('Responding')
    saveConversation(conversations[channel_id], channel_id)
    await message.channel.send(response)

@bot.command()
async def test(ctx, *args) -> None:
    print(conversations)



bot.run(discord_token)
