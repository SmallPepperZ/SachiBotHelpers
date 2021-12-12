from pony.orm.core import db_session, select
from .db_entries import SnowFighter
class Leaderboard():
    @db_session
    def __init__(self):
        users:list[SnowFighter] = list(select(user for user in SnowFighter))
        users.sort(key=lambda x:x.score, reverse=True)
        self.users = [user for user in users if user.snowballs_thrown > 0]

    @db_session
    def get_rank(self, user_id:int):
        for index, user in enumerate(self.users):
            if int(user.user_id) == user_id:
                return index+1
        return 0