import discord
from pony.orm.core import PrimaryKey, Required, Set
from typing import Optional
from .. import db

class SnowFighter(db.Entity):
    user_id = PrimaryKey(str)
    
    fights_initiated = Set("SnowFight", reverse="thrower")
    fights_recieved = Set("SnowFight", reverse="target")

    snowballs_collected = Required(int, default=0)
    snowballs_lost = Required(int, default=0)

    last_collected = Required(float, default=0)

    collection_limit = Required(int, default=5)
    
    defense_bonus = Required(int, default=0)
    aim_bonus = Required(int, default=0)


    @property
    def snowballs_thrown(self):
        return len(self.fights_initiated)
    
    @property
    def snowballs_dropped(self):
        return self.snowballs_lost - self.snowballs_thrown

    @property
    def snowballs_held(self) -> int:
        return self.snowballs_collected - self.snowballs_lost

    @property
    def hit_count(self) -> int:
        return len([fight for fight in self.fights_initiated if fight.is_hit])
    
    @property
    def miss_count(self) -> int:
        return len([fight for fight in self.fights_initiated if not fight.is_hit])

    @property
    def times_hit(self) -> int:
        return len([fight for fight in self.fights_recieved if fight.is_hit])

    @property
    def times_missed(self) -> int:
        return len([fight for fight in self.fights_recieved if not fight.is_hit])

    @property
    def score(self):
        return self.hit_count

    
    

    @property
    def id(self) -> int:
        return int(self.user_id)

    def collect_snowball(self, count=1):
        self.snowballs_collected += count

    def remove_snowball(self, count=1):
        self.snowballs_collected -= count

    def drop_snowballs(self):
        self.snowballs_lost += self.snowballs_held

    async def get_discord_user(self, ctx:discord.ApplicationContext) -> Optional[discord.User]:
        return await ctx.bot.fetch_user(self.id)


class SnowFight(db.Entity):
    _table_ = "snowfights"
    id        = PrimaryKey(int, auto=True)
    
    thrower   = Required(SnowFighter, reverse="fights_initiated")
    target    = Required(SnowFighter, reverse="fights_recieved")
    
    is_hit    = Required(bool)

    timestamp = Required(float)


