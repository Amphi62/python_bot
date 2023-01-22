# discord importations
import re

import discord
from discord.ext import commands

# asynchron and threading libraries
import asyncio

# python default librairies
import os
from random import randint, shuffle
from datetime import datetime

# download dependencies
from dotenv import load_dotenv

# own class importations
from resources.hu_tao import HU_TAO
from resources.word_hiragana import WORD_HIRAGANA
from resources.word_katakana import WORD_KATAKANA
from service.GameService import GameService
from utility.debug import debug
from utility.decorator import function_called_coroutine
from utility.game import build_instant_gaming_object, check_link_game_exist

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

historic_hiragana = WORD_HIRAGANA.copy()
historic_katakana = WORD_KATAKANA.copy()

game_service = GameService()


# ---------- Event (start and error events) ----------
@bot.event
async def on_ready():
    debug("Starting bot !")


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"{error}")


# ---------- Extras ----------
@bot.command(name="uwu")
async def uwu(ctx):
    await ctx.send(f"uw{'u' * randint(1, 15)} !!!")


@bot.command(name="hu_tao")
async def hu_tao(ctx):
    insult = HU_TAO[randint(0, len(HU_TAO) - 1)]
    await ctx.send(f"{insult}")


@bot.command(name="aurelie")
async def aurelie(ctx):
    await ctx.send("bouh bouh bouh")


# ---------- Japanese learning ----------
@bot.command(name="hiragana")
async def tab_hirigana(ctx):
    with open('resources/img/hiragana-tableau.jpg', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)


@bot.command(name="katakana")
async def tab_katakana(ctx):
    with open('resources/img/katakana-tableau.jpg', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)


@bot.command(name="get-hiragana")
async def get_hiragana(ctx):
    global historic_hiragana
    shuffle(historic_hiragana)
    elt = historic_hiragana.pop(0)

    await ctx.send(f"**{elt.word}** ||{elt.romanji}|| ||{elt.traduction}||")

    if len(historic_hiragana) == 0:
        historic_hiragana = WORD_HIRAGANA.copy()
        await ctx.send("Il n'y a plus de mot dans la liste. Re-remplissage automatique.")


@bot.command(name="get-katakana")
async def get_katakana(ctx):
    global historic_katakana
    shuffle(historic_katakana)
    elt = historic_katakana.pop(0)

    await ctx.send(f"**{elt.word}** ||{elt.romanji}|| : ||{elt.traduction}||")

    if len(historic_katakana) == 0:
        historic_katakana = WORD_KATAKANA.copy()
        await ctx.send("Il n'y a plus de mot dans la liste. Re-remplissage automatique.")


# ---------- Clear command ----------
@bot.command(name="clear")
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


# ---------- InstantGaming and Steam commands ----------
@bot.command("add_game")
async def add_game_to_list(ctx, *arguments):
    steam_link = None
    instant_gaming_link = None
    name_game = []

    for arg in arguments:
        if re.match(r'https://.*instant-gaming.*', arg) and check_link_game_exist(arg):
            instant_gaming_link = arg
        elif re.match(r'https://.*steam.*', arg) and check_link_game_exist(arg):
            steam_link = arg
        else:
            name_game.append(arg)

    if len(name_game) == 0 or (len(steam_link) == 0 and len(instant_gaming_link) == 0):
        await ctx.send("Le format est incorrect. Vous devez indiquer le nom du jeu, puis au moins un lien "
                       "InstantGaming ou Steam.")
    else:
        insert_valid = game_service.add(ctx.author.id, " ".join(name_game), instant_gaming_link, steam_link)

        if insert_valid:
            await ctx.send(
                "Le jeu a été ajouté à la liste ! Nous scrutons désormais quotidiennement ses jeux, puis vous "
                "informerons si une réduction apparaît sur les plateformes saisis.")
        else:
            await ctx.send("Le jeu existe déjà.")


@bot.command("delete_game")
async def delete_game_to_list(ctx, *name):
    if len(name) == 0:
        await ctx.send("Vous devez indiquer le nom du jeu à supprimer")
    else:
        name_game = " ".join(name)

        if game_service.delete_game(name_game):
            await ctx.send("Le jeu a bien été supprimé de la liste.")
        else:
            await ctx.send("Le jeu est introuvable ou un problème est survenu.")

bot.run(TOKEN)
