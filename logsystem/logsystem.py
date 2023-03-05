import keep_alive
import discord
from discord.ext import commands
import datetime
import os

TOKEN = os.environ['token']
CHANNEL_ID = 1081286669963116634

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='§', intents=intents)

activity = discord.Activity(type=discord.ActivityType.watching, name='den Mitgliedern zu')
bot.activity = activity

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        channel = bot.get_channel(CHANNEL_ID)
        embed = discord.Embed(
            title=f'{member.name} ist dem Sprachkanal "{after.channel.name}" beigetreten',
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.green()
        )
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)
        await channel.send(embed=embed)
    elif before.channel is not None and after.channel is None:
        channel = bot.get_channel(CHANNEL_ID)
        embed = discord.Embed(
            title=f'{member.name} hat den Sprachkanal "{before.channel.name}" verlassen',
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)
        await channel.send(embed=embed)

keep_alive.keep_alive()
bot.run(TOKEN)