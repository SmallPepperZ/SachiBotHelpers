import json
import traceback

import discord
from discord.abc import GuildChannel
import requests

from . import config



async def send_error_feedback(ctx, error_string, bot: discord.Bot):
    await ctx.message.add_reaction('<:CommandError:804193351758381086>')
    try:
        await ctx.reply(f"Error:\n```{error_string}```\n{bot.owner.name} will be informed", delete_after=60)
    except discord.errors.HTTPException:
        await ctx.reply(f"An error occurred. {bot.owner.name} will be informed")


async def report_error(ctx, error, bot:discord.Bot, silent:bool=False):
    
    if not silent:
        error_description = str(error).replace(config.pathtohide, '')
        await send_error_feedback(ctx, error_description, bot)
    # Get traceback info

    lines = traceback.format_exception(type(error), error, error.__traceback__)
    traceback_text = ''.join(lines)

    # Github gist configuration
    config.errornum += 1

    traceback_text = traceback_text.replace(config.pathtohide, '')

    apiurl = "https://api.github.com/gists"
    gist_id = config.githubgist
    githubtoken = config.githubtoken

    payload = {"description": "SachiBot Errors - A gist full of errors for my bot",
               "public": False,
               "files": {
                   f"SachiBotPyError {config.errornum:02d}.log": {
                       "content": f'Error - {error} \n\n\n {traceback_text}'
                   }
               }
               }
    # Upload to github gist
    requests.patch(f'{apiurl}/{gist_id}',
                   headers={'Authorization': f'token {githubtoken}'},
                   params={'scope': 'gist'},
                   data=json.dumps(payload))
    # Build and send embed for error channel
    channel = bot.get_channel(config.errorchannel)

    embed = discord.Embed(title=f"Error {config.errornum:02d}", color=config.embedcolor)

    embed.add_field(name="Message Url:",
                     value=ctx.message.jump_url, inline=False
                    )
    embed.add_field(name="Message:", 
                     value=ctx.message.clean_content, 
                     inline=True
                    )
    embed.add_field(name="Author:",
                     value=ctx.message.author.mention,
                     inline=True
                    )
    embed.add_field(name="\u200B", value='\u200B', inline=True)
    # Check if it was in a guild
    guildname = ctx.guild.name or "DM"
    channelname = ctx.channel.name if isinstance(ctx.channel, GuildChannel) else ctx.author.id

    embed.add_field(name="Guild:", value=guildname, inline=True)
    embed.add_field(name="Channel:", value=channelname, inline=True)
    embed.add_field(name="\u200B", value='\u200B', inline=True)
    embed.add_field(name="Error:", value=f'```{error}```', inline=False)
    embed.add_field(name="Traceback:",
                     value=f'Traceback Gist - '
                           f'[SachiBotPyError {config.errornum:02d}.log](https://gist.github.com/SmallPepperZ/{gist_id}#file-sachibotpyerror-{config.errornum:02d}-log'
                           f' \"Github Gist #{config.errornum:02d}\") ', inline='false'
                     )
    await channel.send(embed=embed)
    
    # Ping owner
    await (await channel.send(bot.owner.mention)).delete()

async def send_cooldown(ctx, error):
	await ctx.message.add_reaction(str('<:Cooldown:804477347780493313>'))
	if str(error.cooldown.type.name) != "default":
		cooldowntype = f'per {error.cooldown.type.name}'
	else:
		cooldowntype = 'global'
		await ctx.reply(f"This command is on a {round(error.cooldown.per, 0)}s {cooldowntype} cooldown. "
						f"Wait {round(error.retry_after, 1)} seconds",
						delete_after=min(10, error.retry_after))