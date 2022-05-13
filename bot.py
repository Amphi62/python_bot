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
import youtube_dl
from dotenv import load_dotenv

# own class importations
from factory.QueueFactory import QueueFactory
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

queue = QueueFactory.playlist1()


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


@bot.command(name="join")
async def join_room(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name="leave")
async def leave_room(ctx):
    await ctx.voice_client.disconnect()


@bot.command(name="play")
async def play(ctx):
    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(queue.get_current_music().get_url(), download=False)
        new_url = info['formats'][0]['url']

    ctx.voice_client.play(discord.FFmpegPCMAudio(new_url, **FFMPEG_OPTIONS), after=lambda e: next(ctx))


@bot.command(name='pause')
async def pause(ctx):
    if ctx.voice_client.is_playing():
        await ctx.voice_client.pause()
    else:
        await ctx.send("Faudrait p'tête que y'a déjà une musique nan ?")


@bot.command(name='resume')
async def resume(ctx):
    if ctx.voice_client.is_paused():
        await ctx.voice_client.resume()
    else:
        await ctx.send("Faudrait p'tête que y'a déjà une musique nan ?")


@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client.is_playing():
        await ctx.voice_client.stop()
    else:
        await ctx.send("Faudrait p'tête que y'a déjà une musique nan ?")


@bot.command(name='next')
async def next(ctx):
    if ctx.voice_client.is_playing():
        await ctx.voice_client.stop()

    queue.next_music()
    await play(ctx)


@bot.command(name='prev')
async def prev(ctx):
    if ctx.voice_client.is_playing():
        await ctx.voice_client.stop()

    queue.previous_music()
    await play(ctx)


bot.run(TOKEN)
