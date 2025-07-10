import discord
from discord.ext import commands, tasks
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL = 123456789012345678  # Replace with your #🏠︱welcome channel ID
LOG_CHANNEL = 123456789012345678     # Replace with your #logs channel ID
ANNOUNCEMENTS_CHANNEL = 123456789012345678  # Replace with your #📢︱announcements channel ID
MEMBER_ROLE_ID = 123456789012345678  # Replace with your @👱 Members role ID

# ---- On Ready ----
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    daily_quote.start()

# ---- Welcome Message ----
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL)
    await channel.send(f"Welcome {member.mention}! Enjoy your stay 🎉")
    role = member.guild.get_role(MEMBER_ROLE_ID)
    if role:
        await member.add_roles(role)

# ---- Basic Slash Commands ----
@bot.slash_command(guild_ids=[GUILD_ID], description="Ping test")
async def ping(ctx):
    await ctx.respond("🏓 Pong!")

@bot.slash_command(guild_ids=[GUILD_ID], description="Show the server rules")
async def rules(ctx):
    rules_text = """
📜 **Server Rules**

Welcome to the server! We’re here for chill vibes, good convo, and fun times...

(You can paste your full rules here or load them from a file)
    """
    await ctx.respond(rules_text, ephemeral=True)

# ---- Logging Events ----
@bot.event
async def on_message_delete(message):
    log = bot.get_channel(LOG_CHANNEL)
    if message.author.bot:
        return
    await log.send(f"🗑️ Message deleted in {message.channel.mention} by {message.author}: {message.content}")

@bot.event
async def on_message_edit(before, after):
    log = bot.get_channel(LOG_CHANNEL)
    if before.author.bot:
        return
    await log.send(f"✏️ Message edited by {before.author}:\nBefore: {before.content}\nAfter: {after.content}")

@bot.event
async def on_member_remove(member):
    log = bot.get_channel(LOG_CHANNEL)
    await log.send(f"🚪 {member} has left the server.")

# ---- Daily Quote ----
@tasks.loop(hours=24)
async def daily_quote():
    channel = bot.get_channel(ANNOUNCEMENTS_CHANNEL)
    if channel:
        try:
            with open("quotes.txt", "r") as f:
                quotes = f.readlines()
            quote = random.choice(quotes).strip()
            await channel.send(f"📣 **Daily Quote:**\n> {quote}")
        except:
            await channel.send("📣 Daily quote feature failed to load.")

bot.run(TOKEN)
