# discord importations
import discord
from discord.ext import commands, tasks

# asynchron and threading libraries
import asyncio

# python default librairies
import os
from random import randint, shuffle
from datetime import datetime

# download dependencies
from dotenv import load_dotenv

# own class importations
from entity.inventory.Inventory import Inventory
from entity.inventory.ListInventory import ListInventory
from resources.hu_tao import HU_TAO
from resources.word_hiragana import WORD_HIRAGANA
from resources.word_katakana import WORD_KATAKANA

from utility.debug import debug
from utility.decorator import function_called, function_called_coroutine
from utility.inventory_builder import build_inventory

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()
bot = commands.Bot(command_prefix="!")
bot.remove_command('help')

historic_hiragana = WORD_HIRAGANA.copy()
historic_katakana = WORD_KATAKANA.copy()


@bot.event
async def on_ready():
    debug("Starting bot !")


@bot.command(name="uwu")
@function_called_coroutine
async def uwu(ctx):
    await ctx.send(f"uw{'u' * randint(1, 15)} !!!")


@bot.command(name="hu_tao")
@function_called_coroutine
async def hu_tao(ctx):
    insult = HU_TAO[randint(0, len(HU_TAO) - 1)]
    await ctx.send(f"{insult}")


@bot.command(name="hiragana")
@function_called_coroutine
async def tab_hirigana(ctx):
    with open('resources/img/hiragana-tableau.jpg', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)


@bot.command(name="katakana")
@function_called_coroutine
async def tab_katakana(ctx):
    with open('resources/img/katakana-tableau.jpg', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)


@bot.command(name="get-hiragana")
@function_called_coroutine
async def get_hiragana(ctx):
    global historic_hiragana
    shuffle(historic_hiragana)
    elt = historic_hiragana.pop(0)

    await ctx.send(f"**{elt.word}** ||{elt.romanji}|| ||{elt.traduction}||")

    if len(historic_hiragana) == 0:
        historic_hiragana = WORD_HIRAGANA.copy()
        await ctx.send("Il n'y a plus de mot dans la liste. Re-remplissage automatique.")


@bot.command(name="get-katakana")
@function_called_coroutine
async def get_katakana(ctx):
    global historic_katakana
    shuffle(historic_katakana)
    elt = historic_katakana.pop(0)

    await ctx.send(f"**{elt.word}** ||{elt.romanji}|| : ||{elt.traduction}||")

    if len(historic_katakana) == 0:
        historic_katakana = WORD_KATAKANA.copy()
        await ctx.send("Il n'y a plus de mot dans la liste. Re-remplissage automatique.")


@bot.command(name="aurelie")
@function_called_coroutine
async def aurelie(ctx):
    await ctx.send("bouh bouh bouh")


@bot.command(name="help")
@function_called_coroutine
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour.blue())
    embed.set_author(name='Liste des commandes')

    # Commandes User
    embed.add_field(name="**!uwu**", value="uWuuuuuuuuuuu", inline=False)
    embed.add_field(name="**!hu-tao**", value="Dit des vérités sur le pire perso du jeu", inline=False)
    embed.add_field(name="**!hiragana**", value="Affiche le tableau des hiragana", inline=False)
    embed.add_field(name="**!katakana**", value="Affiche le tableau des katakana", inline=False)
    embed.add_field(name="**!get-hiragana**", value="Retourne un hiragana. Donne la solution en spoiler.", inline=False)
    embed.add_field(name="**!get-katakana**", value="Retourne un katakana. Donne la solution en spoiler.", inline=False)
    await ctx.send(embed=embed)


@bot.command(name="clear")
@function_called_coroutine
async def clear(ctx, number=None):
    if number is None:
        number = 0
        async for _ in ctx.history(limit=None):
            number += 1
    else:
        number = int(number)

    while number > 0:
        if number > 100:
            await ctx.channel.purge(limit=100)
            number -= 100
        else:
            await ctx.channel.purge(limit=number)
            number = 0
        await asyncio.sleep(1.2)


@bot.command(name='create_inv')
async def create_inventory(ctx, *parameters):
    name = " ".join(parameters)
    name_code = "_".join(parameters).lower()

    if len(parameters) == 0:
        await ctx.send(f"Il faut saisir un nom.")
    else:
        inventory = Inventory(name, name_code)
        name_path = f"resources/inventory/inventory-{ ctx.author.id }"

        if os.path.exists(name_path):
            list_inventory = build_inventory(name_path)
        else:
            list_inventory = ListInventory(ctx.author.id, name_path)

        if list_inventory.contains_inventory(name_code):
            await ctx.send(f"Cet inventaire existe déjà.")
        else:
            list_inventory.add_inventory(inventory)
            list_inventory.save_inventory()

            debug(list_inventory, "Create a new inventory")

            await ctx.send(f"L'inventaire a été crée avec succès. Il a pour nom de code : { name_code }.")


@bot.command(name='delete_inv')
async def delete_inventory(ctx, *parameters):
    name_code = "_".join(parameters).lower()

    if len(parameters) == 0:
        await ctx.send(f"Il faut saisir un nom.")
    else:
        name_path = f"resources/inventory/inventory-{ctx.author.id}"

        if os.path.exists(name_path):
            list_inventory = build_inventory(name_path)
        else:
            list_inventory = ListInventory(ctx.author.id, name_path)

        if list_inventory.contains_inventory(name_code):
            list_inventory.remove_inventory(name_code)
            list_inventory.save_inventory()
            debug(list_inventory, f"Delete a {name_code} inventory")
            await ctx.send(f"La suppression a été faite avec succès.")
        else:
            await ctx.send(f"L'inventaire n'existe pas. Il faut entrer le nom de code. Utilisez \"!list_inv\", "
                           f"pour récupérer la liste de vos inventaires.")


@bot.command(name="list_inv")
async def list_inv(ctx):
    name_path = f"resources/inventory/inventory-{ctx.author.id}"

    if not os.path.exists(name_path):
        await ctx.send(f"Vous n'avez pas d'inventaire.")
    else:
        list_inventory = build_inventory(name_path)

        if list_inventory.list_inventories_is_empty():
            await ctx.send(f"Vous n'avez pas d'inventaire.")
        else:
            await ctx.send(f"{list_inventory.get_inventories()}")


@bot.event
@function_called_coroutine
async def on_message(message):
    # if message.content == "pong":
    #    await message.channel.send('ping')
    # elif message.content == "ping":
    #    await message.channel.send("pong")

    await bot.process_commands(message)


@bot.event
@function_called_coroutine
async def on_command_error(ctx, error):
    await ctx.send(f"{error}")


bot.run(TOKEN)
