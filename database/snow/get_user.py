from .db_entries import SnowFighter
from pony.orm.core import ObjectNotFound, db_session

@db_session
def get_user(user_id:int) -> SnowFighter:
    try:
        return SnowFighter[str(user_id)]
    except ObjectNotFound:
            return SnowFighter(user_id=str(user_id))