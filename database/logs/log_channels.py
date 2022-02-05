import discord
from pony.orm.core import PrimaryKey, Required, db_session
from .. import db


class LogChannel(db.Entity):
    _table_ = "log_threads"
    guild_id = PrimaryKey(str)
    log_category = Required(str)
    join_channel = Required(str)
    invite_channel = Required(str)


    def get_join_channel(self, bot:discord.Bot) -> discord.TextChannel:
        return bot.get_channel(int(self.join_channel))

    def get_invite_channel(self, bot:discord.Bot) -> discord.TextChannel:
        return bot.get_channel(int(self.invite_channel))
