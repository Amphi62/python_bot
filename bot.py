# discord importations
from typing import Optional

import discord
from discord import Member
from discord.ext import commands, tasks

# asynchron and threading libraries
import asyncio

# python default librairies
import os
import json
import re
from random import randint, shuffle
from datetime import datetime

# download dependencies
from dotenv import load_dotenv

# own class importations
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


def debug(content, title=None):
    with open("logs.txt", "a") as text_file:
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if title is None:
            title = ''
        else:
            title += ' - '

        print(f"[{time}] {title}{content}", file=text_file)


@bot.event
async def on_ready():
    debug("Starting bot !")


@bot.command(name="uwu")
async def uwu(ctx):
    debug("uwu")
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


@bot.command(name='add_date')
async def add_date(ctx, date, *username):
    path, historic_path = build_path_birthday(ctx.guild.id)

    with open(path, 'rb') as data:
        json_values = json.load(data)

        if not is_admin(ctx.author) and already_use(json_values, ctx.author.id):
            await ctx.send("Vous ne pouvez pas ajouter une nouvelle date. Seules les administrateurs peuvent en "
                           "sélectionner plusieurs.")

        if not re.match(r'[0-9]{2}/[0-9]{2}(/([0-9]{4})|([0-9]{2}))?', date):
            await ctx.send("Le format de la date est erroné. Veuillez utilisé l'un des deux formats : jj/mm/YY ou "
                           "jj/mm/YYYY")

        day, month, year = split_date(date)

        if not evaluate_date(day, month, year):
            await ctx.send("La date entrée n'existe pas.")

        new_birth = {
            "username": ' '.join(username),
            "id_user": ctx.author.id,
            "date_add": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "year": year
        }

        build_day = day + "/" + month
        calendar = json_values['calendar']

        if build_day in calendar:
            calendar[build_day].append(new_birth)
        else:
            calendar[build_day] = [new_birth]

        with open(path, 'w') as file:
            json.dump(json_values, file)

        await ctx.send("La date a bien été ajouté !")


@bot.command(name='remove_date')
async def remove_date(ctx):
    path, historic_path = build_path_birthday(ctx.guild.id)

    with open(path, 'rb') as data:
        json_values = json.load(data)

        if not is_admin(ctx.author):
            pass


@bot.event
async def on_message(message):
    # if message.content == "pong":
    #    await message.channel.send('ping')
    # elif message.content == "ping":
    #    await message.channel.send("pong")

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"{ error }")


def build_path_birthday(id_serv: int) -> tuple[str, str]:
    path = 'resources/birthday/birthday-' + str(id_serv) + '.json'
    historic_path = 'resources/historical/hist-birthday-' + str(id_serv) + '.json'

    # if file doesn't exist, we create thus
    create_birthday_file(path, historic_path, id_serv)

    return path, historic_path


def create_birthday_file(path: str, historic_path: str, id_serv: int) -> None:
    if not os.path.exists(path):
        with open(path, 'w') as file:
            data = {
                "id": id_serv,
                "preventAWeekAgo": True,
                "calendar": dict()
            }
            json.dump(data, file)

    if not os.path.exists(historic_path):
        with open(historic_path, 'w') as file:
            data = {
                "day_checked": list()
            }
            json.dump(data, file)


def is_admin(author: Member) -> bool:
    roles = author.roles
    return any(map(lambda r: r.permissions.administrator, roles))


def already_use(datas: dict, id_author: int) -> bool:
    calendar = datas['calendar']

    for key, value in enumerate(calendar):
        if len([birth for birth in value if birth['id_user'] == id_author]) > 0:
            return True

    return False


def split_date(date: str) -> tuple[str, str, Optional[str]]:
    elt = date.split('/')

    day = elt[0]
    month = elt[1]
    year = None

    if len(elt) > 2:
        year = elt[2]

    return day, month, year


def evaluate_date(day: str, month: str, year: Optional[str]) -> bool:
    int_day = int(day)
    int_month = int(month)

    if int_day < 1 or int_month < 1:
        return False

    if int_month % 2 == 1 and int_day > 31:
        return False

    if int_month % 2 == 0 and int_day > 30:
        return False

    if int_month == 2:
        if year is not None:
            if int(year) % 4 != 0 and int_day > 28:
                return False

        if int_day > 29:
            return False

    return True


bot.run(TOKEN)
