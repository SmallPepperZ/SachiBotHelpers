import os
with open(os.path.join(os.getcwd(),"storage/helpers.cfg")) as f:
    modules = f.read().split('\n')
if "config" in modules:
    from .database.config_obj import config