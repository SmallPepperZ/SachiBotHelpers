import logging




def handler_maker(filepath:str,name:str,level:int, formatter:logging.Formatter) -> logging.FileHandler:
	handler = logging.FileHandler(filepath)
	handler.set_name(name)
	handler.setLevel(level)
	handler.setFormatter(formatter)
	return handler



msg_format = logging.Formatter(style="{", fmt="{asctime} [{name}/{levelname}] {message}")

class Handlers():
	ERROR    = handler_maker("logs/SachiBot.error.log", "SachiBotError", logging.ERROR, msg_format)
	INFO     = handler_maker("logs/SachiBot.info.log" , "SachiBotInfo" , logging.INFO , msg_format)
	DEBUG    = handler_maker("logs/SachiBot.debug.log", "SachiBotDebug", logging.DEBUG, msg_format)



root_logger:logging.Logger = logging.getLogger("SachiBot")

root_logger.addHandler(Handlers.INFO)
root_logger.addHandler(Handlers.DEBUG)
root_logger.addHandler(Handlers.ERROR)
root_logger.addHandler(logging.StreamHandler())
root_logger.setLevel(logging.DEBUG)
