def pretty_cog_name(cog_name:str) -> str:
	return cog_name.replace('cogs.', '').replace('_', ' ').title().replace('.','/')




def pretty_cog_list(cogs:list[str]) -> list[str]:
	formatted_names = []
	for cog in cogs:
		formatted_names.append(pretty_cog_name(cog))
	return formatted_names


def format_as_path(cog_name:str) -> str:
	return f'cogs.{cog_name}'.replace(' ', '_').lower().replace('/','.')



