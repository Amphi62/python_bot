import discord
from discord.ext import commands
from random import randint, shuffle
import os
from dotenv import load_dotenv
import asyncio

from entity.BlindTest import BlindTest
from resources.hu_tao import HU_TAO
from resources.word_hiragana import WORD_HIRAGANA
from resources.word_katakana import WORD_KATAKANA

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()
bot = commands.Bot(command_prefix="!")
bot.remove_command('help')

historic_hiragana = WORD_HIRAGANA.copy()
historic_katakana = WORD_KATAKANA.copy()


@bot.command(name="uwu")
async def uwu(ctx):
    await ctx.send(f"uw{'u' * randint(1, 15)} !!!")


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

        await ctx.send(f"Blind test num. {blind_test.get_id()} créé avec succès !")


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


@bot.command(name="aurelie")
async def aurelie(ctx):
    await ctx.send("bouh bouh bouh")


@bot.command(name="help")
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


@bot.event
async def on_message(message):
    if message.content == "pong":
        await message.channel.send('ping')
    elif message.content == "ping":
        await message.channel.send("pong")

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"La commande n'existe pas !")


bot.run(TOKEN)
