import os
import discord
import requests
from discord.ext import commands

GITHUB_WEBHOOK_URL = "https://discord.com/api/webhooks/WEBHOOK_ID/TOKEN"

DISCORD_TOKEN = "DISCORD_BOT_TOKEN"

NOTIFICATION_CHANNEL_ID = "DISCORD_CHANNEL_ID"

bot = commands.Bot(command_prefix='!')

async def send_notification(message):
    channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
    await channel.send(message)

@bot.route("/github-webhook", methods=["POST"])
async def github_webhook(request):
    if request.json:
        if request.json.get("action") == "created" and request.json.get("ref_type") == "tag":
            file_name = request.json.get("release").get("tag_name")
            message = f"A new file has been uploaded to Github: {file_name}"
            await send_notification(message)
    return "OK"

# Start the bot
bot.run(DISCORD_TOKEN)
