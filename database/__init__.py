from pony.orm import Database
import os



db = Database()

db.bind(provider="sqlite", filename="../../storage/SachiBotStorage.db", create_db=False)



with open(os.path.join(os.getcwd(),"storage/helpers.cfg")) as f:
    modules = f.read().split('\n')
if "config" in modules:
    from .config import Config
if "invite" in modules:
    from .invites import Invitee
if "snow" in modules:
    from .snow.db_entries import SnowFight, SnowFighter

db.generate_mapping(create_tables=True)


