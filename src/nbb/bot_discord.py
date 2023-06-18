#!/usr/bin/env python3

import os

from nbb.models import get_message
from nbb.config import get_config
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CONF = get_config()

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", None) or CONF["discord"]["token"]


@bot.command(
    help="Get next bus at some stops.",
    brief="Get next bus at some stops.",
)
async def nbb(ctx, *args):
    """Get next bus from the command line."""
    if len(args) == 0:
        args = [None]
    await ctx.channel.send(get_message(CONF, args[0]))


bot.run(DISCORD_TOKEN)
