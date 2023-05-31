import string
import random
import discord
from discord.ext import commands
import conversations_manager as cm
from settings import *


class ChannelManagerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cc'])
    async def createChannel(self, ctx, *args):
        if not isinstance(ctx.channel, discord.TextChannel) or ctx.channel.id != base_channel_id:
            return

        channel_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        category = discord.utils.get(ctx.guild.categories, id=channel_category_id)
        channel = await ctx.guild.create_text_channel(channel_name, category=category)

        await ctx.send(f"Channel created ({channel.name}/{channel.id}): {channel.mention}")

    @commands.command(aliases=['dd'])
    async def deleteChannel(self, ctx, *args):
        if not isinstance(ctx.channel, discord.TextChannel) or ctx.channel.category_id != channel_category_id:
            return

        cm.conversations.pop(ctx.channel.id, None)
        await ctx.channel.delete()


async def setup(bot):
    await bot.add_cog(ChannelManagerCog(bot))
