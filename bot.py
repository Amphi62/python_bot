import discord
from discord.ext import commands
from random import randint, shuffle
import os
from dotenv import load_dotenv

from entity.BlindTest import BlindTest
from resources.hu_tao import HU_TAO
from resources.word_hiragana import WORD_HIRAGANA
from resources.word_katakana import WORD_KATAKANA

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()
bot = commands.Bot(command_prefix="!")


historic_hiragana = WORD_HIRAGANA.copy()
historic_katakana = WORD_KATAKANA.copy()


@bot.command(name="uwu")
async def uwu(ctx):
    await ctx.send(f"uw{'u' * randint(1, 15) } !!!")


@bot.command(name="hu_tao")
async def hu_tao(ctx):
    insult = HU_TAO[randint(0, len(HU_TAO) - 1)]
    await ctx.send(f"{insult}")


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


@bot.command(name="create-bt")
# @commands.has_role('admin')
async def create_blind_test(ctx, *args):
    if len(args) < 1:
        await ctx.send("La commande doit au moins être suivi d'un nom")
    else:
        name = args[0]
        number = 3 if len(args) == 1 else args[1]
        blind_test = BlindTest(name, number)

        await ctx.send(f"Blind test num. { blind_test.get_id() } créé avec succès !")


@bot.command(name="get-hiragana")
async def get_hiragana(ctx):
    global historic_hiragana
    shuffle(historic_hiragana)
    elt = historic_hiragana.pop(0)

    await ctx.send(f"**{elt.word}** ||{elt.romanji} : {elt.traduction}||")

    if len(historic_hiragana) == 0:
        historic_hiragana = WORD_HIRAGANA.copy()
        await ctx.send("Il n'y a plus de mot dans la liste. Re-remplissage automatique.")


@bot.command(name="get-katakana")
async def get_katakana(ctx):
    global historic_katakana
    shuffle(historic_katakana)
    elt = historic_katakana.pop(0)

    await ctx.send(f"**{elt.word}** ||{elt.romanji} : {elt.traduction}||")

    if len(historic_katakana) == 0:
        historic_katakana = WORD_KATAKANA.copy()
        await ctx.send("Il n'y a plus de mot dans la liste. Re-remplissage automatique.")


bot.run(TOKEN)
