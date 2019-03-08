#!/usr/bin/python3.6
import feedparser
from bs4 import BeautifulSoup as bs
import re
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
import discord
import os
import wikipedia
from urllib.request import urlopen
bot = commands.Bot(command_prefix='!')
HOMEDIR = os.path.expanduser('~')
TOKENHOME = "%s/.Moderskeppet/" % (HOMEDIR)

with open(TOKENHOME + "token.txt", "r") as readfile:
    TOKEN = readfile.read().strip()


@bot.command(name='wiki', pass_context=True)
async def wiki(ctx, *, arg):
    wikipedia.set_lang("sv")
    w = wikipedia.summary(arg)
    await bot.say(w)


@bot.command(name='spel', pass_context=True)
async def spel(context, *, arg):
        playing = arg
        await bot.change_presence(game=discord.Game(name=arg))


@bot.command(name='nt', pass_context=True)
async def nt(context, arg):
    d = feedparser.parse('https://www.nt.se/nyheter/norrkoping/rss/')
    for post in d.entries[0:int(arg)]:
        await bot.say(post.title + ": " + post.link + "")


@bot.command(name='svt1', pass_context=True)
async def svt1(context):
    svt1 = urlopen("https://www.svtplay.se/kanaler").read().decode("utf-8")
    soup = bs(svt1, 'html.parser')
    meny = soup.find(class_ = "play_guide-page-program-list-schedule__link").getText()
    time = soup.find(class_ = "play_guide-page-program-list-schedule__time").getText()
    meny = meny[5:]
    await bot.say("%s %s" % (time, meny))


@bot.command(name='mat', pass_context=True)
async def mat(context):
    storm = urlopen("http://www.stormkoket.se").read().decode("utf-8")
    soup = bs(storm, 'html.parser')
    meny1 = soup.find(class_="panel-pane pane-todays-menu").getText()
    meny2 = re.sub('Visa menyn för denna vecka', '', meny1)
    await bot.say(meny2)


@bot.command(name='serverinvite', pass_context=True)
async def inv (context):
    invite = await bot.create_invite(context.message.server, max_uses=1, xkcd=True)
    await bot.send_message(context.message.author, "Inbjudningsurlen är {}".format(invite.url))
    await bot.say("Inbjudningslänk genererad! kolla i pm! ")


@bot.command(pass_context=True)
async def rename(ctx, *,name):
    await bot.edit_profile(username=name)


@bot.event
async def on_ready():
    print('Inloggad som: ' + bot.user.name)


bot.run(TOKEN)
