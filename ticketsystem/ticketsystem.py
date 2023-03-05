import discord
from discord.ext import commands
import os
import keep_alive

TICKET_CATEGORY = 1081903658482024541
TICKET_EMOJI = '🎫'
SUPPORT_ROLE = 'Team'
CLOSE_COMMAND = '!close' 

TOKEN = os.environ['token']

bot = commands.Bot(command_prefix='!')

activity = discord.Activity(type=discord.ActivityType.listening, name='dem Ticket System')
bot.activity = activity

@bot.event
async def on_ready():
    print(f'Bot ist bereit: {bot.user.name}')

async def create_ticket(ctx):
    embed = discord.Embed(title="Ticket erstellen", description="Klicken Sie auf das 🎫-Emoji, um ein Ticket zu erstellen.", color=0x00ff00)
    message = await ctx.send(embed=embed)

    await message.add_reaction(TICKET_EMOJI)

@bot.command()
async def ticket(ctx):
    await create_ticket(ctx)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == TICKET_EMOJI and not payload.member.bot:
        guild = bot.get_guild(payload.guild_id)
        category = guild.get_channel(TICKET_CATEGORY)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            payload.member: discord.PermissionOverwrite(read_messages=True),
            discord.utils.get(guild.roles, name=SUPPORT_ROLE): discord.PermissionOverwrite(read_messages=True)
        }
        channel = await category.create_text_channel(name=f'ticket-{payload.member.display_name}', overwrites=overwrites)

        embed = discord.Embed(title="Willkommen in Ihrem Ticket!", description="Ein Support-Mitarbeiter wird sie in kürze unterstützen.", color=0x00ff00)
        await channel.send(f'{payload.member.mention}', embed=embed)

@bot.command()
async def close(ctx):
    if ctx.channel.category_id == TICKET_CATEGORY:
        if ctx.author == ctx.channel.guild.owner or discord.utils.get(ctx.author.roles, name=SUPPORT_ROLE):
            await ctx.channel.delete()
            await ctx.send('Ticket wurde geschlossen.')
        else:
            await ctx.send('Nur der Autor des Tickets und die Support-Rolle können das Ticket schließen.')
    else:
        await ctx.send('Dieser Befehl kann nur in einem Ticket-Kanal ausgeführt werden.')

keep_alive.keep_alive()
bot.run(TOKEN)
