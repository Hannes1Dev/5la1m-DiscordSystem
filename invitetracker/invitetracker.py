import keep_alive
import os
import discord
from discord.ext import commands


TOKEN = os.environ['token']
bot = commands.Bot(command_prefix='/')

game = discord.Game("Einladungen zählen")
bot.activity = game

@bot.event
async def on_ready():
    print(f'Bot ist bereit: {bot.user.name}')

@bot.event
async def on_member_join(member):
    inviter = await get_inviter(member)
    print(f'{member.name} joined using invitation code {inviter.code} from {inviter.inviter.name}')

async def get_inviter(member):
    invites = await member.guild.invites()
    for invite in invites:
        if invite.inviter == member:
            return invite
    return None

@bot.command(name='invite')
async def get_invites(ctx):
    invites = await ctx.guild.invites()
    invite_counts = {}
    for invite in invites:
        if invite.inviter.name not in invite_counts:
            invite_counts[invite.inviter.name] = invite.uses
        else:
            invite_counts[invite.inviter.name] += invite.uses

    embed = discord.Embed(title="Invite Leaderboard", color=discord.Color.blue())
    for inviter, count in invite_counts.items():
        embed.add_field(name=inviter, value=str(count), inline=False)

    await ctx.send(embed=embed)

keep_alive.keep_alive()
bot.run(TOKEN)