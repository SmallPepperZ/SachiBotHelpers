from . import config
import discord 

def save_status(cog):
    config.status = [list(cog.bot_member.activity.type)[1], str(cog.bot_member.activity.name), list(cog.bot_member.status)[0]]

async def apply_status(bot:discord.Client):
    status = config.status
    await bot.change_presence(activity=discord.Activity(type=status[0], name=status[1]), status=status[2])

async def changestatus(cog, status_type:discord.Status):
    if cog.bot_member.activity is not None:
        await cog.bot.change_presence(activity=discord.Activity(type=cog.bot_member.activity.type, name=cog.bot_member.activity.name), status=status_type)
    else:
        await cog.bot.change_presence(status=status_type)
    save_status(cog)