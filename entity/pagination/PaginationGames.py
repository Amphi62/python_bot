import discord


def create_embed(data):
    description = "!add_game pour ajouter un jeu manquant"
    embed = discord.Embed(title="Liste des jeux disponibles", description=description)

    for game in data:
        name, instant_gaming_reduction_price, instant_gaming_price, instant_gaming_stock, steam_reduction_price, steam_price = game

        if instant_gaming_reduction_price is None:
            instant_gaming_value = "Instant Gaming : {}".format(instant_gaming_price)
        else:
            instant_gaming_value = "Instant Gaming : ~~{}~~ {}".format(instant_gaming_price, instant_gaming_reduction_price)

        instant_gaming_value += " {} ".format(instant_gaming_stock)

        if steam_reduction_price is None:
            steam_value = "Steam : {}".format(instant_gaming_price)
        else:
            steam_value = "Steam : ~~{}~~ {}".format(instant_gaming_price, instant_gaming_reduction_price)

        build_game_value = "{}\n{}".format(instant_gaming_value, steam_value)

        embed.add_field(name=name, value=build_game_value, inline=False)

    return embed


class PaginationGames(discord.ui.View):
    current_page: int = 1
    sep: int = 1
    data = []

    def __init__(self):
        super().__init__()
        self.update_buttons()

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep])

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=create_embed(data), view=self)

    def update_buttons(self):
        is_first_page = self.current_page == 1
        is_last_page = self.current_page == int(len(self.data) / self.sep)

        self.first_page_button.disabled = is_first_page
        self.prev_button.disabled = is_first_page

        self.next_button.disabled = is_last_page
        self.last_page_button.disabled = is_last_page

    @discord.ui.button(label="|<", style=discord.ButtonStyle.primary)
    async def first_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        until_item = self.current_page * self.sep
        await self.update_message(self.data[:until_item])

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item:until_item])

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item:until_item])

    @discord.ui.button(label=">|", style=discord.ButtonStyle.primary)
    async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = int(len(self.data) / self.sep)
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item:])
