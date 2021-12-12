import discord
from discord.embeds import Embed


class EmbedPaginator(discord.ui.View):
    def __init__(self, embeds:list[discord.Embed]):
        super().__init__()
        self.index = 0
        self.embeds=embeds
        self.count = len(embeds)

    @property
    def current_embed(self):
        return self.embeds[self.index]
    
    @property
    def label(self) -> str:
        return f'Page {self.index+1}/{self.count}'

    async def update_message(self, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.current_embed)

    @discord.ui.button(label="<<", style=discord.ButtonStyle.blurple)
    async def first(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.index = 0
        await self.update_message(interaction)

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def previous(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.index -= 1 if self.index > 0 else 0
        await self.update_message(interaction)

    # @discord.ui.button(label="Page 1", style=discord.ButtonStyle.gray, disabled=True)
    # async def label_button(self, button:discord.ui.Button, interaction:discord.Interaction):
    #     button.label = self.label
    #     print(button.label)


    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def next(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.index += 1 if self.index < len(self.embeds)-1 else 0
        await self.update_message(interaction)

    @discord.ui.button(label=">>", style=discord.ButtonStyle.blurple)
    async def last(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.index = len(self.embeds)-1
        await self.update_message(interaction)
