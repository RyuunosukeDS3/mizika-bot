import discord
import os
import logging
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)


async def load_commands():
    """Dynamically load all command modules inside 'commands' directory"""
    for filename in os.listdir("commands"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"commands.{filename[:-3]}")
            logger.info(f"Loaded command {filename[:-3]}")


async def setup():
    await load_commands()

bot.setup_hook = setup


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")
    guild = bot.guilds[0]
    role_name = "trusted_downloader"
    existing_role = discord.utils.get(guild.roles, name=role_name)

    if not existing_role:
        await guild.create_role(name=role_name)
        logger.info(f"Created role: {role_name}")
    else:
        logger.info(f"Role '{role_name}' already exists.")


@bot.event
async def on_shutdown():
    logger.info("Bot is shutting down, cleaning up connections...")

bot.run(config.TOKEN)
